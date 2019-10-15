from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import config

engine = create_engine(config.POSTGRES_URI, pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
