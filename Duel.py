import random
import time
import os


class Character:
    # this class is modeling characters that will fight each other

    # this method creates character attributes
    def __init__(self, health, damage, critical_strike_chance, dodge_chance, name):
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


def clear_console():
    # this function clears console
    os.system('cls')


def greeting_message():
    # this function displays greeting message to the user
    banner = """
████████▄  ███    █▄     ▄████████  ▄█        v.1.0
███   ▀███ ███    ███   ███    ███ ███       
███    ███ ███    ███   ███    █▀  ███       
███    ███ ███    ███  ▄███▄▄▄     ███       
███    ███ ███    ███ ▀▀███▀▀▀     ███       
███    ███ ███    ███   ███    █▄  ███       
███   ▄███ ███    ███   ███    ███ ███▌    ▄ 
████████▀  ████████▀    ██████████ █████▄▄██  by Mateusz Meksuła
    """
    print(banner)
    print("Who is the best fighter? Let's find out\n")


def referee(char_1, char_2):
    # this function simulates referee that
    # asks fighters if they are ready to fight

    print("")
    print(f'Referee: \t{char_1.name.title()}, are you ready?')
    time.sleep(1)
    print(f'{char_1.name.title()}: Yes!')
    time.sleep(1)
    print(f'Referee: \t{char_2.name.title()}, are you ready?')
    time.sleep(1)
    print(f'{char_2.name.title()}: Yes!')
    time.sleep(1)
    print(f'Referee: \tFight!')
    time.sleep(2)


def make_choice(char_list):
    # this function allows user to choose character from a list

    # variable 'index' allows to display list indexes
    index = 1
    for char in char_list:
        print(f"{index}: {char.name.title()}")
        index += 1

    # returning characters list index of a list of characters
    # other functions will require characters list index as an input

    # creation of empty string 'choice', so while loop can initialize
    choice = ""

    # user have to type number that corresponds to a character
    # otherwise while loop won't break
    while choice not in range(1, len(char_list) + 1):

        # this try-except block is in case user will not input number
        try:
            choice = int(input("\nType corresponding number: "))
            if choice not in range(1, len(char_list) + 1):
                print('Please, typy only the corresponding number')
        except ValueError:
            print('Please, type only the corresponding number')

    list_index = choice - 1
    return list_index


def show_char_stats(char_list):
    # this function allows user to see character attributes

    while True:

        # asking user to make a choice, which characters stats he wants to display
        print("\nWhich one?: \n")
        chosen_char = char_list[make_choice(char_list)]

        # printing chosen character's attributes
        print("")
        print(f"Name: \t\t\t{chosen_char.name.title()}")
        print(f"Health: \t\t{chosen_char.health}")
        print(f"Damage: \t\t{chosen_char.damage[0]}-{chosen_char.damage[1]}")
        print(f"Critical strike chance: {chosen_char.critical_strike_chance}%")
        print(f"Chance to dodge strike: {chosen_char.dodge_chance}%")

        # asking user if he wants to see another character attributes
        choice = input("\nAnother one? (yes/no): ").upper()
        if choice != 'YES':
            break


def match_making(char_list):
    # this function allows user to choose two characters to fight each other

    # creation of an empty list to later append two characters
    fighting_characters = []

    # removing first chosen character to make sure
    # user can't choose same character again
    print("\nChoose first fighter: \n")
    first_char = char_list.pop(make_choice(char_list))
    fighting_characters.append(first_char)

    # same as above, appending user choice to list
    print("\nChoose second fighter: \n")
    second_char = char_list[make_choice(char_list)]
    fighting_characters.append(second_char)

    # returning list of two characters that will fight each other
    return fighting_characters


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
            print(f"{char_1.name.title()} missed!")
            print(f"{char_2.name.title()} missed!")

        elif damage_1 == 0 and damage_2 != 0:
            print("")
            print(f"{char_1.name.title()} missed!")
            print(f"{char_2.name.title()} hits for {damage_2}! {critical_strike_msg_2}")

        elif damage_1 != 0 and damage_2 == 0:
            print("")
            print(f"{char_1.name.title()} hits for {damage_1}! {critical_strike_msg_1}")
            print(f"{char_2.name.title()} missed!")

        elif damage_1 != 0 and damage_2 != 0:
            print("")
            print(f"{char_1.name.title()} hits for {damage_1}! {critical_strike_msg_1}")
            print(f"{char_2.name.title()} hits for {damage_2}! {critical_strike_msg_2}")
        time.sleep(0.7)

    # displaying result of the fight
    if char_1.health <= 0 and char_2.health <= 0:
        print('\nDraw!')
    elif char_1.health > 0 >= char_2.health:
        print(f"\n{char_1.name.title()} wins the fight!")
    elif char_2.health > 0 >= char_1.health:
        print(f"\n{char_2.name.title()} wins the fight!")

    # restoring characters health after the fight
    # with the initial value of their health points
    char_1.restore_health(health_to_restore_1)
    char_2.restore_health(health_to_restore_2)

    # this line stops the function from closing
    input("\nPress any key to continue: ")


def main():
    # creation of characters
    character_1 = Character(150, [15, 20], 40, 30, 'charles')
    character_2 = Character(175, [20, 25], 30, 50, 'dustin')
    character_3 = Character(200, [17, 22], 25, 55, 'islam')
    character_4 = Character(125, [12, 17], 20, 30, 'beneil')
    character_5 = Character(150, [14, 19], 30, 30, 'gamrot')
    character_6 = Character(175, [18, 23], 50, 20, 'tony')

    # creation of list of characters
    characters_list = [character_1, character_2, character_3,
                       character_4, character_5, character_6]

    # game menu
    # while loop is used to display game menu after every action
    while True:

        clear_console()
        greeting_message()

        print("1: Play")
        print("2: Show fighter stats ")
        print("any key: quit")

        choice = input('\nType corresponding number: ')
        if choice == '1':
            fighting_chars = match_making(characters_list[:])
            referee(fighting_chars[0], fighting_chars[1])
            fight(fighting_chars[0], fighting_chars[1])

        elif choice == '2':
            show_char_stats(characters_list)
        else:
            break


if __name__ == '__main__':
    main()
