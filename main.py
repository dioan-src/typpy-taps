import time
import sys
import tty
import termios

from type_enums import ENTER, BACKSPACE, CTRLC, ESC, CLEAR_TO_EOL, DEL

def getch():
    """Reads a single character from terminal (like _getch in C)"""
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

    sys.stdout.write(f'Type the following line: {CLEAR_TO_EOL}\n')

    sys.stdout.write("\033[s")  # save cursor at top of dynamic area
    sys.stdout.write(f"{target}{CLEAR_TO_EOL}\n")
    sys.stdout.write(f"↑{CLEAR_TO_EOL}\n")
    sys.stdout.flush()

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

            sys.stdout.write("\033[u")

            if char == BACKSPACE:
                if index>0:
                    index -= 1
                display_line = f"\033[32m{target[:index]}\033[0m{target[index:]}{CLEAR_TO_EOL}\n"
                pointer_line = (" " * index) + f"↑{CLEAR_TO_EOL}\n"
            elif expected_char == char:
                index += 1
                display_line = f"\033[32m{target[:index]}\033[0m{target[index:]}{CLEAR_TO_EOL}\n"
                pointer_position = index
                pointer_line = (" " * index) + f"↑{CLEAR_TO_EOL}\n"
            else:
                passed_portion = target[:index]
                leftover_portion = target[index:]
                wrong_count += 1
                display_line = (
                    f"\033[32m{passed_portion}\033[0m"+f"\033[31m{char}\033[0m"+f"{leftover_portion}{CLEAR_TO_EOL}\n"
                )
                pointer_line = (" " * (index+1)) + f"↑{CLEAR_TO_EOL}\n"

            sys.stdout.write(display_line)
            sys.stdout.write(pointer_line)
            sys.stdout.flush()

        except KeyboardInterrupt:
            break


    end_time = time.time()
    elapsed = end_time - start_time

    if success:
        print("\nDone!")
        print(f"Time: {elapsed:.2f}s")
        print(f"Wrong characters: {wrong_count}")
        print(f"Total typed: {total_typed}")
        print(f"Accuracy: {((total_typed - wrong_count) / total_typed) * 100:.2f}%")
    else:
        print("\nWell that absolutely sucked wtf")

if __name__ == "__main__":
    sentence = "The quick brown fox jumps over the lazy dog"
    typing_test(sentence)
