import subprocess

from touchpadgestures.app import App
from touchpadgestures.detectors.swipe import SwipeDetector
from touchpadgestures.detectors.tap import TapDetector
from touchpadgestures.event_source import EventSource
from touchpadgestures.props import read_props, write_props


def main():
    props = read_props()
    props['TapButton3'] = 0
    write_props(props)

    proc = subprocess.Popen(['synclient', '-ms'], stdout=subprocess.PIPE)
    source = EventSource(proc)

    app = App(props, source)

    app.add_detector(SwipeDetector)
    app.add_detector(TapDetector)

    app.loop()
