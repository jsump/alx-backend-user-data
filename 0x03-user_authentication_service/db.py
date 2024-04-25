#!/usr/bin/env python3
"""
DB module
"""


from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, InvalidRequestError
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
        user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(user)
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise ValueError("User email already exists")
        return user

    def find_user_by(self, **kwargs: Any) -> Optional[User]:
        """
        This method takes in arbitrary keyword args
        Returns first row found in users table as filtered by args
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound_ORM
            return user
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """
        This method updates user attributes
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            raise NoResultFound_ORM
        try:
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"Wrong attribute '{key}'")
                setattr(user, key, value)
            self._session.commit()
        except NoResultFound_ORM:
            raise NoResultFound_ORM
        
    def update_session_id(user_id: int, session_id: str) -> None:
        """
        Update session id method
        """
        pass
