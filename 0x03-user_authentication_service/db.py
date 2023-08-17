#!/usr/bin/env python3
"""DB module"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
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
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user to database"""
        user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs: dict) -> User:
        """Finc user by from the database by arbtrary keywords"""
        keys = []
        vals = []
        for k, v in kwargs.items():
            if hasattr(User, k):
                keys.append(getattr(User, k))
                vals.append(v)
            else:
                raise InvalidRequestError
        user = self._session.query(User).filter(
            tuple_(*keys).in_([tuple(vals)])).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user t othe database"""
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if hasattr(User, k) and v is not None:
                setattr(user, k, v)
            else:
                raise ValueError
        self._session.commit()
        return None
