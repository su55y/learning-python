from storage import Storage
from storage.db import MySQL

if __name__ == "__main__":
    storage = Storage(MySQL())
