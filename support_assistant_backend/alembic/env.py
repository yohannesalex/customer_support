from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from alembic import context
import asyncio
import os
from core.config import settings

# This is the Alembic Config object
config = context.config

# Set database URL from environment variable
db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
config.set_main_option("sqlalchemy.url", db_url)

# Import your Base and models
# Add this before target_metadata = Base.metadata
import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(abspath(__file__))))

# Make sure this imports your actual Base and models
from db.base_class import Base
from models.users import User  # Explicit importtarget_metadata = Base.metadata
target_metadata = Base.metadata

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' (async) mode."""
    connectable = create_async_engine(db_url)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())