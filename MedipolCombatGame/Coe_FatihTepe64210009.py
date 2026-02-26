import random


def medipol_combat():  #medipol combat game all game inside this function
    def user_name(order): #this function for players name
        print(f"-----{order} Hero-----")
        name = input(f"Please type your hero name:")
        while True: #loop until valid name
            if name == "": # if it is empty we can not accept
                name = input("Emtpy can not accept. Please type your hero name:")
            elif order == "Second" and name.lower() == player1.lower(): # two player's names can not be same
                name = input(f"{player1} is taken. Please choose name:")
            else:
                return name # if it is valid name

    def coin_toss():#for choose who is first
        coin_toss_result = random.randint(1, 2)# this line create one number
        if coin_toss_result == 1:#if number is 1 player1 will start first. so this chance is %50
            game_while(player1, player2)
        if coin_toss_result == 2:#if number is 2 player2 will start first. so this chance is %50
            game_while(player2, player1)

    def game_while(a, b): # this is game loop, a mean first user, b means second user
        a_health = 100
        b_health = 100
        print(f"Coin toss result: {a} starts fight")# this a change according to coin_toss function
        print("------------------------------------")

        while True:
            if a_health > 0 :
                healths(a, b, a_health, b_health)# this function make a table for Hp
                b_health -= attack(a)
                healths(a, b, a_health, b_health)#table for Hp
            elif a_health <= 0:
                healths(a, b, a_health, b_health)  # table for Hp
                winner=b
                game_over(winner)
                break
            if  b_health > 0:
                a_health -= attack(b)
            elif  b_health <= 0:
                winner = a
                game_over(winner)
                break

    def attack(attacker):
        print(f"---------{attacker} Attacks!!---------")
        attack_magnitude = int(input("Choose your attack magnitude between 1 and 50:"))
        while True:
            if 1 <= attack_magnitude <= 50: #magnitude must be betweem 1 and 50
                attack_chance = 100 - attack_magnitude#for example user input 30 this attack chance will be 70
                if random.randint(1, 100) <= attack_chance:#if attack_chance is 70. this if function will run 1 to 70 so chance is %70
                    attack_magnitude = attack_magnitude #this if function will run 1 to 70 so chance is %70.
                    break
                else:
                    attack_magnitude = 0 # if random randint bigger than 70 attack is 0
                    break
            else: # if it is not between 1 and 50
                print("Please enter a valid number. Attack magnitude must be between 1 and 50")
                attack_magnitude = int(input("Choose your attack magnitude between 1 and 50:"))
        if attack_magnitude == 0:# this means attack failed
            print(f"Opppps!  {attacker}  missed the attack")
            return 0
        else: # if attack successful
            print(f"{attacker} hits {attack_magnitude} damage!!!!")
            return attack_magnitude

    def healths(a, b, a_health, b_health):  # this function make a table
        print(a, " " * (int((a_health / 2) + 1)), " " * (50 - int(a_health / 2) + 1), b)  # this write players name
        print(f"HP[{a_health}]", "I" * int(a_health / 2), " " * (50 - int(a_health / 2)), f"HP[{b_health}]", "I" * int(b_health / 2))  # Hp
    def game_over(winner):
        print(60 * "#")
        print("#" * 30, winner, "Wins!!!!", 30 * "#")#x is winner's name
        print(60 * "#")
        answer = (input("Do you wanna play again:")).lower()
        if answer == "yes":# if do you wanna play again
            coin_toss()# start from coin_toss again
        elif answer == "no":
            print("Thanks for playing! See you again!")
        else:
            print("Thanks for playing! See you again!")

    player1 = user_name("First")
    player2 = user_name("Second")
    coin_toss()

medipol_combat()
