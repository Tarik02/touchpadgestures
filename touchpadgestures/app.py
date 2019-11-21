import dataclasses
import subprocess
import sys
from typing import Optional, List
from time import time
from pathlib import Path
from pkg_resources import resource_string

from touchpadgestures.detectors.detector import Detector
from touchpadgestures.event import Event
from touchpadgestures.event_source import EventSource
from touchpadgestures.info import Info


class App:
    proc: Optional[subprocess.Popen] = None
    proc_upd: int = 0

    detectors: List[Detector] = []
    active_detector: Optional[Detector] = None
    touched = False
    time: float = 0
    ignore_until: float = 0

    timer_next: float = 0
    timer_detector: Optional[Detector] = None

    info: Info

    def __init__(self, props, event_source: EventSource):
        self.props = props
        self.event_source = event_source

        left, right = self.props['LeftEdge'], self.props['RightEdge']
        top, bottom = self.props['TopEdge'], self.props['BottomEdge']
        width, height = right - left, bottom - top
        self.info = Info(
            left=-width // 2,
            right=width // 2,
            top=-width // 2,
            bottom=width // 2,
        )

    def add_detector(self, constructor):
        self.detectors.append(constructor(self))

    def _send(self, detector: Detector, event: Event):
        return detector.handle(self.time, event.x, event.y, event.force, event.fingers, event.area)

    def _ensure_executor(self):
        config_dir = Path.home()/'.config'/'touchpadgestures'
        executor_file = config_dir/'executor.sh'
        if not executor_file.is_file():
            config_dir.mkdir(parents=True, exist_ok=True)
            executor_file.write_bytes(resource_string(__name__, '../etc/executor.sh'))
        if executor_file.stat().st_mtime > self.proc_upd or \
                self.proc is None or \
                self.proc.poll() is None:
            if self.proc is not None:
                try:
                    self.proc.kill()
                except Exception as e:
                    print(e)
            self.proc = subprocess.Popen([
                '/bin/bash',
                str(executor_file),
            ],
                stdin=subprocess.PIPE,
                stdout=sys.stdout,
                cwd=str(config_dir),
            )

    def fix_event(self, event: Event) -> Event:
        # make coordinates be square with center in point (0, 0)
        left, right = self.props['LeftEdge'], self.props['RightEdge']
        top, bottom = self.props['TopEdge'], self.props['BottomEdge']
        width, height = right - left, bottom - top
        x = event.x - left
        y = event.y - top
        x = int((x / width - 0.5) * width)
        y = int((y / height - 0.5) * width)
        return dataclasses.replace(event, x=x, y=y)

    def process_event(self, event: Event):
        if event.is_end:
            if self.touched:
                self.touched = False
                if self.active_detector is not None:
                    self._send(self.active_detector, event)
                    self.active_detector.end(False)
                    self.active_detector = None
                else:
                    for detector in self.detectors:
                        self._send(detector, event)
                        detector.end(False)
                return
        else:
            if not self.touched:
                self.touched = True
                for detector in self.detectors:
                    detector.begin()

        if self.active_detector is not None:
            self._send(self.active_detector, event)
        else:
            for detector in self.detectors:
                if self._send(detector, event):
                    self.active_detector = detector
                    for detector2 in self.detectors:
                        if detector2 != detector:
                            detector2.end(True)
                    break

    def loop(self):
        self.time = time()

        while True:
            timeout = self.timer_next - self.time
            if self.timer_detector is None or timeout <= 0:
                event = self.event_source.get(None)
            else:
                event = self.event_source.get(timeout)

            self.time = time()
            if self.timer_detector is not None and self.time >= self.timer_next:
                detector = self.timer_detector
                self.timer_detector = None
                detector.handle_timer(self.time)

            if event is not None:
                if event.force < 30 and event.fingers != 0:
                    continue
                if self.ignore_until > self.time:
                    continue
                event = self.fix_event(event)
                self.process_event(event)

    def set_timer(self, detector: Detector, moment: float):
        self.timer_detector = detector
        self.timer_next = moment

    def clear_timer(self, detector: Detector):
        if self.timer_detector == detector:
            self.timer_detector = None

    def ignore_events_for(self, duration: float):
        self.ignore_until = self.time + duration

    def exec(self, detector, name: str, args: List[str]):
        self._ensure_executor()
        line = ' '.join([detector.name, name, *args])
        print(line)
        self.proc.stdin.write((line + '\n').encode('utf-8'))
        self.proc.stdin.flush()
