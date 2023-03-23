from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

    # def init_db():


# engine = create_engine(getenv("DB_CONN_STR", "sqlite:///test.db"), echo=True)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

# @contextmanager
# def NewSession():
#     with Session(engine) as session:
#         session.begin()
#         try:
#             yield session
#         except:
#             session.rollback()
#             raise
#         else:
#             session.commit()
