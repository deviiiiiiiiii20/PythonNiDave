import time
import sys

def type_line(text, delay=0.10):
    for char in text:
        sys.stdout.write(char)
        time.sleep(delay)
    print()

lyrics = [
    "I hope that I can turn back the time",
    "To make it alright, alright",
]

for line in lyrics:
    type_line(line)
    time.sleep(0.5)

