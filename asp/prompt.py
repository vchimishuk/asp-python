import acurses
import controller
import window
import color


class Controller(controller.StatusController):
    def prompt(self, ps):
        self.set_input_mode(True)
        s = self.window.prompt(ps).strip()
        self.set_input_mode(False)

        return s

    def set_input_mode(self, on):
        acurses.cursor(on)


class Window(window.Window):
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)

    def prompt(self, ps):
        ps += ':'

        self.erase()
        self.write(1, 0, ps)
        self.refresh()

        left = len(ps) + 2
        input = self.subwin(left, 0, self.width - left, 1).textbox()
        s = input.edit()

        return s
