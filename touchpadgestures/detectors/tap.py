from touchpadgestures.detectors.detector import Detector

MAX_INTERVAL = 0.25
LONG_CLICK = 0.4


class TapDetector(Detector):
    name = 'tap'

    state = 0
    counter = 0
    big = False

    def begin(self):
        if self.state == -1:
            self.state = 0

    def end(self, cancel: bool):
        if cancel:
            self.reset()

    def reset(self):
        self.state = 0
        self.counter = 0
        self.big = False
        self.app.clear_timer(self)

    def handle(self, time: float, x: int, y: int, force: int, fingers: int, area: int) -> bool:
        if self.state == 0 and force > 45:
            if fingers == 3 or (fingers == 1 and area >= 8):
                self.state = 1
            else:
                self.state = -1

        if self.state == 1:
            if force > 45 and (self.counter > 0 or fingers == 3 or area >= 8):
                self.state = 2
                self.set_timer(time + MAX_INTERVAL)

        if self.state == 2:
            if force < 30:
                self.state = 1
                self.counter += 1
                self.set_timer(time + MAX_INTERVAL)

        if self.state == 4:
            if force < 30:
                self.reset()

        if self.state >= 2:
            if area >= 8:
                self.big = True

        return self.counter >= 2 or self.state == 3

    def handle_timer(self, time: float):
        if self.state == 1:
            self.exec('short', str(self.counter), '1' if self.big else '0')
            self.reset()
        elif self.state == 2:
            self.set_timer(time + LONG_CLICK - MAX_INTERVAL)
            self.state = 3
        elif self.state == 3:
            self.counter += 1
            self.state = 4
            self.exec('long', str(self.counter), '1' if self.big else '0')
