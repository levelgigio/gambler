# https://livecasino.bet365.com/Play/FootballCardShowdown
print(
    """
    ____  _________________ _____ ______   ____  ____  ______
   / __ )/ ____/_  __/__  // ___// ____/  / __ )/ __ \/_  __/
  / __  / __/   / /   /_ </ __ \/___ \   / __  / / / / / /   
 / /_/ / /___  / /  ___/ / /_/ /___/ /  / /_/ / /_/ / / /    
/_____/_____/ /_/  /____/\____/_____/  /_____/\____/ /_/     
"""
)

import pyautogui
from PIL import Image
import PIL.ImageGrab
import pytesseract
import time
import datetime

pytesseract.pytesseract.tesseract_cmd = (
    "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

# Positions on screen
MIDDLE_OF_SCREEN = (
    980,
    500,
)  # middle of screen to keep mouse away from buttons when not betting
COUNTDOWN_TIMER = (960, 450, 990, 480)  # countdown for betting
WIN_BANNER = (
    915,
    270,
    1035,
    290,
)  # result of a winning bet appears in a different position
RESULT_BANNER = (920, 385, 1030, 410)  # result of a normal round
BET_HOME_TEAM = (865, 890)  # position of button to bet home
BET_AWAY_TEAM = (1090, 890)  # position of button to bet away
REFRESH_PAGE = (110, 65)  # position of refresh button on browser
EXPAND_PAGE = (1640, 345)  # expand the cassino transmission
# LATEST_WINNER = (375, 835, 400, 855) # position of latest winner on the 21 blocks on down-left

# Bot behavior
BOT_ENTRANCE_THRESHOLD = 3  # bet only after N repetitions
BET_DEPTH_LIMIT = 1  # double the bet on losing N times
AFK_TIMER = 2.5  # minutes of not betting on anything
UNINDENTIFIED_TIMER = 5  # minutes of bot not recognizing a result. implies that something went wrong with screen
BALANCE = 200  # how much bot have to play in reais
BLIND = 5  # value of one chip in reais
LOGGING = True  # wheter or not generate a log file
OBSERVING_ONLY = True  # whether or not bot should click or only monitor


def click(x, y, print_action=True):
    # Move the mouse to the specified position
    pyautogui.moveTo(x, y)

    # Perform a left mouse button click
    pyautogui.click()

    if print_action:
        print("Click performed successfully.")


def crop(image, x1, y1, x2, y2):
    # Crop the image
    cropped_image = image.crop((x1, y1, x2, y2))
    return cropped_image


def screenshot():
    # Capture the screen
    screenshot = PIL.ImageGrab.grab()
    return screenshot


def identify(image):
    # Apply OCR to extract text from the image
    text = pytesseract.image_to_string(
        image,
        config="--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    )
    return text.strip()


def money_printer():
    global BALANCE
    global BOT_ENTRANCE_THRESHOLD
    global BET_DEPTH_LIMIT
    global BLIND

    # Hard reset the bot
    sequence = ["W" for i in range(BOT_ENTRANCE_THRESHOLD)]
    current_bet = BLIND
    betting = False
    bet_team = ""
    latest_action_time = datetime.datetime.now()
    latest_identified_result = datetime.datetime.now()
    initial_time = datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm")
    current_bet_depth = 0
    lost_to = None
    lost = False

    if LOGGING:
        # Log parameters
        with open(f"logs/{initial_time}_parameters.txt", "a+") as f:
            f.write("BOT_ENTRANCE_THRESHOLD = " + str(BOT_ENTRANCE_THRESHOLD) + "\n")
            f.write("BET_DEPTH_LIMIT = " + str(BET_DEPTH_LIMIT) + "\n")
            f.write("BALANCE = " + str(BALANCE) + "\n")
            f.write("BLIND = " + str(BLIND) + "\n")
            f.close()

    # While not bankrupt
    while BALANCE > 0:
        # Result identification loop
        while True:
            # Searchs for the result. Could be in two different positions on
            # screen depending on wheter you won or lose or not play at all
            result = identify(crop(screenshot(), *RESULT_BANNER))
            resultwin = identify(crop(screenshot(), *WIN_BANNER))

            # If result is AWAYTEAM or HOMETEAM
            if result in ["AWAYTEAM", "HOMETEAM"] or resultwin in [
                "AWAYTEAM",
                "HOMETEAM",
            ]:
                # Reset mouse position
                if not OBSERVING_ONLY:
                    click(*MIDDLE_OF_SCREEN, print_action=False)

                # Result was identified
                latest_identified_result = datetime.datetime.now()
                print()
                print(result, resultwin)
                # If betting we should check wheter the result identified represents
                # a winning or a losing bet, and act accordinly
                if betting:
                    # Winning a bet
                    if result == bet_team or resultwin == bet_team:
                        print("You won R$", 2 * current_bet)
                        BALANCE = BALANCE + 2 * current_bet
                        current_bet = BLIND
                        betting = False
                        bet_team = ""
                        current_bet_depth = 0

                    # Lost a bet but see if depth allows to go to double or nothing
                    elif current_bet_depth < BET_DEPTH_LIMIT or BET_DEPTH_LIMIT == -1:
                        print("Increasing bet to R$", 2 * current_bet)
                        current_bet = 2 * current_bet
                        current_bet_depth = current_bet_depth + 1

                    # Actually lost
                    else:
                        print("You lost")
                        current_bet = BLIND
                        betting = False
                        bet_team = ""
                        current_bet_depth = 0
                        lost = True
                        if result == "AWAYTEAM" or resultwin == "AWAYTEAM":
                            lost_to = "A"
                        else:
                            lost_to = "H"

                print("Your balance is:", BALANCE)

                # Exit result identification loop because it identified AWAYTEAM or HOMETEAM
                break

            # If result is DRAW
            elif result == "DRAW" or resultwin == "DRAW":
                # Reset mouse position
                if not OBSERVING_ONLY:
                    click(*MIDDLE_OF_SCREEN, print_action=False)

                # Result was identified
                latest_identified_result = datetime.datetime.now()
                print()
                print(result, resultwin)

                # When you get a draw on your bet, you get back half,
                # and stops betting for now
                if betting:
                    print("You get back R$", current_bet / 2)
                    BALANCE = BALANCE + current_bet / 2
                    current_bet = BLIND
                    betting = False
                    bet_team = ""
                    current_bet_depth = 0
                    lost_to = "D"
                    lost = True

                print("Your balance is:", BALANCE)

                # Exit result identification loop because it identified a DRAW
                break

            # No result identified
            else:
                # Check if something went wrong with page.
                # Represents a bot timeout
                if (
                    datetime.datetime.now() - latest_identified_result
                ).total_seconds() > UNINDENTIFIED_TIMER * 60:
                    # Slowly refresh page
                    print()
                    print(
                        f"Refreshing page because of result banner was not being identified for {UNINDENTIFIED_TIMER} minutes"
                    )
                    click(*REFRESH_PAGE)
                    time.sleep(5)
                    print("Expanding page...")
                    click(*EXPAND_PAGE)

                    # Hard reset the bot
                    sequence = ["W" for i in range(BOT_ENTRANCE_THRESHOLD)]
                    current_bet = BLIND
                    betting = False
                    bet_team = ""
                    latest_action_time = datetime.datetime.now()
                    latest_identified_result = datetime.datetime.now()
                    initial_time = datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm")
                    current_bet_depth = 0
                    lost_to = None
                    lost = False

                    # Restart looking for a result
                    continue

                # If nothing is wrong with page but nothing was identified either,
                # continue the loop until it identifies a result or timeouts
                time.sleep(0.5)

        # Switch values
        if result == "AWAYTEAM" or resultwin == "AWAYTEAM":
            current_winner = "A"
        elif result == "HOMETEAM" or resultwin == "HOMETEAM":
            current_winner = "H"
        else:
            current_winner = "D"

        # This is used to create the behavior of only returning on betting after
        # the streak of repeating results ends
        if current_winner != lost_to:
            lost = False

        # Monitor the sequence of results
        sequence.insert(0, current_winner)

        # Prints the sequence of results. Max size of array printed is 14 to avoid
        # visual polution
        print(
            sequence[
                : -(
                    BOT_ENTRANCE_THRESHOLD
                    if len(sequence) - BOT_ENTRANCE_THRESHOLD <= 14
                    else BOT_ENTRANCE_THRESHOLD + len(sequence) - 14
                )
            ]
        )

        # Wait a bit
        time.sleep(1)

        # After giving a result the game shows a countdown timer that allows players
        # to place their bets. Only during this time the buttons to bet are available.
        # We need to make sure it is showing this so our bot can click and bet.
        countdown_list = []
        while True:
            # Try to identify the countdown
            countdown = identify(crop(screenshot(), *COUNTDOWN_TIMER))

            # Sometimes a random number is identified, so to make sure it is capturing
            # a countdown timer, we wait until we identify two numbers in a row,
            # like 9 and then 8, or 7 and then 6, and so on. So we take roughly
            # 2 seconds to identify the countdown.
            if (
                countdown in [str(i) for i in range(1, 10)]
                and countdown not in countdown_list
            ):
                if len(countdown_list):
                    if int(countdown_list[-1]) - int(countdown) == 1:
                        print("Timer:", countdown)
                        latest_identified_result = datetime.datetime.now()
                        break
                countdown_list.append(countdown)

            # No number identified. Check if something went wrong with page.
            # Represents a bot timeout
            elif (
                datetime.datetime.now() - latest_identified_result
            ).total_seconds() > UNINDENTIFIED_TIMER * 60:
                # Slowly refresh page
                print()
                print(
                    f"Refreshing page because of countdown timer not being identified for {UNINDENTIFIED_TIMER} minutes"
                )
                click(*REFRESH_PAGE)
                time.sleep(5)
                print("Expanding page...")
                click(*EXPAND_PAGE)

                # Hard reset the bot
                sequence = ["W" for i in range(BOT_ENTRANCE_THRESHOLD)]
                current_bet = BLIND
                betting = False
                bet_team = ""
                latest_action_time = datetime.datetime.now()
                latest_identified_result = datetime.datetime.now()
                initial_time = datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm")
                current_bet_depth = 0
                lost_to = None
                lost = False

                # Break the countdown identification loop. Will actually skip all
                # conditions below except for logging and waiting.
                # Will restart looking for a result
                break

            # If nothing is wrong with page but nothing was identified either,
            # continue the loop until it identifies the countdown or timeouts
            else:
                time.sleep(0.2)

        # If sequence is matching the parameter for bot bet entrance, it should
        # start betting!
        if (
            all(x == current_winner for x in sequence[0:BOT_ENTRANCE_THRESHOLD])
            and current_winner != "D"
            and current_winner != "W"
            and not lost
        ):
            # If the bet is greater than the balance, skip it
            if current_bet > BALANCE:
                print("You do not have funds to keep up with the bet.")
                # Soft reset the bot
                current_bet = BLIND
                betting = False
                bet_team = ""
                current_bet_depth = 0
                lost_to = current_winner
                lost = True

            # If the repeating result is A then bet H
            elif current_winner == "A":
                print("Betting R$", current_bet, "on HOME")
                betting = True
                bet_team = "HOMETEAM"
                for i in range(current_bet // BLIND):
                    if not OBSERVING_ONLY:
                        click(*BET_HOME_TEAM)
                    time.sleep(0.2)
                BALANCE = BALANCE - current_bet
                if not OBSERVING_ONLY:
                    latest_action_time = datetime.datetime.now()

            # If the repeating result is H then bet A
            elif current_winner == "H":
                print("Betting R$", current_bet, "on AWAY")
                bet_team = "AWAYTEAM"
                betting = True
                for i in range(current_bet // BLIND):
                    if not OBSERVING_ONLY:
                        click(*BET_AWAY_TEAM)
                    time.sleep(0.2)
                BALANCE = BALANCE - current_bet
                if not OBSERVING_ONLY:
                    latest_action_time = datetime.datetime.now()

            # Wait for the dealer
            time.sleep(4)

        # Sequence is not matching the parameters, bot is not betting. Let's check if
        # it has been AFK too long, so we can refresh the page to reset the Anti-AFK system
        elif (
            datetime.datetime.now() - latest_action_time
        ).total_seconds() > AFK_TIMER * 60:
            # Quickly refresh page
            print()
            print(f"Refreshing page because of AFK TIMER of {AFK_TIMER} minutes")
            click(*REFRESH_PAGE)
            time.sleep(1)
            print("Expanding page...")
            click(*EXPAND_PAGE)

            # Refreshing represents an action to avoid getting caught on the Anti-AFK system
            latest_action_time = datetime.datetime.now()

        # Sequence is no good for bot bet entrance, and it has not been AFK, so just
        # wait for the dealer
        else:
            time.sleep(4)

        if LOGGING:
            # Log sequence
            with open(f"logs/{initial_time}_sequence.txt", "a+") as f:
                f.write(current_winner)
                f.close()

            # Log balance
            with open(f"logs/{initial_time}_balance.txt", "a+") as f:
                f.write(str(BALANCE))
                f.write("\n")
                f.close()
            
            # Log times
            with open(f"logs/{initial_time}_time.txt", "a+") as f:
                f.write(datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm"))
                f.write("\n")
                f.close()



money_printer()
