import os
import pygame
import random

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)

image_cache = {}

class FighterAnimation:
    def __init__(self, screen, name, x, y, flip=False):
        self.screen = screen
        self.flip = flip
        self.name = name
        self.frame_index = 0
        self.set_cache()
        self.action = "Idle"
        self.update_time = pygame.time.get_ticks()
        self.image = self.get_next_frame()
        self.rect = self.image.get_rect(center=(x, y))

    def set_cache(self):
        actions = ["Idle", "Attack", "Hurt", "Death"]
        for action in actions:
            dict_key = f"{self.name}_{action}"
            if dict_key not in image_cache:
                path = f'img/{self.name}/{action}'
                img_list = []
                for file_name in sorted(os.listdir(path)):
                    image = pygame.image.load(f"{path}/{file_name}").convert_alpha()
                    size = (image.get_width() * 3, image.get_height() * 3)
                    img =  pygame.transform.scale(image, size)
                    if self.flip:
                        img = pygame.transform.flip(img, True, False)
                    img_list.append(img)
                image_cache.update({dict_key: img_list})

    def get_key_from_cache(self, key):
        return image_cache.get(key)

    def get_next_frame(self):
        key = f'{self.name}_{self.action}'
        frames = self.get_key_from_cache(key)
        if self.frame_index < len(frames):
            frame = frames[self.frame_index]
            self.frame_index += 1
            return frame
        elif self.action == "Death":
            return frames[-1]
        else:
            self.idle()
            return frames[self.frame_index]

    def animate(self):
        animation_cooldown = 100  # Tempo entre cada frame (em milissegundos)
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.image = self.get_next_frame()
        self.screen.blit(self.image, self.rect)

    def idle(self):
        # set variables to idle animation
        self.action = "Idle"
        self.reset_animation()

    def hurt(self):
        # set variables to hurt animation
        self.action = "Hurt"
        self.reset_animation()

    def death(self):
        # set variables to death animation
        self.action = "Death"
        self.reset_animation()

    def attack(self):
        self.action = "Attack"
        self.reset_animation()

    def reset_animation(self):
        self.frame_index = 0


# fighter class
class Fighter(FighterAnimation):
    def __init__(self, x, y, name, max_hp, strength, potions, screen, flip=False):
        self.screen = screen
        super().__init__(screen, name, x, y, flip)
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        super().attack()
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # run enemy hurt animation
        target.hurt()
        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), RED)
        damage_text_group.add(damage_text)
        # set variables to attack animation

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def create_health_bar(self, x, y):
        self.health_bar = HealthBar(x, y, self.hp, self.max_hp, self.screen)
        
    def draw_health_bar(self):
        self.health_bar.draw(self.hp)
        

    def use_potion(self) -> None:
        percent_heal = 0.35
        total_heal = int(percent_heal * self.max_hp)
        if self.alive and self.potions > 0:
            if self.max_hp - self.hp > total_heal:
                heal_amount = total_heal
            else:
                heal_amount = self.max_hp - self.hp
            self.hp += heal_amount
            self.potions -= 1
            damage_text = DamageText(self.rect.centerx, self.rect.y, str(heal_amount), GREEN)
            damage_text_group.add(damage_text)


class HealthBar:
    def __init__(self, x, y, hp, max_hp, screen):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.screen = screen

    def draw(self, hp):
        # update with new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(self.screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(self.screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        font = pygame.font.SysFont('Times New Roman', 26)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()
