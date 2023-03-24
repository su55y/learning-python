from database import Session
from contextlib import contextmanager


@contextmanager
def get_session(commit=True):
    s = Session()
    try:
        yield s
    except:
        s.rollback()
        raise
    else:
        if commit:
            s.commit()
    finally:
        s.close()
