import time
import sys
import tty
import termios

from Game import Game
from data.sentences import SentenceSize
from data.sentences import get_random_sentence
from helpers.console import singleprint, multiprint, save_cursor
from keyboard_enums import ENTER, BACKSPACE, CTRLC, ESC, CLEAR_TO_EOL, DEL

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == CTRLC:
            raise KeyboardInterrupt
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def typing_test(target):

    index = 0
    wrong_count = 0
    total_typed = 0
    success = False
    
    start_time = time.time()

    singleprint("Type the following line: ")
    save_cursor()
    
    multiprint([target, "↑"])

    while True:
        if index == len(target):
            success = True
            break

        try:
            char = getch()

            if char in {ENTER, ESC, CTRLC}:
                break

            if char not in {BACKSPACE, DEL}:
                total_typed += 1

            expected_char = target[index] if index < len(target) else None


            if char == BACKSPACE:
                if index>0:
                    index -= 1
                display_line = f"\033[32m{target[:index]}\033[0m{target[index:]}"
                pointer_line = (" " * index) + f"↑"
            elif expected_char == char:
                index += 1
                display_line = f"\033[32m{target[:index]}\033[0m{target[index:]}"
                pointer_line = (" " * index) + f"↑"
            else:
                passed_portion = target[:index]
                leftover_portion = target[index:]
                wrong_count += 1
                display_line = (
                    f"\033[32m{passed_portion}\033[0m"+f"\033[31m{char}\033[0m"+f"{leftover_portion}"
                )
                pointer_line = (" " * (index+1)) + f"↑"

            multiprint([display_line, pointer_line])

        except KeyboardInterrupt:
            break


    end_time = time.time()
    elapsed = end_time - start_time

    if success:
        multiprint([
            "Done!",
            f"Time: {elapsed:.2f}s",
            f"Wrong characters: {wrong_count}",
            f"Total typed: {total_typed}",
            f"Accuracy: {((total_typed - wrong_count) / total_typed) * 100:.2f}%",
        ])
    else:
        singleprint("\nWell that absolutely sucked wtf")

if __name__ == "__main__":
    try:

        game = (Game()).set_size(SentenceSize.MEDIUM).set_target()
        
        print(vars(game))

        if game.initialized:
            print('Good to go')
        else:
            print('shit to go')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")