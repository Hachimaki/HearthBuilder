from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine('sqlite:///relations.db')


def new_session() -> Session:
    """
    # create a configured "Session" class
    Session = sessionmaker(bind=some_engine)

    # create a Session
    session = Session()

    :return: Returns a session instance
    """
    return sessionmaker(bind=engine)()


from .deck_item import *

Base.metadata.create_all(engine)
