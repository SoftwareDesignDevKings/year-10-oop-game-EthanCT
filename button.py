import pygame
from constants import *


class Button:
    def __init__(self, x, y, width, height, text, font,
                 color=(80, 80, 80), hover_color=(120, 120, 120),
                 text_color=(255, 255, 255), border_color=(200, 200, 200),
                 border_width=2):

        self.rect         = pygame.Rect(x, y, width, height)
        self.text         = text
        self.font         = font
        self.color        = color
        self.hover_color  = hover_color
        self.text_color   = text_color
        self.border_color = border_color
        self.border_width = border_width

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        # only fires on a left click, and only if the mouse is actually over the button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered()
        return False

    def draw(self, surface):
        fill = self.hover_color if self.is_hovered() else self.color

        pygame.draw.rect(surface, fill, self.rect, border_radius=6)
        pygame.draw.rect(surface, self.border_color, self.rect,
                         self.border_width, border_radius=6)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)