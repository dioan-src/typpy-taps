from Game import Game
from keyboard_enums import BACKSPACE

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

def render(game: Game, last_char: str | None = None) -> tuple[str, str]:
    target = game.get_target()
    index = game.get_index()

    passed = target[:index]
    leftover =target[index:]

    display = f"{GREEN}{passed}{RESET}{leftover}"
    pointer = " " * index + "↑"

    if (last_char 
        and not last_char == BACKSPACE 
        and not game.target_typed 
        and last_char != target[index-1]
    ):
        display = (
            f"{GREEN}{target[:index]}{RESET}"
            f"{RED}{last_char}{RESET}"
            f"{target[index:]}"
        )
        pointer = " " * (index+1) + "↑"

    return display, pointer

    