# Enigma Machine

# https://www.cryptomuseum.com/crypto/enigma/wiring.htm
# Enigma M4 U-Boot 

# ---------------------------------------------------------------------------

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logging.debug('Start of program\n')

#------------------------------------------------------------------------------
# Variables

# Rotors right side
char_bs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Rotors
rotor_1 = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
rotor_2 = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
rotor_3 = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
rotor_4 = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'
rotor_5 = 'VZBRGITYUPSDNHLXAWMJQOFECK'
rotor_6 = 'JPGVOUMFYQBENHZRDKASXLICTW'
rotor_7 = 'NZJHGRCXMYSWBOUFAIVLPEKQDT'
rotor_8 = 'FKQHTLXOCBJSPDZRAMEWNIUYGV'

all_rotors = ["rotor_1", "rotor_2", "rotor_3", "rotor_4", "rotor_5", "rotor_6", "rotor_7", "rotor_8"]

# Reflectors
all_reflectors = ["reflector_1", "reflector_2"]

reflector_1 = {'A': 'E', 'B': 'N', 'C': 'K', 'D': 'Q', 'E': 'A', 'F': 'U', 'G': 'Y', 'H': 'W', 'I': 'J', 'J': 'I', 'K': 'C', 'L': 'O', 'M': 'P', 'N': 'B', 'O': 'L', 'P': 'M', 'Q': 'D', 'R': 'X', 'S': 'Z', 'T': 'V', 'U': 'F', 'V': 'T', 'W': 'H', 'X': 'R', 'Y': 'G', 'Z': 'S'}
reflector_2 = {'A': 'R', 'B': 'D', 'C': 'O', 'D': 'B', 'E': 'J', 'F': 'N', 'G': 'T', 'H': 'K', 'I': 'V', 'J': 'E', 'K': 'H', 'L': 'M', 'M': 'L', 'N': 'F', 'O': 'C', 'P': 'W', 'Q': 'Z', 'R': 'A', 'S': 'X', 'T': 'G', 'U': 'Y', 'V': 'I', 'W': 'P', 'X': 'S', 'Y': 'U', 'Z': 'Q'}

# Plugboard 
plugboard_dict = {}

# Rootor spin count
r1_spin_count = 0
r2_spin_count = 0
r3_spin_count = 0

# List of letters after they go through rotors
rotor_letters = []

#------------------------------------------------------------------------------
# Functions

def raw_string():
    """
    Ask the user for a string of letters.
    Returns the user's raw message in capital letters.
    """
    condition = False

    while condition == False:
        raw_str = input("Your message: ")
        if len(raw_str) == 0 or raw_str.isspace():
            print("Type at least one character.")
        else:
            condition = True
    
    return raw_str.upper()

def plug_board():

    """
    Creates a dictionary (plugboard_dict) with the users letter swap choices

    Asks the user how many letter they want to swap.
    Asks for key:value letters for future swaping. 
    """

    # Number of cables in plug board
    condition_cables = False
    while condition_cables == False:
        nb_pb_cables = input("Number of plugboard cables: ")

        if not nb_pb_cables.isdecimal() or int(nb_pb_cables) > 13:
            print(f'Invalid input: {nb_pb_cables}. Value must be an integer in between 0 and 13.')
        else:
            logging.debug(nb_pb_cables)
            condition_cables = True

    # Matching letters in plugboard
    for cable in range(1, int(nb_pb_cables) + 1): 
        condition_letter_pair_1 = False
        condition_letter_pair_2 = False

        while condition_letter_pair_1 == False:
            letter_pair_1 = input(f"Cable {cable}. Input one letter: ")
            letter_pair_1 = letter_pair_1.upper()
            if not letter_pair_1.isalpha() or len(letter_pair_1) > 1:
                print(f'Invalid input. Input must be one letter')
            elif letter_pair_1 in plugboard_dict:
                print(f"Letter {letter_pair_1} already conected to {plugboard_dict[letter_pair_1]}")
            else:
                logging.debug(letter_pair_1)
                condition_letter_pair_1 = True

        while condition_letter_pair_2 == False:
            letter_pair_2 = input("Cable. Input one letter: ")
            letter_pair_2 = letter_pair_2.upper()
            if not letter_pair_2.isalpha() or len(letter_pair_2) > 1:
                print('Invalid input. Input must be one letter')
            elif letter_pair_2 in plugboard_dict:
                print(f"Letter {letter_pair_2} already conected to {plugboard_dict[letter_pair_2]}")
            else:
                logging.debug(letter_pair_2)
                condition_letter_pair_2 = True

        plugboard_dict.update({letter_pair_1:letter_pair_2})
        plugboard_dict.update({letter_pair_2:letter_pair_1})

    logging.debug(plugboard_dict)

def rotor_settings():

    """
    Returns r1, r2, r3 and rf with the user's choice for rotors and reflector.
    Removes the chosen itens from the global all_* lists 
    """

    def rotor_equivalent(r_number):

        """
        Match user input (string) with the correspondent rotor variable
        """

        if r_number == "rotor_1":
            return rotor_1
        elif r_number == "rotor_2":
            return rotor_2
        elif r_number == "rotor_3":
            return rotor_3
        elif r_number == "rotor_4":
            return rotor_4
        elif r_number == "rotor_5":
            return rotor_5
        elif r_number == "rotor_6":
            return rotor_6
        elif r_number == "rotor_7":
            return rotor_7
        elif r_number == "rotor_8":
            return rotor_8
        elif r_number == "reflector_1":
            return reflector_1
        elif r_number == "reflector_2":
            return reflector_2

    # Rotor 1
    condition = False
    while condition == False:
        r1 = input(f"ROTOR 1. Choose from {all_rotors}: ")
        if r1 not in all_rotors:
            print(f"Rotor must be one of the following rotors: {all_rotors}")
        else:
            all_rotors.pop(all_rotors.index(r1))
            r1 = rotor_equivalent(r1)
            logging.debug(all_rotors)
            condition = True

    # Rotor 2
    condition = False
    while condition == False:
        r2 = input(f"ROTOR 2. Choose from {all_rotors}: ")
        if r2 not in all_rotors:
            print(f"Rotor must be one of the following rotors: {all_rotors}")
        else:
            all_rotors.pop(all_rotors.index(r2))
            r2 = rotor_equivalent(r2)
            logging.debug(all_rotors)
            condition = True

    # Rotor 3
    condition = False
    while condition == False:
        r3 = input(f"ROTOR 3. Choose from {all_rotors}: ")
        if r3 not in all_rotors:
            print(f"Rotor must be one of the following rotors: {all_rotors}")
        else:
            all_rotors.pop(all_rotors.index(r3))
            r3 = rotor_equivalent(r3)
            logging.debug(all_rotors)
            condition = True

    # Reflector
    condition = False
    while condition == False:
        rf = input(f"REFLECTOR. Choose from {all_reflectors}: ")
        if rf not in all_reflectors:
            print(f"Rotor must be one of the following reflectors: {all_reflectors}")
        else:
            rf = rotor_equivalent(rf)
            logging.debug(all_rotors)
            condition = True

    return r1, r2, r3, rf

def rotors(char_pb, rotor_1, rotor_2, rotor_3, reflector):

    raw_letter_index = char_bs.index(char_pb)    # raw_letter in base_list index
    logging.debug(f'Raw index: {raw_letter_index}')

    # rotor_1
    letter_rt_1 = rotor_1[raw_letter_index]         # raw_letter encoded by rotor_1
    letter_rt_1_index = char_bs.find(letter_rt_1)  # letter_rt_1 in base_list index
           
    logging.debug(f'Rotor 1: {letter_rt_1}')

    # rotor_2
    letter_rt_2 = rotor_2[letter_rt_1_index]        # letter_rt_1 encoded by rotor_2
    letter_rt_2_index = char_bs.index(letter_rt_2)  # letter_rt_2 in base_list index

    logging.debug(f'Rotor 2: {letter_rt_2}')

    # rotor_3
    letter_rt_3 = rotor_3[letter_rt_2_index]        # letter_rt_2 encoded by rotor_3

    logging.debug(f'Rotor 3: {letter_rt_3}')

    # reflector
    reflected = reflector[letter_rt_3]                          # letter_rt_3 encoded by reflector

    logging.debug(f'{letter_rt_3} reflected: {reflected}')

    # rotor_3_back
    letter_rt_3_back_index = rotor_3.index(reflected)           # index of 'reflected' on rotor 3 left side [encrypted]
    letter_rt_3_back = char_bs[letter_rt_3_back_index]          # correspondet at rotor 3 right side [ABC]
            
    logging.debug(f'Rotor 3 back: {letter_rt_3_back}')

    # rotor_2_back
    letter_rt_2_back_index = rotor_2.index(letter_rt_3_back)    # index of 'letter_rt_3_back' on rotor 2 left side [encrypted]
    letter_rt_2_back = char_bs[letter_rt_2_back_index]          # correspondet at rotor 2 right side [ABC]

    logging.debug(f'Rotor 2 back: {letter_rt_2_back}')

    # rotor_1_back
    letter_rt_1_back_index = rotor_1.index(letter_rt_2_back)    # index of 'letter_rt_2_back' on left side rotor 1 [encrypted]
    letter_rt_1_back = char_bs[letter_rt_1_back_index]          # correspondet at rotor 1 right side [ABC] (main output)
            
    logging.debug(f'Rotor 1 back: {letter_rt_1_back}')

    return letter_rt_1_back

def letter_swap_pb(text):
    """
    Swap any letter that is connected to another letter in the plugboard.
    Return pb_text
    """

    pb_text = []

    for letter in text:
        if letter in plugboard_dict.keys():
            letter = plugboard_dict[letter]
        pb_text.append(letter)
    pb_text = "".join(pb_text)
        
    return pb_text

def rotor_spin(rt_1, rt_2, rt_3):
    """
    Spins the rotors when called
    26 - 26 - 26, beginning at 0 - 0 - 0

    A complete rotation on rotor_1 creates one spin on rotor_2.
    A complete rotation on rotor_2, creates one spin in rotor_3
    A complete rotation on rotor_3 stes all rotors to 0 - 0 - 0
    """

    global r1_spin_count, r2_spin_count, r3_spin_count
    global rotor_1, rotor_2, rotor_3

    # Spin rotor 1
    if r1_spin_count < 25:
        rotor_1 = rt_1[1:]+rt_1[0]
        r1_spin_count += 1
    else:
        rotor_1 = rt_1[1:]+rt_1[0]
        r1_spin_count = 0

        # Spin rotor 2
        if r2_spin_count < 25:
            rotor_2 = rt_2[1:]+rt_2[0]
            r2_spin_count += 1
        else:
            rotor_2 = rt_2[1:]+rt_2[0]
            r2_spin_count = 0
            
            # Spin rotor 3
            if r3_spin_count < 25:
                rotor_3 = rt_3[1:]+rt_3[0]
                r3_spin_count += 1
            else:
                rotor_3 = rt_3[1:]+rt_3[0]
                r3_spin_count = 0

# -------------------------------------------------------------------------------

# MAIN CODE

r1, r2, r3, rf = rotor_settings()
plug_board()
raw_string = raw_string()
pb_text = letter_swap_pb(raw_string)

for letter in pb_text.upper():
    if letter.isalpha():
        # Rotor spin
        rotor_spin(r1, r2, r3)  

        # Rotor letter
        new_letter = rotors(letter, r1, r2, r3, rf) 
        rotor_letters.append(new_letter)
    else:
        rotor_letters.append(letter)

rotor_text = "".join(rotor_letters)
pb_rotor_text = letter_swap_pb(rotor_text)
print("Your encripted message is: "+ pb_rotor_text)

logging.debug('End of program')
    

