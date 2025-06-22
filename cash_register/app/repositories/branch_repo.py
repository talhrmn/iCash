from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from shared.database.exceptions import DatabaseError
from shared.database.logger import logger
from shared.database.models import Branch


class BranchRepository:
    """
    Repository for managing supermarket branch data.

    Provides methods for creating, retrieving, and managing supermarket branches.
    Each branch represents a physical location of the supermarket.

    Attributes:
        db: SQLAlchemy session for database operations
    """

    def __init__(self, db: Session):
        self.db = db

    def get_branches(self) -> List[Branch]:
        """
        Retrieve all supermarket branches.

        Returns:
            List[Branch]: List of all branches in the system

        Raises:
            DatabaseError: If there's an error retrieving branches
        """
        try:
            stmt = select(Branch)
            result = self.db.execute(stmt)
            branches = result.scalars().all()
            logger.info(f"Retrieved {len(branches)} branches")
            return branches
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving branches: {e}")
            raise DatabaseError(f"Failed to retrieve branches: {e}")

    def get_branch_by_id(self, branch_id: str) -> Optional[Branch]:
        """
        Retrieve a branch by its ID.

        Args:
            branch_id: Unique identifier for the branch

        Returns:
            Optional[Branch]: The branch if found, None otherwise

        Raises:
            DatabaseError: If there's an error retrieving the branch
        """
        try:
            branch = self.db.get(Branch, branch_id)
            if not branch:
                logger.warning(f"Branch not found: {branch_id}")
                return None
            return branch
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving branch {branch_id}: {e}")
            raise DatabaseError(f"Failed to retrieve branch: {e}")

    def get_or_create_branch(self, branch_id: str) -> Branch:
        """
        Get an existing branch or create a new one if it doesn't exist.

        Args:
            branch_id: Unique identifier for the branch

        Returns:
            Branch: The existing or newly created branch

        Raises:
            DatabaseError: If there's an error creating the branch
        """
        try:
            existing = self.get_branch_by_id(branch_id)
            if existing:
                return existing

            branch = Branch(id=branch_id)
            self.db.add(branch)
            self.db.commit()
            logger.info(f"Created new branch: {branch_id}")
            return branch
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error creating branch {branch_id}: {e}")
            raise DatabaseError(f"Failed to create branch: {e}")
