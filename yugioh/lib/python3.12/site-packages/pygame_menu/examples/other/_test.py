import pygame
import pygame_menu
from pygame import QUIT


class Menu(pygame_menu.Menu):

    def __init__(self):
        super().__init__(title="Test", width=150, height=200, theme=pygame_menu.themes.THEME_DARK.copy())

        help_menu = pygame_menu.Menu(title="Help", width=150,
                                     height=200, theme=pygame_menu.themes.THEME_DARK.copy(),
                                     center_content=True)

        help_menu.add.label("Test label", wordwrap=True,
                            font_size=15, padding=5,
                            align=pygame_menu.locals.ALIGN_CENTER)
        help_menu.add.button("Back", pygame_menu.events.BACK)

        self.add.button("Play", pygame_menu.events.EXIT)
        # if you comment out this line the program works
        self.add.button(help_menu.get_title(), help_menu)
        self.add.button("Quit", pygame_menu.events.EXIT)

        self.enable()


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((500, 400))
    clock = pygame.time.Clock()
    main_menu = Menu()

    while True:
        screen.fill((0, 0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()

        main_menu.update(events)
        main_menu.draw(screen)

        pygame.display.update()

        clock.tick(60)
