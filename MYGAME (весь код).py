import pygame
import random
pygame.init()

# НАСТРОЙКИ ЭКРАНА
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# ИНИЦИАЛИЗАЦИЯ ЗВУКА
pygame.mixer.init()

# ЗАГРУЗКА МУЗЫКИ 
music_file_game = "c:/Users/Admin/Desktop/MYGAME/music/aid170amin (mp3cut.net).mp3" 
music_file_menu = "c:/Users/Admin/Desktop/MYGAME/music/unfair prod (mp3cut.net).mp3"  
pygame.mixer.music.load(music_file_game) 
pygame.mixer.music.set_volume(0.3) 
menu_music = pygame.mixer.Sound(music_file_menu)
menu_music.set_volume(0.5)

# ЗАГРУЗКА ФОНОВЫХ ИЗОБРАЖЕНИЙ
game_picture = pygame.image.load("c:/Users/Admin/Desktop/MYGAME/phone/game.jpg") 
game_picture = pygame.transform.scale(game_picture, (SCREEN_WIDTH, SCREEN_HEIGHT))

menu_picture = pygame.image.load("c:/Users/Admin/Desktop/MYGAME/phone/i.jpg") 
menu_picture = pygame.transform.scale(menu_picture, (SCREEN_WIDTH, SCREEN_HEIGHT))

game_over_screen = pygame.image.load("c:/Users/Admin/Desktop/MYGAME/phone/game-over-red-text-in-pixel-art-style-vector.jpg") 
game_over_screen = pygame.transform.scale(game_over_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

level_complete_screen = pygame.image.load("c:/Users/Admin/Desktop/MYGAME/phone/game-over-red-text-in-pixel-art-style-vector.jpg")
level_complete_screen = pygame.transform.scale(level_complete_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

# КЛАСС ГЕРОЯ
class Hero:
    def __init__(self):
        # Основные параметры героя
        self.width = 120
        self.height = 150
        self.x = SCREEN_WIDTH // 2 - self.width // 2 
        self.y = SCREEN_HEIGHT - 120 
        self.speed = 5 

        self.image = pygame.image.load('c:/Users/Admin/Desktop/MYGAME/sprite/bird_result_a82e91ef661a11f18939b2cfdd2a167c (1).png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        #маска для определения столкновений
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Параметры бонуса замедления
        self.bonus_active = False 
        self.bonus_timer = 0 

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed 
        if keys[pygame.K_d]:
            self.x += self.speed

        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        
        self.rect.x = self.x

        if self.bonus_active:
            if pygame.time.get_ticks() - self.bonus_timer > 5000:
                self.bonus_active = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# КЛАСС ПРЕПЯТСТВИЙ (спрайт)
class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# КЛАСС ПРЕПЯТСТВИЙ (основной)
class Obstacle(ObstacleSprite):
    def __init__(self, x, y, width, height, speed, filename):
        super().__init__(x, y, filename) 
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.transform.scale(self.image, (width, height)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.original_speed = speed 

    def move(self, slow_motion=False):
        # Движение препятствия вниз
        if slow_motion:
            self.rect.y += self.speed * 0.5
        else:
            self.rect.y += self.speed

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-200, -50)
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.width)

    def draw(self):
        screen.blit(self.image, self.rect)

# КЛАССЫ ПРЕПЯТСТВИЙ
class Stone(Obstacle):
    def __init__(self, x, y, speed):
        # Камень
        super().__init__(x, y, 60, 65, speed, "c:/Users/Admin/Desktop/MYGAME/sprite/b7ea4111c4b19f8.png")

class Fire(Obstacle):
    def __init__(self, x, y, speed):
        # Огонь/бомба
        super().__init__(x, y, 100, 100, speed, "c:/Users/Admin/Desktop/MYGAME/sprite/retro-pixel-art-bomb-icon-explosive-graphic-symbol-in-8-bit-style-vector (1).png")

class Sword(Obstacle):
    def __init__(self, x, y, speed):
        # Меч
        super().__init__(x, y, 40, 110, speed, "c:/Users/Admin/Desktop/MYGAME/sprite/sword-pixel-art-style-free-vector.png")

# КЛАСС МОНЕТКИ
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 3  

    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > SCREEN_HEIGHT:
            return True  
        return False

    def draw(self):
        # Отрисовка монетки
        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2)
        pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), 15)  
        pygame.draw.circle(screen, (255, 165, 0), (center_x, center_y), 12, 2)  
        font = pygame.font.Font(None, 20)
        text = font.render("$", True, (255, 255, 255))  
        screen.blit(text, (center_x - 5, center_y - 8))

# КЛАСС БОНУСА ЗАМЕДЛЕНИЯ
class SlowBonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.animation_frame = 0 

    def update(self):
        self.y += 2
        self.rect.y = self.y
        self.animation_frame += 0.1
        if self.y > SCREEN_HEIGHT:
            return True 
        return False

    def draw(self):
        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2)
    
        pygame.draw.circle(screen, (0, 150, 255), (center_x, center_y), 20)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 18, 2)
    
        font = pygame.font.Font(None, 25)
        text = font.render("B", True, (255, 255, 255))
        screen.blit(text, (center_x - 8, center_y - 12))

# КЛАСС КНОПКИ С ИЗОБРАЖЕНИЕМ
class ImageButton:
    def __init__(self, x, y, width, height, text, im_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(im_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hovered = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# КЛАСС ИГРЫ
class Game:
    def __init__(self, level):
        self.level = level 
        self.hero = Hero()  
        self.score = 0  

        # Настройки уровня
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

        # Создание препятствий для уровня
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

        # Списки монеток и бонусов
        self.coins = []
        self.coin_spawn_timer = 0
        self.coin_spawn_interval = 1500

        self.bonuses = []
        self.bonus_spawn_timer = 0
        self.bonus_spawn_interval = 20000

        # Создание кнопок
        self.button_next = ImageButton(SCREEN_WIDTH/2-(252/2), 350, 252, 74, "NEXT LEVEL", "c:/Users/Admin/Desktop/MYGAME/phone/0d90a821a9a95f8f353f33febec9e0f1.jpg")
        self.button_exit = ImageButton(SCREEN_WIDTH/2-(252/2), 600, 252, 74, "EXIT", "c:/Users/Admin/Desktop/MYGAME/phone/0d90a821a9a95f8f353f33febec9e0f1.jpg")
        self.button_restart = ImageButton(SCREEN_WIDTH/2-(252/2), 700, 252, 74, "START OVER", "c:/Users/Admin/Desktop/MYGAME/phone/0d90a821a9a95f8f353f33febec9e0f1.jpg")
        self.button_menu = ImageButton(SCREEN_WIDTH/2-(252/2), 500, 252, 74, "MENU", "c:/Users/Admin/Desktop/MYGAME/phone/0d90a821a9a95f8f353f33febec9e0f1.jpg")

        # Таймеры и состояния игры
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

    def start_music(self):
        # Запуск игровой музыки
        if not self.music_playing:
            pygame.mixer.music.load(music_file_game)
            pygame.mixer.music.play(-1)
            self.music_playing = True

    def stop_music(self):
        # Остановка музыки
        pygame.mixer.music.stop()
        self.music_playing = False


    def spawn_coin(self):
        # Создание новой монетки
        if len(self.coins) < 5: 
            self.coins.append(Coin(
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(-400, -50)
            ))

    def spawn_bonus(self):
        # Создание нового бонуса
        if len(self.bonuses) < 3:
            self.bonuses.append(SlowBonus(
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(-400, -50)
            ))

    def check_collision(self):
        # Проверка всех столкновений героя
        hero_rect = self.hero.get_rect()
        for obstacle in self.obstacles:
            offset_x = obstacle.rect.x - hero_rect.x
            offset_y = obstacle.rect.y - hero_rect.y
            if self.hero.mask.overlap(obstacle.mask, (offset_x, offset_y)) is not None:
                return "obstacle" 

        # Проверка сбора монеток
        for coin in self.coins[:]:
            if hero_rect.colliderect(coin.rect):
                self.coins.remove(coin)
                return "coin" 

        # Проверка сбора бонуса
        for bonus in self.bonuses[:]:
            if hero_rect.colliderect(bonus.rect):
                self.bonuses.remove(bonus)
                return "bonus"

        return None

    def check_timer(self):
        # Проверка времени уровня
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
        # Получение прошедшего времени с учетом паузы
        current_time = pygame.time.get_ticks()
        if self.is_paused:
            return (self.start_ticks - self.paused_time) // 1000
        else:
            return (current_time - self.start_ticks - self.paused_time) // 1000


    def update(self):
        #обновления игрового состояния
        if self.paused:
            return 

        if not self.game_over and not self.level_complete:
            # Запуск музыки
            self.start_music()

            # Обновление героя
            self.hero.update()

            # Проверка столкновений
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

            # Проверка таймера уровня
            self.check_timer()

            # Спавн монеток и бонусов
            current_time = pygame.time.get_ticks()
            if not self.is_paused:
                if current_time - self.coin_spawn_timer > self.coin_spawn_interval:
                    self.spawn_coin()
                    self.coin_spawn_timer = current_time

                if current_time - self.bonus_spawn_timer > self.bonus_spawn_interval:
                    self.spawn_bonus()
                    self.bonus_spawn_timer = current_time

            # Движение препятствий
            for obstacle in self.obstacles:
                obstacle.move(self.slow_motion)

            # Отключение замедления
            if self.slow_motion and not self.hero.bonus_active:
                self.slow_motion = False

            # Обновление монето
            for coin in self.coins[:]:
                if coin.update():
                    self.coins.remove(coin)

            # Обновление бонусов
            for bonus in self.bonuses[:]:
                if bonus.update():
                    self.bonuses.remove(bonus)

    def draw(self):
        # Отрисовка всех элементов игры
        if self.level_complete:
            screen.blit(menu_picture, (0, 0))
        elif self.game_over:
            screen.blit(game_over_screen, (0, 0))
        else:
            screen.blit(game_picture, (0, 0))

        if not self.game_over and not self.level_complete:
            # Отрисовка игровых объектов
            self.hero.draw()
            for obstacle in self.obstacles:
                obstacle.draw()
            for coin in self.coins:
                coin.draw()
            for bonus in self.bonuses:
                bonus.draw()

            # Отрисовка интерфейса (таймер уровень счет)
            font = pygame.font.SysFont("Comic Sans MS", 36)
            time_left = max(0, self.level_time - self.get_elapsed_time())
            timer_text = font.render(f"Time: {time_left}s", True, (255, 255, 255))
            screen.blit(timer_text, (10, 10))

            level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
            screen.blit(level_text, (SCREEN_WIDTH - 130, 10))

            score_text = font.render(f"Score: {self.score}", True, (255, 255, 0))
            screen.blit(score_text, (SCREEN_WIDTH - 250, 50))

            # Индикатор активного бонуса
            if self.hero.bonus_active:
                bonus_text = font.render("SLOW MOTION ACTIVE!", True, (0, 150, 255))
                screen.blit(bonus_text, (SCREEN_WIDTH - 350, 90))
                bonus_time_left = max(0, 5 - (pygame.time.get_ticks() - self.hero.bonus_timer) // 1000)
                bonus_indicator = font.render(f"Bonus: {bonus_time_left}s", True, (0, 150, 255))
                screen.blit(bonus_indicator, (10, 60))

            # Отрисовка паузы
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

        # Отрисовка экрана Game Over
        if self.game_over:
            score_font = pygame.font.Font(None, 40)
            final_score = score_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            score_rect = final_score.get_rect(center=(SCREEN_WIDTH/2, 220))
            screen.blit(final_score, score_rect)

            # Кнопки на экране Game Over
            mouse_pos = pygame.mouse.get_pos()
            self.button_restart.check_hover(mouse_pos)
            self.button_restart.draw(screen)
            self.button_menu.check_hover(mouse_pos)
            self.button_menu.draw(screen)
            self.button_exit.check_hover(mouse_pos)
            self.button_exit.draw(screen)

        # Отрисовка экрана завершения уровня
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

            # Кнопки на экране завершения уровня
            mouse_pos = pygame.mouse.get_pos()
            if self.level < 3:
                self.button_next.check_hover(mouse_pos)
                self.button_next.draw(screen)
            self.button_exit.check_hover(mouse_pos)
            self.button_exit.draw(screen)

    def handle_events(self):
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_music()
                return False  

            # Обработка паузы по пробелу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over and not self.level_complete:
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()  # Пауза музыки
                            self.pause_start_ticks = pygame.time.get_ticks()
                            self.is_paused = True
                        else:
                            pygame.mixer.music.unpause()
                            self.paused_time += pygame.time.get_ticks() - self.pause_start_ticks
                            self.is_paused = False

            # Обработка кнопок на экране Game Over
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

            # Обработка кнопок на экране завершения уровня
            if self.level_complete and self.show_buttons:
                if self.level < 3:
                    if self.button_next.handle_event(event):
                        self.stop_music()
                        return "next_level"
                if self.button_exit.handle_event(event):
                    self.stop_music()
                    return False 
        return True

    def run(self):
        # Основной игровой цикл
        running = True
        while running:
            result = self.handle_events()
            # Обработка результатов событий
            if result == "next_level":
                return "next_level"
            if result == "restart":
                return "restart"
            if result == "menu":
                return "menu"
            if result == False:
                return False

            self.update()
            self.draw() 
            pygame.display.flip() 
            self.clock.tick(150)  
        return True

# КЛАСС МЕНЮ
class Menu:
    def __init__(self):
        # Создание кнопок меню
        self.button_play = ImageButton(SCREEN_WIDTH/2-(252/2), 100, 252, 74, "PLAY", "c:/Users/Admin/Desktop/MYGAME/phone/0d90a821a9a95f8f353f33febec9e0f1.jpg")
        self.button_exit = ImageButton(SCREEN_WIDTH/2-(252/2), 300, 252, 74, "EXIT", "c:/Users/Admin/Desktop/MYGAME/phone/0d90a821a9a95f8f353f33febec9e0f1.jpg")
        self.music_playing = False

    def start_music(self):
        # Запуск музыки меню
        if not self.music_playing:
            pygame.mixer.music.load(music_file_menu)
            pygame.mixer.music.play(-1)
            self.music_playing = True

    def stop_music(self):
        # Остановка музыки меню
        pygame.mixer.music.stop()
        self.music_playing = False

    def run(self):
        # Основной цикл меню
        self.start_music()

        while True:
            screen.blit(menu_picture, (0, 0)) 

            # Заголовок игры
            font = pygame.font.Font(None, 80)
            title = font.render("PIXEL ADVENTURE", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 50))
            screen.blit(title, title_rect)

            # Обработка кнопок
            mouse_pos = pygame.mouse.get_pos()
            self.button_play.check_hover(mouse_pos)
            self.button_play.draw(screen)
            self.button_exit.check_hover(mouse_pos)
            self.button_exit.draw(screen)

            # Обработка событий в меню
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

# ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА
if __name__ == "__main__":

    menu = Menu()
    menu.run()

    # Цикл уровней
    level = 1
    while True:
        game = Game(level)
        result = game.run() 

        # Обработка результатов игры
        if result == "next_level":
            level += 1
            if level > 3:
                level = 3 
        elif result == "restart":
            continue 
        elif result == "menu":
            menu = Menu() 
            menu.run()
            level = 1
            continue
        else:
            break