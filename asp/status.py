import controller
import window
import color


class Controller(controller.StatusController):
    pass


class Window(window.Window):
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)

        self.set_background(color.STATUS_LINE)
