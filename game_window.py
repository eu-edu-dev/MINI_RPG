import pygame
import button
from characters import *

RUNNING = 0
DEFEATED = -1
VICTORY = 1

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class MainGameGraphic:
    def __init__(self):
        pygame.init()
        pygame.font.init()  # Initialize fonts
        self.create_window()
        self.load_images()
        self.create_characters()
        self.attack = False
        self.target = None
        self.clicked = False
        self.game_status = RUNNING
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.ai_index = 10000
        self.update_time = pygame.time.get_ticks()

    def create_window(self):
        self.bottom_panel = 150
        self.screen_width = 800
        self.screen_height = 400 + self.bottom_panel
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Battle')

    def load_images(self):
        self.background_img = pygame.image.load('img/Background/background.png').convert_alpha()
        self.panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
        self.potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
        self.restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
        self.victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
        self.defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
        self.sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()

        self.font = pygame.font.SysFont('Times New Roman', 26)

    def create_characters(self):
        position_y = self.screen_height - self.bottom_panel + 40
        self.knight = Fighter(200, 260, 'Knight', 40, 10, 3, self.screen)
        self.knight.create_health_bar(100, position_y)
        self.opponents_list = [
            Fighter(550, 250, 'Martial Hero 2', 20, 6, 1, self.screen, True),
            # Fighter(600, 270, 'Bandit', 20, 6, 1, self.screen),
            Fighter(700, 270, 'Bandit', 20, 6, 1, self.screen)
        ]
        self.characters_list = self.opponents_list + [self.knight]
        for index, opponent in enumerate(self.opponents_list):
            opponent.create_health_bar(550, position_y + (60 * index))

    def draw_healthbar(self):
        for characther in self.characters_list:
            characther.draw_health_bar()

    def handle_ui(self):
        self.draw_bg()
        self.draw_panel()
        self.create_buttons()
        self.check_potions()
        self.load_characters()
        self.draw_healthbar()
        self.set_cursor()
        self.draw_damage_text()

    def draw_bg(self):
        self.screen.blit(self.background_img, (0, 0))

    def draw_panel(self):
        self.screen.blit(self.panel_img, (0, self.screen_height - self.bottom_panel))
        self.draw_text(f'{self.knight.name} HP: {self.knight.hp}', self.font, RED, 100,
                       self.screen_height - self.bottom_panel + 10)
        for count, i in enumerate(self.opponents_list):
            self.draw_text(f'{i.name} HP: {i.hp}', self.font, RED, 550,
                           (self.screen_height - self.bottom_panel + 10 + count * 60))

    def draw_text(self, text, text_font, text_col, x, y):
        img = text_font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def create_buttons(self):
        self.restart_button = button.Button(self.screen, 350, 120, self.restart_img, 120, 30)
        self.potion_button = button.Button(self.screen, 100, self.screen_height - self.bottom_panel + 70, self.potion_img,
                                           64, 64)

    def draw_damage_text(self):
        damage_text_group.update()
        damage_text_group.draw(self.screen)

    def check_potions(self):
        potion = False
        if self.potion_button.draw():
            potion = True
        self.draw_text(
            str(self.knight.potions), self.font, RED, 150, self.screen_height - self.bottom_panel + 70)
        return potion

    def set_cursor(self):
        collide_opponent = self.get_collide_opponent()
        if collide_opponent:
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)
            self.screen.blit(self.sword_img, pygame.mouse.get_pos())
            if self.clicked and collide_opponent and collide_opponent.alive:
                self.attack = True
                self.target = collide_opponent
        else:
            pygame.mouse.set_visible(True)

    def get_collide_opponent(self):
        for opponent in self.opponents_list:
            if opponent.rect.collidepoint(pygame.mouse.get_pos()) and opponent.alive:
                return opponent

    def load_characters(self):
        for character in self.characters_list:
            character.animate()


class Game(MainGameGraphic):

    def run_game(self):
        while game.running:
            game.run()
        pygame.quit()

    def run(self):
        self.clock.tick(self.fps)
        self.handle_ui()
        self.check_game_status()
        self.set_default()
        self.update_actions()
        if self.clicked:
            self.combat()
        self.ai_turn()
        self.check_game_status()
        pygame.display.update()

    def set_default(self):
        self.attack = False
        self.target = None
        self.clicked = False

    def update_actions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True
                self.attack = True
                self.target = self.get_collide_opponent()

    def check_game_status(self):
        if self.game_status != RUNNING:
            if self.game_status == VICTORY:
                self.screen.blit(self.victory_img, (275, 50))
            if self.game_status == DEFEATED:
                self.screen.blit(self.defeat_img, (290, 50))
            if self.restart_button.draw():
                self.reset_characters()
                self.game_status = RUNNING

    def combat(self):
        if self.knight.alive and self.ai_index > len(self.opponents_list):
            if self.attack and self.target:
                self.knight.attack(self.target)
            elif self.knight.potions > 0 and self.check_potions() and (self.knight.max_hp - self.knight.hp) > 0:
                self.knight.use_potion()
            else:
                return
            self.ai_index = 0
            self.set_default()

    def npc_ai(self, opponent):
        if (opponent.hp / opponent.max_hp) < 0.5 and opponent.potions > 0:
            opponent.use_potion()
        else:
            opponent.attack(self.knight)
        if self.knight.hp <= 0:
            self.game_status = DEFEATED

    def ai_turn(self):
        if any(opponent.alive for opponent in self.opponents_list):
            animation_cooldown = 1000
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                if self.ai_index < len(self.opponents_list):
                    opponent = self.opponents_list[self.ai_index]
                    if opponent.alive:
                        self.npc_ai(opponent)
                self.update_time = pygame.time.get_ticks()
                self.ai_index += 1
        else:
            self.game_status = VICTORY

    def reset_characters(self):
        for character in self.characters_list:
            character.reset()
        self.set_default()
        self.ai_index = 99999


game = Game()

game.run_game()
