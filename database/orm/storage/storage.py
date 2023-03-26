from database import Session
from contextlib import contextmanager


@contextmanager
def get_session(commit=True):
    s = Session()
    try:
        yield s
        if commit:
            s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()
