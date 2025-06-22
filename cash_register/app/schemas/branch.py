"""
Branch schemas for the cash_register application.

These schemas define the data structures for branch-related responses.
"""

from pydantic import BaseModel, ConfigDict


class BranchResponse(BaseModel):
    """
    Response schema for branch information.

    This schema represents a branch in the supermarket system.

    Attributes:
        id: Unique identifier for the branch
    """
    id: str
    model_config = ConfigDict(from_attributes=True)
