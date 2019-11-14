import re
import subprocess
from threading import Thread
from queue import Queue, Empty
from typing import Optional

from touchpadgestures.event import Event

WHITESPACE_RE = re.compile(r'\s+')


class EventSource:
    def __init__(self, proc: subprocess.Popen):
        self.proc = proc
        self.queue = Queue(32)
        self.thread = Thread(target=self._thread_action)
        self.thread.start()

    def _thread_action(self):
        while True:
            line = self.proc.stdout.readline()
            if not line:
                break
            line = line.decode('utf-8').strip()
            items = WHITESPACE_RE.split(line)
            if items[0] == 'time':
                continue
            x, y, force, fingers, area = [int(i) for i in items[1:6]]
            event = Event(x, y, force, fingers, area)
            self.queue.put(event)

    def get(self, timeout: Optional[float]) -> Optional[Event]:
        try:
            return self.queue.get(block=True, timeout=timeout)
        except Empty:
            return None
