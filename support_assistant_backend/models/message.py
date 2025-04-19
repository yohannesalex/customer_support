
import uuid
from datetime import datetime
# Import necessary SQLAlchemy components for column types, foreign keys, and relationships.
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
# Import the custom Base class for declarative models.
from support_assistant_backend.db.base_class import Base

# Define the Message database model inheriting from Base.
class Message(Base):
    # Define columns for the 'message' table.
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    is_ai = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define the foreign key relationship to the 'ticket' table.
    ticket_id = Column(PG_UUID(as_uuid=True), ForeignKey("ticket.id"))
    # Define the relationship back to the Ticket model.
    ticket = relationship("Ticket", back_populates="messages")