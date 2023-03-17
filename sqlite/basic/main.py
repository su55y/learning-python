from hooks import DBHooks
from queries import *


db_hooks = DBHooks(file="test.db")
if not db_hooks.init_db([TB_COUNTRIES_SQL, TB_CAPITALS_SQL]):
    raise Exception("init db failed")
