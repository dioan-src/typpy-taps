from __future__ import annotations
import time
from typing import Optional


from data.sentences import SentenceSize, get_random_sentence

class Game:
    def __init__(self) -> None:
        self.size: SentenceSize = None
        self.target: Optional[str] = None
        self.index: int = 0
        self.wrong_count: int = 0
        self.total_typed: int = 0
        self.success: bool = False
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

    def set_result(self) -> None:
        self.success = self.index >= len(self.target)

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
    
    def is_won(self) -> bool:
        return self.success
    
    @property
    def initialized(self) -> bool:
        return self.target is not None
    
    @property
    def finished(self) -> bool:
        return self.target is not None and self.target >= len(self.target)