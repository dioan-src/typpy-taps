import time
from data.sentences import get_random_sentence, SentenceSize
from typing import Optional
import curses

class BaseMode:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        # self.engine = TypingEngine() # The timer/WPM logic
        self.target_text: Optional[str] = None
        self.typed_text = ""
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.duration: Optional[int] = None
        self.errors = 0

    def load_text(self):
        """Each mode overrides this to get text from different places"""
        raise NotImplementedError

    def is_running(self):
        """Override this to define win/loss conditions"""
        raise NotImplementedError
    
    def is_time_up(self) -> bool:
        if self.duration is None:
            return False
        if self.start_time is None:
            raise Exception('Game Has Not Yet Started')
        return (time.time() - self.start_time) >= self.duration

    def get_time_remaining(self) -> int:
        if self.duration is None: return 0
        elapsed = time.time() - self.start_time
        return max(0, int(self.duration - elapsed))

    def setup(self):
        self.load_text()

        if self.target_text is None:
            raise Exception('Target has not been set')

    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

    def run(self):
        """The Shared Game Loop: All modes use this logic"""
        self.setup()

        # Shared Countdown logic
        for i in range(3, 0, -1):
            self.stdscr.clear()
            self.stdscr.addstr(3, 5, f"Game starting in {i}...")
            self.stdscr.addstr(5, 5, self.target_text, curses.A_DIM)
            self.stdscr.refresh()
            curses.napms(1000)

        self.start()

        # Main Typing Loop
        while self.is_running():
            if self.is_time_up():
                break

            self.draw_frame()
            
            # Use a short timeout for getkey so the clock can update 
            # even if the user isn't typing
            self.stdscr.timeout(100) 
            try:
                key = self.stdscr.getkey()
                self.handle_input(key)
            except curses.error:
                continue # No key pressed within 100ms

    def draw_frame(self):
        """Handles the rendering logic for the typing area"""
        self.stdscr.clear()
        # Draw target text as background
        self.stdscr.addstr(5, 5, self.target_text, curses.A_DIM)
        
        # Draw typed text with colors
        for i, char in enumerate(self.typed_text):
            if i < len(self.target_text):
                color = curses.color_pair(1) if char == self.target_text[i] else curses.color_pair(2)
                self.stdscr.addstr(5, 5 + i, char, color)
        
        self.stdscr.refresh()

    def handle_input(self, key):
        """Standard input handling"""
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            self.typed_text = self.typed_text[:-1]
        elif len(key) == 1:

            current_index = len(self.typed_text)
            if current_index < len(self.target_text):
                if key != self.target_text[current_index]:
                    self.errors += 1

            self.typed_text += key

class ClassicMode(BaseMode):
    def load_text(self):
        self.target_text = get_random_sentence(SentenceSize.SMALL)

    def is_running(self):
        return len(self.typed_text) < len(self.target_text)

class RaceMode(BaseMode):

    def setup(self):
        super().setup()
        self.duration = 10

    def load_text(self):
        self.target_text = get_random_sentence(SentenceSize.SMALL)

    def is_running(self):
        return (len(self.typed_text) < len(self.target_text)) and not self.is_time_up()

    def draw_frame(self):
        super().draw_frame()
        
        # Add a timer display at the top
        remaining = self.get_time_remaining()
        color = curses.color_pair(2) if remaining < 3 else curses.A_BOLD
        self.stdscr.addstr(1, 5, f"TIME REMAINING: {remaining}s", color)
        self.stdscr.refresh()

class PerfectionistMode(BaseMode):
    def load_text(self):
        self.target_text = get_random_sentence(SentenceSize.SMALL)
        
    def is_running(self):
        return (len(self.typed_text) < len(self.target_text)) and self.errors == 0

# class ChillMode(BaseMode):
#     # no timer. no target. unlimited mode. until you drop
#     def setup(self): pass
#     def update(self): pass
#     def draw(self): pass
