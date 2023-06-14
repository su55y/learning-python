from ..storage import Storage
from ..storage.db import SQLite

if __name__ == "__main__":
    storage = Storage(SQLite())
