import random


class Character:

    # this method creates character attributes
    def __init__(self, name, health, damage, critical_strike_chance, dodge_chance):
        self.name = name
        self.health = health
        self.damage = list(damage)
        self.critical_strike_chance = critical_strike_chance
        self.dodge_chance = dodge_chance

    # this method determines how much damage the strike will deal
    def strike(self):
        return random.randrange(self.damage[0], self.damage[1])

    # this method determines if a strike will be a critical strike
    def critical_strike(self):
        if self.critical_strike_chance < random.randint(0, 101):
            return True
        else:
            return False

    # this method determines if a character will dodge an opponent's strike
    def dodge(self):
        if self.dodge_chance < random.randint(0, 101):
            return True
        else:
            return False

