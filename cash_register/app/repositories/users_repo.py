from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from shared.database.exceptions import DatabaseError
from shared.database.logger import logger
from shared.database.models import User


class UsersRepository:
    """
    Repository for managing user data.

    Provides methods for creating and retrieving user accounts.
    Each user represents a customer in the supermarket system.

    Attributes:
        db: SQLAlchemy session for database operations
    """

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            Optional[User]: The user if found, None otherwise

        Raises:
            DatabaseError: If there's an error retrieving the user
        """
        try:
            user = self.db.get(User, user_id)
            return user
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving user {user_id}: {e}")
            raise DatabaseError(f"Failed to retrieve user: {e}")

    def create_user(self) -> User:
        """
        Create a new user account.

        Returns:
            User: The newly created user

        Raises:
            DatabaseError: If there's an error creating the user
        """
        user_id = uuid4()
        try:
            user = User(id=user_id)
            self.db.add(user)
            self.db.commit()
            logger.info(f"Created new user: {user_id}")
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error creating user {user_id}: {e}")
            raise DatabaseError(f"Failed to create user: {e}")

    def get_or_create_user(self, user_id: UUID = None) -> User:
        """
        Get an existing user or create a new one if it doesn't exist.

        Args:
            user_id: Optional user ID to look up or create

        Returns:
            User: The existing or newly created user

        Raises:
            DatabaseError: If there's an error creating the user
        """
        try:
            if user_id:
                user = self.get_user_by_id(user_id)
                if user:
                    return user
            else:
                user_id = uuid4()

            user = User(id=user_id)
            self.db.add(user)
            self.db.commit()
            logger.info(f"Created new user: {user_id}")
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error creating user {user_id}: {e}")
            raise DatabaseError(f"Failed to create user: {e}")
