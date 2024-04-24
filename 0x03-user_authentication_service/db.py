#!/usr/bin/env python3
"""
DB module
"""


from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound as NoResultFound_ORM
from typing import Any, Optional

from user import User


Base = declarative_base()


class DB:
    """
    DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add new user to DB
        """
        num_user = self._session.query(func.max(User.id)).scalar()
        new_user_id = num_user + 1

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Any) -> Optional[User]:
        """
        THis method takes in arbitrary keyword args
        Returns first row found in users table as filtered by args
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound_ORM:
            raise NoResultFound
        except InvalidRequestError:
            raise
