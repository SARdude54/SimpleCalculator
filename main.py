import pygame
import sys
import time
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 400, 500

BG = "#050D21"
BTN_BG = "#1B2E5B"
BTN_HOVER = "#22226E"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")
text_font = pygame.font.SysFont('arial', 20)
entry_box_font = pygame.font.SysFont('arial', 40)
clicked = False


class Button(pygame.rect.Rect):
    """
    Button object is a widget that inherits pygame Rect class
    """
    def __init__(self, left, top, width, height, color, text, text_color, hover_color=None, clicked_color=None,):
        super().__init__(left, top, width, height)
        self.color = color
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        self.text_color = text_color
        self.text = text
        self.text_surf = text_font.render(self.text, True, self.text_color)
        self.clicked = False

    def render(self, display: pygame.Surface, mx, my):
        """
        Renders button contents on screen
        :param display: pygame.Surface
        :param mx: double
        :param my: double
        :return: None
        """
        if self.collidepoint(mx, my):
            pygame.draw.rect(display, self.hover_color, self)

        if self.collidepoint(mx, my) and clicked:
            if self.clicked_color is None:
                pygame.draw.rect(display, BTN_BG, self)
            else:
                pygame.draw.rect(display, self.clicked_color, self)
            self.clicked = True
        else:
            self.clicked = False

        if not self.collidepoint(mx, my):
            pygame.draw.rect(display, self.color, self)

        display.blit(self.text_surf, self.center)

    def on_click(self, func):
        """
        sets function when button is pressed
        :param func: function
        :return: None
        """
        if self.clicked:
            func()
            time.sleep(0.1)


class Label(pygame.rect.Rect):
    """
    Label object that inherits pygame Rect
    Renders text on window
    """
    def __init__(self, left, top, width, height, color, text_color):
        super().__init__(left, top, width, height)
        self.color = color
        self.text_color = text_color
        self.text = ""
        self.text_surf = entry_box_font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()

        self.text_pos = [self.left+10, self.center[1]-20]

    def render(self, display: pygame.Surface):
        """
        Renders label contents
        :param display: pygame.Surface
        :return: None
        """
        pygame.draw.rect(display, self.color, self)

        self.text_surf = entry_box_font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()

        display.blit(self.text_surf, self.text_pos)

    def set_text(self, text):
        """
        sets label text
        :param text: str
        :return: None
        """
        self.text += text

    def clear_text(self):
        """
        clears text on label
        :return: None
        """
        self.text = ""


def evaluate():
    """
    Evaluates the mathematical expression
    Calls when equal button is pressed
    :return:
    """
    expression = text_label.text
    text_label.clear_text()
    try:
        text_label.set_text(str(eval(expression)))
    except SyntaxError as e:
        print(e)


text_label = Label(25, 50, WIDTH - 40, 100, BG, WHITE)

buttons = []

for i in range(1, 4):
    buttons.append(Button(75 * i - 50, 200, 60, 60, BTN_BG, str(i), WHITE, BTN_HOVER))
for i in range(4, 7):
    buttons.append(Button(75 * i - 275, 275, 60, 60, BTN_BG, str(i), WHITE, BTN_HOVER))
for i in range(7, 10):
    buttons.append(Button(75 * i - 500, 350, 60, 60, BTN_BG, str(i), WHITE, BTN_HOVER))

btn_0 = Button(25, 425, 60, 60, BTN_BG, "0", WHITE, BTN_HOVER)
btn_dot = Button(100, 425, 60, 60, BTN_BG, ".", WHITE, BTN_HOVER)
btn_eq = Button(175, 425, 60, 60, BTN_BG, "=", WHITE, BTN_HOVER)

btn_plus = Button(250, 275, 60, 60, BTN_BG, "+", WHITE, BTN_HOVER)
btn_minus = Button(325, 275, 60, 60, BTN_BG, "-", WHITE, BTN_HOVER)
btn_multiply = Button(250, 350, 60, 60, BTN_BG, "*", WHITE, BTN_HOVER)
btn_divide = Button(325, 350, 60, 60, BTN_BG, "/", WHITE, BTN_HOVER)

btn_clear = Button(250, 200, 135, 60, BTN_BG, "C", WHITE, BTN_HOVER)

buttons.append(btn_0)
buttons.append(btn_dot)
buttons.append(btn_eq)
buttons.append(btn_plus)
buttons.append(btn_minus)
buttons.append(btn_multiply)
buttons.append(btn_divide)
buttons.append(btn_clear)

while True:
    window.fill(BG)
    mx, my = pygame.mouse.get_pos()

    for button in buttons:
        if button.text in str(list(range(0, 10))) or button.text == "." or button.text == "+" or button.text == "-" or button.text == "*" or button.text == "/":
            button.on_click(lambda: text_label.set_text(button.text))

        if button.text == "C":
            button.on_click(lambda: text_label.clear_text())

        if button.text == "=":
            button.on_click(lambda: evaluate())

    for event in pygame.event.get():

        if event.type == MOUSEBUTTONDOWN:
            clicked = True
        if event.type == MOUSEBUTTONUP:
            clicked = False

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    text_label.render(window)

    for button in buttons:
        button.render(window, mx, my)

    clock.tick(60)
    pygame.display.update()
