from src.flib import sender , log
from config.config import sleeping_time_in_secs , debug_level
import time


def main():
    log('I`m started working')
    if debug_level == 1:
        print('| Starting |')
    while True:
        sender()
        time.sleep(sleeping_time_in_secs)
    
if __name__ == "__main__":
    main()