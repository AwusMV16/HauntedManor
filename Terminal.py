import sys
import time

def typewrite(_word: str, delay: float = 0.04):
    for char in _word:
        sys.stdout.write(char)  
        sys.stdout.flush()  
        time.sleep(delay)
    print()

def hideCursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def showCursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()