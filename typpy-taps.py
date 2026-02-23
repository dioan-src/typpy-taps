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

def typing_test():

    try:
        game = (Game()).set_size(SentenceSize.MEDIUM).set_target()

        if not game.initialized:
            raise Exception("Something's fucked")

        game.start()    

        singleprint("Type the following line: ")
        save_cursor()
        
        multiprint([game.get_target(), "↑"])

        while True:
            if game.get_index() == len(game.get_target()):
                break

            char = getch()

            if char in {ENTER, ESC, CTRLC}:
                raise KeyboardInterrupt

            if char not in {BACKSPACE, DEL}:
                game.increase_total_typed()

            expected_char = game.get_current_char()

            if char == BACKSPACE:
                game.decrease_index()
                display_line = f"\033[32m{game.get_target()[:game.get_index()]}\033[0m{game.get_target()[game.get_index():]}"
                pointer_line = (" " * game.get_index()) + f"↑"
            elif expected_char == char:
                game.increase_index()
                display_line = f"\033[32m{game.get_target()[:game.get_index()]}\033[0m{game.get_target()[game.get_index():]}"
                pointer_line = (" " * game.get_index()) + f"↑"
            else:
                game.increase_mistakes()
                passed_portion = game.get_target()[:game.get_index()]
                leftover_portion = game.get_target()[game.get_index():]
                display_line = (
                    f"\033[32m{passed_portion}\033[0m"+f"\033[31m{char}\033[0m"+f"{leftover_portion}"
                )
                pointer_line = (" " * (game.get_index()+1)) + f"↑"

            multiprint([display_line, pointer_line])

            

        game.set_end_time()
        game.set_result()

        if game.is_won():
            multiprint([
                "Done!",
                f"Time: {game.get_time_elapsed():.2f}s",
                f"Wrong characters: {game.get_mistakes()}",
                f"Total typed: {game.get_total_typed()}",
                f"Accuracy: {((game.get_total_typed() - game.get_mistakes()) / game.get_total_typed()) * 100:.2f}%",
            ])
        else:
            singleprint("Well that absolutely sucked wtf")

    except KeyboardInterrupt:
        singleprint("Game ended by user")
    except Exception as e:
        singleprint(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    typing_test()