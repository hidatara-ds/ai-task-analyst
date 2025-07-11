import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# Base class for SQLAlchemy ORM
Base = declarative_base()


# Singleton implementation, following FastAPI implementation that needs yielding connections for dependency injection
class DatabaseSessionManager:
    """
    Manages the database connection and session lifecycle.
    Implements a singleton pattern to ensure only one instance is used.
    """

    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        """
        Initializes the database engine and sessionmaker.
        """
        # Create an asynchronous engine with connection recycling
        self._engine = create_async_engine(
            host, pool_recycle=1800
        )  # Recycle connections every 30 minutes, otherwise it will die and throw error
        # Create a sessionmaker bound to the engine
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        """
        Closes the database engine and resets the engine and sessionmaker.
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        # Dispose of the engine and reset engine and sessionmaker to None
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Provides a connection to the database within a context manager.
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Provides a session to the database within a context manager.
        """
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        # Create a new session from the sessionmaker
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # This is to be used in tests, as we will be creating and dropping to test stuff
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


# Instantiate the singleton DatabaseSessionManager
sessionmanager = DatabaseSessionManager()


# This function will be used to manage the dependency injection of the database session
async def get_db():
    """
    Dependency function to provide a database session.
    """
    # Use the session context manager to provide a session
    async with sessionmanager.session() as session:
        yield session
