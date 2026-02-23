import sys

from typing import Sequence
from keyboard_enums import CLEAR_TO_EOL, RESTORE_CURSOR, SAVE_CURSOR, NEW_LINE



def dump(line: str) -> None:
    sys.stdout.write(line)

def singleprint(line: str) -> None:
    dump(line)
    add_new_line()


def multiprint(lines: Sequence[str]) -> None:
    if not lines:
        return
    
    restore_cursor()
    for index, line in enumerate(lines):
        dump(line)
        finish_line()
        add_new_line()
    
    flush()


def finish_line() -> None: 
    dump(CLEAR_TO_EOL)


def add_new_line() -> None:
    dump(NEW_LINE)
    
def save_cursor() -> None:
    dump(SAVE_CURSOR)

def restore_cursor() -> None:
    dump(RESTORE_CURSOR)

def flush() -> None:
    sys.stdout.flush()