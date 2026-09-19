import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MUSIC_MENU, IMG_MENU_BG, IMG_BUTTON
from buttons import ImageButton


class Menu:
    def __init__(self):
        self.button_play = ImageButton(SCREEN_WIDTH/2-(252/2), 100, 252, 74, "PLAY", IMG_BUTTON)
        self.button_exit = ImageButton(SCREEN_WIDTH/2-(252/2), 300, 252, 74, "EXIT", IMG_BUTTON)
        self.music_playing = False

        self.menu_bg = pygame.image.load(IMG_MENU_BG)
        self.menu_bg = pygame.transform.scale(self.menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def start_music(self):
        if not self.music_playing:
            pygame.mixer.music.load(MUSIC_MENU)
            pygame.mixer.music.play(-1)
            self.music_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def run(self, screen):
        self.start_music()

        while True:
            screen.blit(self.menu_bg, (0, 0))

            font = pygame.font.Font(None, 80)
            title = font.render("PIXEL ADVENTURE", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 50))
            screen.blit(title, title_rect)

            mouse_pos = pygame.mouse.get_pos()
            self.button_play.check_hover(mouse_pos)
            self.button_play.draw(screen)
            self.button_exit.check_hover(mouse_pos)
            self.button_exit.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    pygame.quit()
                    exit()
                if self.button_play.handle_event(event):
                    self.stop_music()
                    return
                if self.button_exit.handle_event(event):
                    self.stop_music()
                    pygame.quit()
                    exit()

            pygame.display.flip()
