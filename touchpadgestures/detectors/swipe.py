from touchpadgestures.util import angle, angle_diff, dist_sqr
from touchpadgestures.detectors.detector import Detector

THRESHOLD1 = 500
THRESHOLD2 = 800
THRESHOLD_REPEAT = 600
THRESHOLD_REPEAT_CANCEL = 500
REPEAT_FIRST_TIMEOUT = 0.6
REPEAT_INTERVAL = 0.8

DIR_NAMES = ['right', 'up', 'left', 'down']
AXIS_NAMES = ['horizontal', 'vertical']


class SwipeDetector(Detector):
    name = 'swipe'

    state = 0
    big = False
    sx, sy = 0, 0
    ex, ey = 0, 0
    start_angle = 0

    repeat_axis = 0

    @property
    def dist_sqr(self):
        return dist_sqr(self.ex, self.ey, self.sx, self.sy)

    @property
    def angle(self):
        return angle(self.ex - self.sx, self.ey - self.sy)

    @property
    def rounded_angle(self):
        a = self.angle
        if a >= 310 or a <= 50:
            return 0
        elif 50 <= a <= 130:
            return 1
        elif 130 <= a <= 230:
            return 2
        elif 230 <= 310:
            return 3

    @property
    def axis_angle(self):
        if self.repeat_axis == 0:
            dist = self.ex - self.sx
            return 0 if dist > 0 else 2
        else:
            dist = self.ey - self.sy
            return 1 if dist > 0 else 3

    def axis_dist(self, axis: int):
        if axis == 0:
            return abs(self.ex - self.sx)
        else:
            return abs(self.ey - self.sy)

    def begin(self):
        self.state = 0

    def end(self, cancel: bool):
        if not cancel:
            if self.state in [3, 4]:
                self.exec(AXIS_NAMES[self.repeat_axis] + '.stop')

    def handle(self, time: float, x: int, y: int, force: int, fingers: int, area: int) -> bool:
        if self.state == -2 or self.state == 0:
            if fingers == 3 or (fingers == 1 and area >= 8):
                self.state = 1
                self.sx, self.sy = x, y
                self.big = area >= 8
            else:
                if self.state != -1 and not (
                    self.app.info.left <= x <= self.app.info.right or
                    self.app.info.top <= y <= self.app.info.bottom
                ):
                    self.state = -1
                else:
                    # if moving from the corner, then set state to -2 and wait for good event
                    self.state = -2

        if self.state >= 1:
            if area >= 8:
                self.big = True

        if self.state == 1:
            self.ex = x
            self.ey = y
            if self.dist_sqr > THRESHOLD1 ** 2:
                self.state = 2
                self.start_angle = self.angle

        if self.state == 2:
            self.ex = x
            self.ey = y
            if angle_diff(self.start_angle, self.angle) > 30:
                print('bad')
                self.state = -1
            if self.dist_sqr > THRESHOLD2 ** 2:
                self.state = 3
                self.repeat_axis = self.rounded_angle % 2
                self.exec(DIR_NAMES[self.rounded_angle], '1' if self.big else '0')

        if self.state >= 3:
            self.sx, self.sy = 0, 0
            self.ex = x
            self.ey = y

        if self.state == 3:
            # print(self.axis_dist(self.repeat_axis))
            if self.axis_dist(self.repeat_axis) < THRESHOLD_REPEAT_CANCEL:
                self.state = 4

        if self.state == 4:
            # print([self.axis_dist(self.repeat_axis), THRESHOLD_REPEAT])
            if self.axis_dist(self.repeat_axis) > THRESHOLD_REPEAT:
                self.exec(
                    AXIS_NAMES[self.repeat_axis] + '.repeat',
                    DIR_NAMES[self.axis_angle],
                )
                self.state = 3

        return self.state >= 2












