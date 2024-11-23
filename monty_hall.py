# this file will contain a function for each step of the Monty Hall Problem
# there are some style issues here I'd like to clean up, mainly the long lines

import random
import time


# create function to clean up how door numbers are displayed
def display_door(door_num):
    return door_num.replace('_', ' #').capitalize()


# function to hide prizes behind each door
def hide_prizes():
    # set all doors to have goat
    doors = {'door_1': 'goat', 'door_2': 'goat', 'door_3': 'goat'}
    # re-assign random door for car
    car_door = random.randint(1,3)
    if car_door == 1:
        doors['door_1'] = 'car'
    elif car_door == 2:
        doors['door_2'] = 'car'
    else:
        doors['door_3'] = 'car'
    return doors


# function to let user choose their door, or default to Door 1
def choose_door(user_input=True, door_num='1', door_name='door_1'):
    if user_input:
        door_num = input('Choose a door. Number 1, 2, or 3? ')
    # allow escape to break loop
    if not door_num.isalnum():
        return door_num
    # convert door number to door name
    door_int = int(door_num)
    if door_int in (1, 2, 3):
        door_name = 'door_' + str(door_int)
    # if input was not 1, 2, or 3—prompt user again
    else:
        door_name = choose_door(door_num=input('Input out of range. Please choose a number 1-3. '))
    return door_name


# function to reveal a door with a goat
def reveal_goat(doors, chosen_door):
    # if not the chosen door or hiding the car, add to list of possible doors to open
    doors_list = [k for k, v in doors.items() if (k != chosen_door) & (v != 'car')]
    # now there are either 1 or 2 possible doors left
    if len(doors_list) == 1:
        revealed_door = doors_list[0]
    # if there are 2 possibilities, choose 1 at random
    elif len(doors_list) == 2:
        revealed_door = random.choice(doors_list)
    # find the remaining door
    remaining_door = [k for k in doors if k not in (chosen_door, revealed_door)][0]
    return revealed_door, remaining_door


# function to switch doors or stay
def switch_stay(doors, chosen_door, revealed_door, user_input = True, switch_decision = 'y', first_run = True):
    # for some reason, this function likes to jump others in execution order, so I'm slowing it down in demo mode
    if (user_input) & (first_run):
        time.sleep(1)

    # find remaining door that hasn't been chosen or revealed
    doors_dict = doors.copy()
    doors_to_remove = (chosen_door, revealed_door)
    for k in doors_to_remove:
        doors_dict.pop(k, None)
    remaining_door = list(doors_dict)[0]

    # if requesting user input and this is the first time the question is being asked, prompt with this text
    if user_input:
        switch_decision = input(f'Would you like to switch to {display_door(remaining_door)} or stay with {display_door(chosen_door)}? Type Y to switch or N to stay.\n')
        
    # if Yes to switch, return remaining door; if No to switch, return chosen door
    if switch_decision.lower() == 'y':
        final_door = remaining_door
    elif switch_decision.lower() == 'n':
        final_door = chosen_door
    # if this user gives a different alphanumeric answer, give different question text
    elif switch_decision.isalnum():
        final_door = switch_stay(doors=doors, chosen_door=chosen_door, revealed_door=revealed_door, user_input=False,
                                 first_run=False,
                                 switch_decision=input(f'Input out of range. Please type Y to switch to {display_door(remaining_door)} or type N to stay with {display_door(chosen_door)}. '))
    # if no input (like Esc to skip input), assume Stay
    else:
        print(f"No user input detected. Let's assume you stay with {display_door(chosen_door)}.")
        final_door = chosen_door

    return final_door


# function to reveal prize
def reveal_prize(doors, chosen_door, revealed_door, final_door, theatrics=True):
    chosen_prize = doors[final_door]
    # when running for demonstration purposes rather than statistical
    if theatrics:
        if chosen_door == final_door:
            decision, conj, prep_object = 'stay', 'and', f'with {display_door(final_door)}'
        else:
            decision, conj, prep_object = 'switch', 'but', f'to {display_door(final_door)}'
        print(f"\nSo you originally chose {display_door(chosen_door)}, {conj} you've decided to {decision.upper()} {prep_object}.")
        print(f"We've already revealed that there was a goat behind {display_door(revealed_door)}.")
        print(f"Let's see if you made the right decision! We can now reveal that behind {display_door(final_door)} is a...")
        time.sleep(6)
        for _ in range(3):
            time.sleep(1.5)
            print("...")
        time.sleep(1.5)
        print(f"\n{chosen_prize.upper()}!\n")
        if chosen_prize == 'car':
            print(f"You made the right decision to {decision} {prep_object}. You won!\n")
        else:
            winning_door = [k for k, v in doors.items() if v == 'car'][0]
            print(f"Oh no! You shouldn't have {decision+'ed'} {prep_object}.")
            print(f"The car was behind {display_door(winning_door)}. Better luck next time...\n")
    else:
        return chosen_prize


# define function for the introduction to the game
def intro(user_input=True, ready='y'):
    if user_input:
        print("\nWelcome! You find yourself facing the Monty Hall Problem.\n")
        print("There are 3 doors in front of you. Behind one door is a car, but behind the other two there is a goat.")
        print("If you pick the right door, you win the new car! Are you ready to play?\n")
        ready = input("Enter Y to continue or N to contemplate this real stumper.\n").lower()
        if ready=='n':
            ready = input("All good! Think it over. And whenever you're ready to continue, please enter Y. Or, enter N to cancel.\n")
        cta = " Please enter Y to continue or N to cancel.\n"
        flippant_responses = [f"Well that wasn't even an option. Let's try again!",
            f"Okay, what are we doing here? It's one button.",
            f"C'mon man, I worked kinda hard on this. Can you just play the game?",
            f"Honestly, I don't even blame you—I'd be doing the same thing.",
            f"But seriously, this is a fun little demo project. I don't have time to write infinite responses.",
            f"I am begging you. Please, for the love of all that is good in the world, free me from this.",
            f"What's your favorite Bill Murray movie? Mine is Groundhog Day.",
            f"I could've been spending time with my future wife and our cat, but nOoOooOOOoooOooOOo I had to be prepared for a real Dr. Diligent like you to see how much flavor text I could muster.",
            f"At this point, if I get even a polite chuckle out of you, you at least owe me an interview.",
            f"Oh yeah, that's what this is all about, building out my portfolio—a thing everyone says you need to do despite 99% of applications not making it to the point in the process where anyone would consider your portfolio.",
            f"I'm not keeping track of every entry, so are you trying a bunch of different keys or do you have a favorite?",
            f"I bet there's someone out there that's a real ampersand lover. Maybe there's a couple of them. I now pronounce you Mr. and Dr. Ampersand.",
            f"Alright we've had a lot of fun here today, but I think it's important that we go ahead and continue.",
            f"Huh. Okay. I thought we'd kind of established a rapport there. I see. Um.",
            f"You know what, this is getting mean. Honestly, I just wanted to play a game with you.",
            f'Wait that reminds me, did you know that the highest rated movie in the Saw franchise is "Saw X"? Weird, right? Almost as weird as it being the 9th Saw movie.',
            f"Okay but wait, similar note, what was the deal with Microsoft going from Windows 8 to Windows 10? And wasn't that a thing with the iPhone too? I know 9 is a lucky number in China, so I don't think that's the reason.",
            f"I feel as if we've become friends here, so I need to make a confession. I lied to you. It was all in good fun, but I just can't hide the truth any longer. My favorite Bill Murray movie is actually Ghostbusters.",
            f"Hey Siri, play Closing Time by Semisonic.",
            f"At this point you've probably forgotten the rules of the game. If you don't continue now, you'll need to start over. This is not a bit—this is the last one of these."]
        # initialize response counter to not go out of bounds
        response_count = 0
        while (ready not in ('y', 'n')) & (response_count < len(flippant_responses)):
            ready = input(flippant_responses[response_count]+cta)
            response_count += 1
        if ready != 'y':
            print("Understandable. Goodbye.\n")
    else:
        pass
    return ready


# create function to combine steps of gameplay
def make_deal(demo_mode=True, switch_decision='y'):
    # add panache for demo mode
    if demo_mode:
        # introduction
        ready = intro(user_input=demo_mode)
        if ready != 'y':
            return print("You can restart whenever you're ready. Thanks for playing along!\n")
        
        # hide prizes, choose door
        doors = hide_prizes()
        chosen_door = choose_door(user_input=demo_mode)
        if chosen_door not in ('door_1', 'door_2', 'door_3'):
            return print("The only way to win is not to play.")
        print(f"\nYou've chosen {display_door(chosen_door)}.")

        # reveal goat
        revealed_door, remaining_door = reveal_goat(doors, chosen_door)
        print(f"\nWe're now going to reveal what's behind {display_door(revealed_door)}.")
        time.sleep(1)
        for _ in range(3):
            print("...")
            time.sleep(1)
        print("A goat!")

        # stay or switch
        print("\nNow you have an opportunity.")
        print(f"You can Stay and keep the prize behind {display_door(chosen_door)}, or you can Switch to {display_door(remaining_door)}.\n")
        final_door = switch_stay(doors, chosen_door, revealed_door, user_input=demo_mode)

        # reveal prize
        reveal_prize(doors, chosen_door, revealed_door, final_door, theatrics=demo_mode)

    # statistics mode
    else:
        doors = hide_prizes()
        chosen_door = choose_door(user_input=demo_mode)
        revealed_door, remaining_door = reveal_goat(doors, chosen_door)
        final_door = switch_stay(doors, chosen_door, revealed_door, user_input=demo_mode, switch_decision=switch_decision)
        prize = reveal_prize(doors, chosen_door, revealed_door, final_door, theatrics=demo_mode)
        return prize


# allow demo mode to be run as .py
if __name__ == '__main__':
    make_deal()