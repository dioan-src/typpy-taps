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
    
    @property
    def initialized(self) -> bool:
        return self.target is not None