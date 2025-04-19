import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
# Import the custom Base class.
from support_assistant_backend.db.base_class import Base

# Define the User database model inheriting from Base.
class User(Base):
    __tablename__ = 'users'
    # Define columns for the 'user' table.
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

    # Define the relationship back to the Ticket model.
    tickets = relationship("Ticket", back_populates="user")