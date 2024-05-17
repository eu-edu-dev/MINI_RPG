from characters import Fighter


class LevelMixin:
    def __init__(self, screen):
        self.level = 1
        self.screen = screen
        self.knight = self.get_knight()
        self.level_points = 0

    def get_knight(self) -> Fighter:
        return Fighter(
            200, 260, 'Knight',
            40, 10, 3,
            self.screen, width=300, heigth=300
        )

    def skeleton(self, position=1) -> Fighter:
        return Fighter(
            375+125*position, 284, 'Skeleton',
            (18 + 2 * self.level), (3 + 3 * self.level), 1,
            self.screen, True, width=120, height=120
        )

    def bandit(self, position=0) -> Fighter:
        return Fighter(
            375+125*position, 270, 'Bandit',
            (25 + 3 * self.level), (2 + 2 * self.level), 1, self.screen
        )

    def martial_hero(self, position=0) -> Fighter:
        return Fighter(
            375+125*position, 270, 'Martial Hero',
            (30 + 2 * self.level), (4 + 2 * self.level), 1,
            self.screen, True, width=140, height=140
        )

    def power_up_hp(self):
        self.knight.max_hp += 5
        self.knight.hp = self.knight.max_hp
        self.level_points -= 1

    def power_up_strength(self):
        self.knight.strength += 2
        self.level_points -= 1
