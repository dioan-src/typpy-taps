import curses
from keyboard_enums import ENTER, CTRLC, ESC, DEL
from Mode import ClassicMode, RaceMode, PerfectionistMode
from dataclasses import dataclass
from typing import Type

@dataclass
class ModeConfig:
    name: str
    description: str
    mode_class: Type

MODES = {
    1: ModeConfig("Classic Mode", "Type out the sentence presented", ClassicMode),
    2: ModeConfig("Race Mode", "Complete the sentence before time runs out", RaceMode),
    3: ModeConfig("Perfectionist Mode", "Do or die. One mistake and you're out!", PerfectionistMode)
}

def main(stdscr):
    # Setup: Hide the blinking cursor and turn off key echoing
    curses.curs_set(0)
    stdscr.nodelay(False) # Wait for user input
    
    # Define color pairs (ID, Foreground, Background)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Correct
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Wrong
    
    # Run the game logic
    draw_modes_menu(stdscr)

def draw_modes_menu(stdscr):
    stdscr.clear() # Always clear the screen before redrawing
    
    # Syntax: addstr(y, x, "string", optional_color)
    stdscr.addstr(2, 2, " Welcome to Typpy-Taps", curses.A_BOLD)
    stdscr.addstr(4, 2, "Select mode", curses.A_BOLD)
    
    for index, mode in MODES.items():
        y_pos = 5 + index
        
        line = f"[{index}] {mode.name}: {mode.description}"
        stdscr.addstr(y_pos, 2, line)

    stdscr.refresh() # Updates the physical screen

    while True:
        key = stdscr.getch()
        
        try:
            choice = int(chr(key))
        except (ValueError, OverflowError):
            continue

        if choice in MODES:
            selected_mode = MODES[choice]
            break
        elif key == 27: # ESC to quit
            return

    # 4. Use the selected mode
    stdscr.clear()
    stdscr.addstr(5, 5, f"Initializing {selected_mode.name}...")
    stdscr.refresh()
    curses.napms(1000) # Pause for 1 second to show the message

    game = selected_mode.mode_class(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)