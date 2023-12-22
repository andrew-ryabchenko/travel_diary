"""This module provides functionalities for user authentication, 
registration, and managing adventure entries using SQLAlchemy.

It includes functions for checking login credentials, adding new users, 
adding adventure entries, and retrieving user information and adventure entries."""
#pylint: disable=too-many-arguments disable=import-error
import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from db_schema import User, Adventure, engine

def sha256_hash(object: str):
    sha256 = hashlib.sha256(bytes(object, encoding="utf-8"))
    return sha256.hexdigest()

def check_login_credentials(username: str, password: str) -> int | None:
    """Verify user login credentials."""

    password_hash = sha256_hash(password)
    with Session(engine) as session:
        user = session.query(User).filter(User.username == username,
                                          User.password_hash == password_hash).first()
        if user:
            return user.id

        return None

def add_user(username: str, password: str) -> None:
    """Add a new user to the database."""

    sha256 = hashlib.sha256(bytes(password, encoding="utf-8"))
    password_hash = sha256.hexdigest()
    user = User(id=None, username=username, password_hash=password_hash)
    with Session(engine) as session:
        session.add(user)
        session.flush()
        session.commit()

def add_entry(user_id: int, title: str,  country: str, city: str,
              date: datetime, experience: str) -> None:
    """Add a new adventure entry for a user."""

    adventure = Adventure(id=None, user_id=user_id, title=title, destination_country=country,
                          destination_city=city, date=date, experience=experience)
    with Session(engine) as session:
        session.add(adventure)
        session.flush()
        session.commit()

def retrieve_user(user_id) -> User | None:
    """Retrieve a user's details from the database."""

    user = None
    with Session(engine) as session:
        user = session.get(User, user_id)
    return user

def retrieve_entries(user_id, number: int = None) -> [Adventure]:
    """Retrieve adventure entries for a user."""

    with Session(engine) as session:
        if not number:
            results = session.query(Adventure).filter(Adventure.user_id == user_id).all()
            return results
        results = session.query(Adventure).filter(Adventure.user_id == user_id).limit(number)
        return results

def retrieve_entry(adventure_id: int) -> Adventure:
    """Retrieve a specific adventure entry."""

    with Session(engine) as session:
        adventure = session.get(Adventure, adventure_id)
        return adventure

def entry_count(user_id):
    with Session(engine) as session:
        count = session.execute(text("select count(*) from adventure where user_id = :id").bindparams(id=user_id)).first()
        return count[0]

def check_password(user_id: int, password: str):
    password_hash = sha256_hash(password)
    with Session(engine) as session:
        user_table = User.__table__
        user = session.execute(select(user_table).where(user_table.c.id == user_id).where(user_table.c.password_hash == password_hash)).first()
        if user:
            return True
        return False

def change_password(user_id: int, old_password: str, new_password: str) -> bool:
    new_password_hash = sha256_hash(new_password)
    with Session(engine) as session:
        valid = check_password(user_id, old_password)
       
        if not valid:
            return False
        
        user = session.get(User, user_id)
        user.password_hash = new_password_hash

        session.flush()
        session.commit()

        return  True

def check_passwd_comp(passwd: str) -> bool:
    """Checks if password string matches 
    the required complexity"""
    num = False
    spec = False
    upper = False
    lower = False
    for c in passwd:
        if 65 <= ord(c) <= 90:
            upper = True
            continue
        if 97 <= ord(c) <= 122:
            lower = True
            continue
        if 48 <= ord(c) <= 57:
            num = True
            continue
        if 33 <= ord(c) <= 47:
            spec = True
            continue

    return len(passwd) >= 12 and num and spec and upper and lower
