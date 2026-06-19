import logging
from staging import run_staging
from core import run_core

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

def main():
    run_staging()
    run_core()

if __name__ == '__main__':
    main()