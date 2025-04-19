from sqlalchemy.ext.declarative import as_declarative, declared_attr

# Use as_declarative() to turn this class into a base for SQLAlchemy models.
@as_declarative()
class Base:
    # This class serves as the base for all database models.
    id: any
    __name__: str

    # Automatically generate the table name for each model.
    @declared_attr
    def __tablename__(cls) -> str:
        # The table name is the lowercase version of the model's class name.
        return cls.__name__.lower()