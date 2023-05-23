import pyautogui
from PIL import Image
import PIL.ImageGrab
import pytesseract
import time
import datetime

# Bot behavior
BOT_ENTRANCE_THRESHOLD = 3
BET_DEPTH_LIMIT = 1
BALANCE = 2000  # reais
BLIND = 50  # reais
LOG_DATE = '20232205_21h20m'
LOGGING = False



def find_max_fall(numbers):
    extrema = []
    n = len(numbers)
    
    # Include the first number in the list as a local extremum
    extrema.append(numbers[0])
    
    # Iterate over the numbers, excluding the first and last ones
    for i in range(1, n - 1):
        # Check if the current number is a local extremum
        if (numbers[i] >= numbers[i-1] and numbers[i] >= numbers[i+1]) or \
           (numbers[i] <= numbers[i-1] and numbers[i] <= numbers[i+1]):
            if extrema[-1] != numbers[i]:
                extrema.append(numbers[i])
    
    # Include the last number in the list as a local extremum
    
    extrema.append(numbers[-1])
    
    max_fall = 0
    if extrema[0] > extrema[1]:
        i = 0
        while i < len(extrema)-1:
            fall = extrema[i] - extrema[i+1]
            if fall > max_fall:
                max_fall = fall
            i = i + 2
    else:
        i = 1
        while i < len(extrema)-1:
            fall = extrema[i] - extrema[i+1]
            if fall > max_fall:
                max_fall = fall
            i = i + 2

    return max_fall


def money_printer():
    print(
        """
    ____  _________________ _____ ______   ____  ____  ______
   / __ )/ ____/_  __/__  // ___// ____/  / __ )/ __ \/_  __/
  / __  / __/   / /   /_ </ __ \/___ \   / __  / / / / / /   
 / /_/ / /___  / /  ___/ / /_/ /___/ /  / /_/ / /_/ / / /    
/_____/_____/ /_/  /____/\____/_____/  /_____/\____/ /_/     
"""
    )

    global BALANCE
    global BOT_ENTRANCE_THRESHOLD
    global BET_DEPTH_LIMIT
    global BLIND

    initial_balance = BALANCE
    max_balance = BALANCE
    min_balance = BALANCE
    log_balance = []

    initial_time = datetime.datetime.now().strftime("%Y%d%m_%Hh%Mm")
    sequence = ["W" for i in range(BOT_ENTRANCE_THRESHOLD)]
    current_bet = BLIND
    betting = False
    bet_team = ""
    current_bet_depth = 0
    lost_to = None
    lost = False

    with open(f"logs/{LOG_DATE}_sequence.txt", "r") as file:
        # Read the lines and store them in an array
        original_sequence = file.readlines()[0]
        original_sequence = list(original_sequence)

    while BALANCE > 0 and len(original_sequence):
        while BALANCE > 0 and len(original_sequence):
            result = original_sequence.pop(0)
            if result in ["A", "H"]:
                if betting:
                    if result == bet_team:
                        BALANCE = BALANCE + 2 * current_bet
                        current_bet = BLIND
                        betting = False
                        bet_team = ""
                        current_bet_depth = 0
                    elif current_bet_depth < BET_DEPTH_LIMIT or BET_DEPTH_LIMIT == -1:
                        current_bet = 2 * current_bet
                        current_bet_depth = current_bet_depth + 1
                    else:
                        current_bet = BLIND
                        betting = False
                        bet_team = ""
                        current_bet_depth = 0
                        lost = True
                        if result == "A":
                            lost_to = "A"
                        else:
                            lost_to = "H"

                break

            elif result == "D":
                if betting:
                    BALANCE = BALANCE + current_bet / 2
                    current_bet = BLIND
                    betting = False
                    bet_team = ""
                    current_bet_depth = 0
                    lost_to = "D"
                    lost = True

                break

        if result == "A":
            current_winner = "A"
        elif result == "H":
            current_winner = "H"
        else:
            current_winner = "D"

        if current_winner != lost_to:
            lost = False

        sequence.insert(0, current_winner)

        if (
            all(x == current_winner for x in sequence[0:BOT_ENTRANCE_THRESHOLD])
            and current_winner != "D"
            and not lost
        ):
            if current_bet > BALANCE:
                current_bet = BLIND
                betting = False
                bet_team = ""
                current_bet_depth = 0
                lost_to = current_winner
                lost = True
            elif current_winner == "A":
                betting = True
                bet_team = "H"
                BALANCE = BALANCE - current_bet
            elif current_winner == "H":
                bet_team = "A"
                betting = True
                BALANCE = BALANCE - current_bet

        log_balance.append(BALANCE)

        if LOGGING:
            with open(f"logs/simulation/{initial_time}_sequence.txt", "a+") as f:
                f.write(current_winner)
                f.close()
            with open(f"logs/simulation/{initial_time}_balance.txt", "a+") as f:
                f.write(str(BALANCE))
                f.write("\n")
                f.close()

        if BALANCE > max_balance:
            max_balance = BALANCE
        if BALANCE < min_balance:
            min_balance = BALANCE

    print("Entrance", BOT_ENTRANCE_THRESHOLD)
    print("Depth:", BET_DEPTH_LIMIT)
    print()
    print("=============")
    print()

    print("Initial Balance:", initial_balance)
    print("Min Balance:", min_balance)
    print("Max Balance:", max_balance)
    print("Max Fall:", find_max_fall(log_balance))

    print()
    print("=============")
    print()

    print("Balance:", BALANCE)


money_printer()
