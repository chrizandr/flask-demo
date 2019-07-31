"""Models for Hydra Classes."""
import pdb
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date
from passlib.hash import bcrypt
from sqlalchemy.orm import sessionmaker


DB_URL = 'sqlite:///database.db'
Base = declarative_base()
engine = create_engine(DB_URL)


class User(Base):
    """Model for Users.

    Each user has a username and password.
    """

    __tablename__ = "users"

    id_ = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(20))
    email = Column(String(100))

    def __init__(self, username, password, email):
        """Create new instance."""
        self.username = username
        self.password = bcrypt.encrypt(password)
        self.email = email

    def validate_password(self, password):
        """Check encrypted password."""
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        """Verbose object name."""
        return "<id='%s', username='%s'>" % (self.id_, self.username)


def setup(DB_URL):
    """Setup."""
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    session = setup(DB_URL)
    pdb.set_trace()
