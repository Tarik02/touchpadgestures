from touchpadgestures.detectors.detector import Detector

MAX_INTERVAL = 0.25
LONG_CLICK = 0.4


class TapDetector(Detector):
    name = 'tap'

    state = 0
    sx, sy = 0, 0
    ex, ey = 0, 0
    counter = 0
    big = False

    def begin(self):
        # self.state = 0
        # self.counter = 0
        pass

    def end(self, cancel: bool):
        if cancel:
            # print('cancel')
            self.reset()

    def reset(self):
        self.state = 0
        self.counter = 0
        self.big = False
        self.app.clear_timer(self)
        # print('reset')

    def handle(self, time: float, x: int, y: int, force: int, fingers: int, area: int) -> bool:
        if self.state == 0:
            if force > 45 and (self.counter > 0 or fingers == 3 or area >= 8):
                self.state = 1
                self.set_timer(time + MAX_INTERVAL)

        if self.state == 1:
            if force < 30:
                self.state = 0
                self.counter += 1
                self.set_timer(time + MAX_INTERVAL)

        if self.state == 3:
            if force < 30:
                self.reset()

        if self.state >= 1:
            if area >= 8:
                self.big = True

        return self.counter >= 2 or self.state == 2

    def handle_timer(self, time: float):
        if self.state == 0:
            self.exec('short', str(self.counter), '1' if self.big else '0')
            self.reset()
        elif self.state == 1:
            self.set_timer(time + LONG_CLICK - MAX_INTERVAL)
            self.state = 2
        elif self.state == 2:
            self.counter += 1
            self.state = 3
            self.exec('long', str(self.counter), '1' if self.big else '0')
