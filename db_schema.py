"""
A simple module to define database models for a Travel Diary application.

This module uses SQLAlchemy to define and create database tables for storing
user information, their last activities, and their adventures.
"""
#pylint: disable=too-few-public-methods disable=import-error
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine("sqlite+pysqlite:///database.sqlite", echo=True)

class Base(DeclarativeBase):
    """Declarative Base for all mapped classes"""

class User(Base):
    """Mapped class that represents a user in the system."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

class LastActivity(Base):
    """Mapped class that tracks the last activity of a user."""

    __tablename__ = "last_activity"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey("user_account.id"))
    last_activity: Mapped[datetime] = mapped_column()

class Adventure(Base):
    """Mapped class that represents an adventure or activity undertaken by a user."""
    __tablename__ = "adventure"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey("user_account.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    destination_country: Mapped[str] = mapped_column(nullable=False)
    destination_city: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    experience: Mapped[str] = mapped_column(nullable=False)

class Image(Base):
    """Mapped class that represents an image that user supplied along with description of his adventure."""
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, autoincrement=True)
    adventure_id: Mapped[int] = mapped_column(ForeignKey("adventure.id"))
    image_data: Mapped[bytes] = mapped_column(nullable=False)
    image_title: Mapped[str] = mapped_column()

if __name__ == "__main__":

    """Implementation of CLI interface that allows to
    create and drop individual tables"""

    import sys
    option = sys.argv[1]
    table_name = sys.argv[2]
    
    if option == "-d":
        if table_name == "all":
            #Drop all tables
            Base.metadata.drop_all(engine)
        else:
            Base.metadata.tables[table_name].drop(engine)
    elif option == "-c":
        if table_name == "all":
            #Create all tables
            Base.metadata.create_all(engine)
        else:
            Base.metadata.tables[table_name].create(engine)
    else:
        print(f"Unknown option: {option}")
