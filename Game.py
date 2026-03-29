from __future__ import annotations
import time
from typing import Optional
from keyboard_enums import BACKSPACE, DEL, GREEN_LETTERS, RED_LETTERS, RESET_LETTERS
from constants import MEAN_WORD_LENGTH, SECONDS_PER_MINUTE
from data.sentences import SentenceSize, get_random_sentence

class Game:
    def __init__(self) -> None:
        self.mode: Optional[str]
        self.size: SentenceSize = None
        self.target: Optional[str] = None
        self.index: int = 0
        self.wrong_count: int = 0
        self.total_typed: int = 0
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def set_size(self, size: SentenceSize = SentenceSize.TINY) -> Game:
        if self.size is not None:
            raise Exception("Size cannot be reset")
        
        self.size = size

        return self
    
    def set_target(self) -> Game:
        if self.target is not None:
            raise Exception("Target cannot be reset")
        if self.size is None:
            raise Exception("Cannot set target without difficulty")
        
        self.target = get_random_sentence(self.size)

        return self
    
    def start(self) -> None:
        self.start_time = time.time()

    def set_end_time(self) -> None:
        self.end_time = time.time()
    
    def get_target(self) -> str:
        if self.target is None:
            raise Exception("Target is not yet set")
        
        return self.target
    
    def get_current_char(self) -> str|None:
        if self.target is None:
            raise Exception("Target is not yet set")
        
        if self.index >= len(self.target):
            return None
        
        return self.target[self.index]
    
    def increase_index(self) -> None:
        self.index += 1 

    def decrease_index(self) -> None:
        if self.index == 0: 
            return
        
        self.index -= 1 

    def increase_total_typed(self) -> None:
        self.total_typed += 1 

    def increase_mistakes(self) -> None:
        self.wrong_count += 1 

    def get_index(self) -> int:
        return self.index
    
    def get_time_elapsed(self) -> float:
        if self.start_time is None or self.end_time is None:
            raise Exception("Cannot calculate time elapsed")
        
        return (self.end_time - self.start_time)
    
    def get_mistakes(self) -> int:
        return self.wrong_count
    
    def get_total_typed(self) -> int:
        return self.total_typed
    
    def get_net_wpm(self) -> float:
        elapsed = self.get_time_elapsed()
        correct_chars = self.total_typed - self.wrong_count
        return (correct_chars / MEAN_WORD_LENGTH) * (SECONDS_PER_MINUTE / elapsed)
    
    def process_char(self, char: str) -> None:
        if self.target is None:
            raise Exception("Target is not yet set")

        if char == BACKSPACE:
            self.decrease_index()
        
        self.increase_total_typed()

        expected_char = self.get_current_char() 

        if expected_char == char:
            self.increase_index()
        else:
            self.increase_mistakes()
    
    def draw(self, last_char: str | None = None) -> tuple[str, str]:
        passed = self.target[:self.index]
        leftover =self.target[self.index:]

        display = f"{GREEN_LETTERS}{passed}{RESET_LETTERS}{leftover}"
        pointer = " " * self.index + "↑"

        if (last_char 
            and not last_char == BACKSPACE 
            and not self.target_typed 
            and last_char != self.target[self.index-1]
        ):
            display = (
                f"{GREEN_LETTERS}{self.target[:self.index]}{RESET_LETTERS}"
                f"{RED_LETTERS}{last_char}{RESET_LETTERS}"
                f"{self.target[self.index:]}"
            )
            pointer = " " * (self.index+1) + "↑"

        return display, pointer


    @property
    def initialized(self) -> bool:
        return self.target is not None
    
    @property
    def target_typed(self) -> bool:
        return self.target is not None and self.index >= len(self.target)