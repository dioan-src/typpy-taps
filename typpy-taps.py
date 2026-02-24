import time
import sys
import tty
import termios

from Game import Game
from renderer import render
from data.sentences import SentenceSize
from helpers.console import singleprint, multiprint, save_cursor
from keyboard_enums import ENTER, CTRLC, ESC, DEL

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

if __name__ == "__main__":
    try:
        game = (Game()).set_size(SentenceSize.MEDIUM).set_target()

        if not game.initialized:
            raise Exception("Something's fucked")

        game.start()    

        singleprint("Type the following line: ")
        save_cursor()
        
        multiprint([game.get_target(), "↑"])

        while not game.target_typed:

            char = getch()

            if char in {ENTER, ESC, CTRLC, DEL}:
                raise KeyboardInterrupt

            game.process_char(char)
            display_line, pointer_line = render(game, char)
            multiprint([display_line, pointer_line])

        game.set_end_time()

        multiprint([
            "Done!",
            f"Time: {game.get_time_elapsed():.2f}s",
            f"Mistakes: {game.get_mistakes()}",
            f"Total typed: {game.get_total_typed()}",
            f"Accuracy: {((game.get_total_typed() - game.get_mistakes()) / game.get_total_typed()) * 100:.2f}%",
            f"WPM: {game.get_net_wpm():.2f}"

        ])

    except KeyboardInterrupt:
        singleprint("Game ended by user")
    except Exception as e:
        singleprint(f"An unexpected error occurred: {e}")