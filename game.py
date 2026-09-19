import pygame
import random
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MUSIC_GAME, IMG_GAME_BG, IMG_GAME_OVER, IMG_LEVEL_COMPLETE, IMG_BUTTON
)
from hero import Hero
from obstacles import Stone, Fire, Sword
from bonuses import Coin, SlowBonus
from buttons import ImageButton


class Game:
    def __init__(self, level):
        self.level = level
        self.hero = Hero()
        self.score = 0

        if level == 1:
            self.level_time = 60
            self.obstacle_speed = 3
            self.obstacle_count = 2
            self.spawn_rate = 300
        elif level == 2:
            self.level_time = 60
            self.obstacle_speed = 4
            self.obstacle_count = 3
            self.spawn_rate = 200
        else:
            self.level_time = 60
            self.obstacle_speed = 6
            self.obstacle_count = 4
            self.spawn_rate = 100

        self.obstacles = []
        for i in range(self.obstacle_count):
            self.obstacles.append(Stone(
                random.randint(0, SCREEN_WIDTH - 60),
                random.randint(-200, 0),
                self.obstacle_speed
            ))
            self.obstacles.append(Fire(
                random.randint(0, SCREEN_WIDTH - 100),
                random.randint(-200, 0),
                self.obstacle_speed + 1
            ))
            self.obstacles.append(Sword(
                random.randint(0, SCREEN_WIDTH - 40),
                random.randint(-200, 0),
                self.obstacle_speed + 2
            ))

        self.coins = []
        self.coin_spawn_timer = 0
        self.coin_spawn_interval = 1500

        self.bonuses = []
        self.bonus_spawn_timer = 0
        self.bonus_spawn_interval = 20000

        self.button_next = ImageButton(SCREEN_WIDTH/2-(252/2), 350, 252, 74, "NEXT LEVEL", IMG_BUTTON)
        self.button_exit = ImageButton(SCREEN_WIDTH/2-(252/2), 600, 252, 74, "EXIT", IMG_BUTTON)
        self.button_restart = ImageButton(SCREEN_WIDTH/2-(252/2), 700, 252, 74, "START OVER", IMG_BUTTON)
        self.button_menu = ImageButton(SCREEN_WIDTH/2-(252/2), 500, 252, 74, "MENU", IMG_BUTTON)

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.level_complete = False
        self.show_buttons = False
        self.start_ticks = pygame.time.get_ticks()
        self.pause_start_ticks = 0
        self.paused_time = 0
        self.is_paused = False

        self.music_playing = False
        self.paused = False
        self.slow_motion = False

        self.game_bg = pygame.image.load(IMG_GAME_BG)
        self.game_bg = pygame.transform.scale(self.game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_over_bg = pygame.image.load(IMG_GAME_OVER)
        self.game_over_bg = pygame.transform.scale(self.game_over_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level_complete_bg = pygame.image.load(IMG_LEVEL_COMPLETE)
        self.level_complete_bg = pygame.transform.scale(self.level_complete_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def start_music(self):
        if not self.music_playing:
            pygame.mixer.music.load(MUSIC_GAME)
            pygame.mixer.music.play(-1)
            self.music_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def spawn_coin(self):
        if len(self.coins) < 5:
            self.coins.append(Coin(
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(-400, -50)
            ))

    def spawn_bonus(self):
        if len(self.bonuses) < 3:
            self.bonuses.append(SlowBonus(
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(-400, -50)
            ))

    def check_collision(self):
        hero_rect = self.hero.get_rect()
        for obstacle in self.obstacles:
            offset_x = obstacle.rect.x - hero_rect.x
            offset_y = obstacle.rect.y - hero_rect.y
            if self.hero.mask.overlap(obstacle.mask, (offset_x, offset_y)) is not None:
                return "obstacle"

        for coin in self.coins[:]:
            if hero_rect.colliderect(coin.rect):
                self.coins.remove(coin)
                return "coin"

        for bonus in self.bonuses[:]:
            if hero_rect.colliderect(bonus.rect):
                self.bonuses.remove(bonus)
                return "bonus"

        return None

    def check_timer(self):
        current_time = pygame.time.get_ticks()
        if self.is_paused:
            elapsed = (self.start_ticks - self.paused_time) // 1000
        else:
            elapsed = (current_time - self.start_ticks - self.paused_time) // 1000

        if elapsed >= self.level_time and not self.game_over and not self.level_complete:
            self.level_complete = True
            self.show_buttons = True
            self.stop_music()
            return True
        return False

    def get_elapsed_time(self):
        current_time = pygame.time.get_ticks()
        if self.is_paused:
            return (self.start_ticks - self.paused_time) // 1000
        else:
            return (current_time - self.start_ticks - self.paused_time) // 1000

    def update(self):
        if self.paused:
            return

        if not self.game_over and not self.level_complete:
            self.start_music()
            self.hero.update()

            collision = self.check_collision()
            if collision == "obstacle":
                pygame.time.wait(1200)
                self.game_over = True
                self.show_buttons = True
                self.stop_music()

            if collision == "coin":
                self.score += 10

            if collision == "bonus":
                self.hero.bonus_active = True
                self.hero.bonus_timer = pygame.time.get_ticks()
                self.slow_motion = True
                self.score += 50

            self.check_timer()

            current_time = pygame.time.get_ticks()
            if not self.is_paused:
                if current_time - self.coin_spawn_timer > self.coin_spawn_interval:
                    self.spawn_coin()
                    self.coin_spawn_timer = current_time

                if current_time - self.bonus_spawn_timer > self.bonus_spawn_interval:
                    self.spawn_bonus()
                    self.bonus_spawn_timer = current_time

            for obstacle in self.obstacles:
                obstacle.move(self.slow_motion)

            if self.slow_motion and not self.hero.bonus_active:
                self.slow_motion = False

            for coin in self.coins[:]:
                if coin.update():
                    self.coins.remove(coin)

            for bonus in self.bonuses[:]:
                if bonus.update():
                    self.bonuses.remove(bonus)

    def draw(self, screen):
        if self.level_complete:
            screen.blit(self.level_complete_bg, (0, 0))
        elif self.game_over:
            screen.blit(self.game_over_bg, (0, 0))
        else:
            screen.blit(self.game_bg, (0, 0))

        if not self.game_over and not self.level_complete:
            self.hero.draw(screen)
            for obstacle in self.obstacles:
                obstacle.draw(screen)
            for coin in self.coins:
                coin.draw(screen)
            for bonus in self.bonuses:
                bonus.draw(screen)

            font = pygame.font.SysFont("Comic Sans MS", 36)
            time_left = max(0, self.level_time - self.get_elapsed_time())
            timer_text = font.render(f"Time: {time_left}s", True, (255, 255, 255))
            screen.blit(timer_text, (10, 10))

            level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
            screen.blit(level_text, (SCREEN_WIDTH - 130, 10))

            score_text = font.render(f"Score: {self.score}", True, (255, 255, 0))
            screen.blit(score_text, (SCREEN_WIDTH - 250, 50))

            if self.hero.bonus_active:
                bonus_text = font.render("SLOW MOTION ACTIVE!", True, (0, 150, 255))
                screen.blit(bonus_text, (SCREEN_WIDTH - 350, 90))
                bonus_time_left = max(0, 5 - (pygame.time.get_ticks() - self.hero.bonus_timer) // 1000)
                bonus_indicator = font.render(f"Bonus: {bonus_time_left}s", True, (0, 150, 255))
                screen.blit(bonus_indicator, (10, 60))

            if self.paused:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 128))
                screen.blit(s, (0, 0))
                font_big = pygame.font.Font(None, 100)
                paused_text = font_big.render("PAUSED", True, (255, 255, 255))
                text_rect = paused_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                screen.blit(paused_text, text_rect)
                font_small = pygame.font.Font(None, 40)
                hint_text = font_small.render("Press SPACE to continue", True, (200, 200, 200))
                hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60))
                screen.blit(hint_text, hint_rect)

        if self.game_over:
            score_font = pygame.font.Font(None, 40)
            final_score = score_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            score_rect = final_score.get_rect(center=(SCREEN_WIDTH/2, 220))
            screen.blit(final_score, score_rect)

            mouse_pos = pygame.mouse.get_pos()
            self.button_restart.check_hover(mouse_pos)
            self.button_restart.draw(screen)
            self.button_menu.check_hover(mouse_pos)
            self.button_menu.draw(screen)
            self.button_exit.check_hover(mouse_pos)
            self.button_exit.draw(screen)

        if self.level_complete:
            font = pygame.font.Font(None, 50)
            if self.level == 3:
                complete_text = font.render("YOU WIN!", True, (255, 215, 0))
            else:
                complete_text = font.render("LEVEL COMPLETE!", True, (255, 255, 0))
            text_rect = complete_text.get_rect(center=(SCREEN_WIDTH/2, 100))
            screen.blit(complete_text, text_rect)

            score_font = pygame.font.Font(None, 40)
            level_score = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
            score_rect = level_score.get_rect(center=(SCREEN_WIDTH/2, 160))
            screen.blit(level_score, score_rect)

            mouse_pos = pygame.mouse.get_pos()
            if self.level < 3:
                self.button_next.check_hover(mouse_pos)
                self.button_next.draw(screen)
            self.button_exit.check_hover(mouse_pos)
            self.button_exit.draw(screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_music()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over and not self.level_complete:
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                            self.pause_start_ticks = pygame.time.get_ticks()
                            self.is_paused = True
                        else:
                            pygame.mixer.music.unpause()
                            self.paused_time += pygame.time.get_ticks() - self.pause_start_ticks
                            self.is_paused = False

            if self.game_over and self.show_buttons:
                if self.button_restart.handle_event(event):
                    self.stop_music()
                    return "restart"
                if self.button_menu.handle_event(event):
                    self.stop_music()
                    return "menu"
                if self.button_exit.handle_event(event):
                    self.stop_music()
                    return False

            if self.level_complete and self.show_buttons:
                if self.level < 3:
                    if self.button_next.handle_event(event):
                        self.stop_music()
                        return "next_level"
                if self.button_exit.handle_event(event):
                    self.stop_music()
                    return False
        return True

    def run(self, screen):
        running = True
        while running:
            result = self.handle_events()
            if result == "next_level":
                return "next_level"
            if result == "restart":
                return "restart"
            if result == "menu":
                return "menu"
            if result == False:
                return False

            self.update()
            self.draw(screen)
            pygame.display.flip()
            self.clock.tick(150)
        return True
