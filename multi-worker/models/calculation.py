from sqlalchemy import Column
from sqlalchemy import Integer
# from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import create_engine
# metadata_obj = MetaData()

Base = declarative_base()

class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)

    def __repr__(self):
        return f"Calculation(id={self.id!r}, x={self.x!r}, y={self.y!r})"

# def init_calculations_db():
#     engine = create_engine("sqlite://", echo=True, future=True)
#     calculations_table = Table('calculations', )
#     engine = create_engine("sqlite://", echo=True, future=True)
engine = create_engine("sqlite://", echo=True, future=True)
Base.metadata.create_all(engine)