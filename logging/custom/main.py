from sys import exit
from utils.custom_logger import logger 

def div(x, y):
    if not all(isinstance(arg, (int, float)) for arg in [x, y]):
        logger.warning("x or y are not number, now something is going to happen")

    logger.debug(f"try {x} / {y}")
    try:
        print(f"{x} / {y} = {x / y}")
    except TypeError as e:
        logger.error(f"can't divide {x} by {y}: {e}")
    except ZeroDivisionError as e:
        logger.critical(f"can't divide {x} by {y}: {e}")
        exit(1)

def main(): 
    div(0, "\U0001F43C")
    div(1, 0)
    logger.info("done")
    exit(0)

if __name__ == "__main__":
    main()
