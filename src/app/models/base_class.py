from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"


Base = declarative_base(cls=CustomBase)
