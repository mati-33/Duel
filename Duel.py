import random
import time


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
        if self.critical_strike_chance > random.randint(0, 101):
            return True
        else:
            return False

    # this method determines if a character will dodge an opponent's strike
    def dodge(self):
        if self.dodge_chance > random.randint(0, 101):
            return True
        else:
            return False

    # this method will restore character health, so he can fight again
    def restore_health(self, health):
        self.health = health


def play_again():
    # this function ask user if he wants to play again
    choice = input("\nPlay again? (yes/no): ").upper()
    if choice == 'YES':
        return True
    else:
        return False


def fight(char_1, char_2):
    # these variables will be used later to restore characters health
    health_to_restore_1 = char_1.health
    health_to_restore_2 = char_2.health

    # fight will end when one of the characters health will be equal or less than 0
    while char_1.health >= 0 and char_2.health >= 0:

        # storing each character strike damage in a variables
        damage_1 = char_1.strike()
        damage_2 = char_2.strike()

        # these empty strings will be later used to display critical strike message
        critical_strike_msg_1 = ""
        critical_strike_msg_2 = ""

        # if the dodge() method returns True, character dodges a strike
        # so the opponent damage is equal to zero
        if char_1.dodge():
            damage_2 = 0
        if char_2.dodge():
            damage_1 = 0

        # if the critical_strike() method returns True, character strike damage is doubled
        # then, message about critical strike is added to an empty string
        if char_1.critical_strike():
            damage_1 = 2 * damage_1
            critical_strike_msg_1 = 'CRITICAL STRIKE!'
        if char_2.critical_strike():
            damage_2 = 2 * damage_2
            critical_strike_msg_2 = 'CRITICAL STRIKE'

        # subtracting opponent damage from character's health
        char_1.health -= damage_2
        char_2.health -= damage_1

        # letting user know how the fight is going
        # following block takes in consideration every possible output
        if damage_1 == 0 and damage_2 == 0:
            print("")
            print(f"{char_1.name} missed!")
            print(f"{char_2.name} missed!")

        elif damage_1 == 0 and damage_2 != 0:
            print("")
            print(f"{char_1.name} missed!")
            print(f"{char_2.name} hits for {damage_2}! {critical_strike_msg_2}")

        elif damage_1 != 0 and damage_2 == 0:
            print("")
            print(f"{char_1.name} hits for {damage_1}! {critical_strike_msg_1}")
            print(f"{char_2.name} missed!")

        elif damage_1 != 0 and damage_2 != 0:
            print("")
            print(f"{char_1.name} hits for {damage_1}! {critical_strike_msg_1}")
            print(f"{char_2.name} hits for {damage_2}! {critical_strike_msg_2}")
        time.sleep(0.7)

    # displaying result of the fight
    if char_1.health <= 0 and char_2.health <= 0:
        print('\nDraw!')
    elif char_1.health > 0 >= char_2.health:
        print(f"\n{char_1.name} wins the fight!")
    elif char_2.health > 0 >= char_1.health:
        print(f"\n{char_2.name} wins the fight!")

    # restoring characters health after the fight
    # with the initial value of their health points
    char_1.restore_health(health_to_restore_1)
    char_2.restore_health(health_to_restore_2)


# creation of characters for testing purposes
test_character_1 = Character('josh', 200, [20, 25], 30, 30)
test_character_2 = Character('mosh', 100, [15, 20], 50, 50)


def main():

    # main game algorithm - needs to be developed
    fight(test_character_1, test_character_2)
    while play_again():
        fight(test_character_1, test_character_2)


if __name__ == '__main__':
    main()
