from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from cash_register.app.logger import logger
from cash_register.app.repositories.branch_repo import BranchRepository
from cash_register.app.schemas.branch import BranchResponse
from shared.database.exceptions import DatabaseError


class BranchService:
    """
    Service for managing supermarket branches.

    Provides business logic for branch operations in the supermarket system.

    Attributes:
        db: SQLAlchemy session for database operations
        repo: Repository for branch operations
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = BranchRepository(db)

    def list_branches(self) -> List[BranchResponse]:
        """
        Retrieve all branches in the system.

        Returns:
            List of branches with their IDs

        Raises:
            DatabaseError: If there's an error retrieving branches
        """
        try:
            branches = self.repo.get_branches()
            logger.info(f"Retrieved {len(branches)} branches")

            return [BranchResponse(id=branch.id) for branch in branches]
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving branches: {e}")
            raise DatabaseError(f"Failed to retrieve branches: {e}")
