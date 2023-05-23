import re
import numpy as np
import matplotlib.pyplot as plt

def break_string_on_change(string):
    result = ""
    previous_char = ""

    for char in string:
        if char != previous_char:
            result += "\n"
        result += char
        previous_char = char

    return result.strip()


def count_using_regex(string, character, size):
    return len(re.findall('^' + character + '{'+ str(size) + '}$', string, re.MULTILINE))

def histogram(string, max_ending=None):
    string_formatted = break_string_on_change(input_string)

    D = []
    H = []
    A = []

    if max_ending == None:
        max_ending = len(string) + 1
        
    for i in range(max_ending):
        if i:
            D.append(count_using_regex(string_formatted, 'D', i))
            H.append(count_using_regex(string_formatted, 'H', i))
            A.append(count_using_regex(string_formatted, 'A', i))
    
    positions = np.arange(1, max_ending)
    bar_width = 0.2

    # print('D', D)
    # print('H', H)
    # print('A', A)
    # plt.bar(range(1,max_ending), H)
    # Plot the bars for H, A, and D
    plt.bar(positions, H, bar_width, label='H')
    plt.bar(positions + bar_width, A, bar_width, label='A')
    plt.bar(positions + 2 * bar_width, D, bar_width, label='D')

    plt.xticks(positions + 2 * bar_width, np.arange(1, max_ending, 1.0))

    # plt.xticks(np.arange(1, max_ending, 1.0))
    plt.ylabel('frequency')
    plt.show()
    

# Test the function
input_string = "AAAAAHAAAAAAHAAAAHAAAADAAAAAAHHAHAAHAHHHADAHAAHHHAAHHHHHHAAAAAAAHHAHAAHHHAAAHAAAHHAAAHHHAHHAHAAHAHHHHAAHDAAAAAHHAAAHHAHAAHAHAHHDAAAAHHAAAAAHDHAHAHAHHDHHAAHHHAADHAHHHHADADHHAAHAAAHHAAADHAHHAHDAHADHAAAHHAHHAAHAAHAAHHHAHHHHHAHHAAAHHAHDHHDHAAHHAAHHHHAHAAHAAHAHHHHAHAAAHAAAHHAAAHAAAADAHHAHAAAHHHADHAHHAHAHAHHHADAADHHHAHHHHHAAHHAHAAHHAAAAHAAAHAADHAAHDDAHADAHHHDHDHDAHHHAHAHHAAAHAAADAADHHAHAHAAHAADHAAHAAAAHAAHAAAHAAHHAHAAAHHAHAHADDADAHAAAAAAHAHDHDAAAHHAHAAAAHAADHADHH"
# input_string = "DAHAHHDAAAA"
# sequence_size = 4
# target_character = 'D'
# result = count_sequence(input_string, sequence_size, target_character)
# print(f"{result} sequences of size {sequence_size} of '{target_character}' in a row.")

histogram(input_string, 21)

