from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()
engine = None
session = None


class RegionConfiguration(Base):
    __tablename__ = 'region_config'
    channel_id = Column(String(255), primary_key=True)
    region = Column(String(255))


engine = create_engine('sqlite:///dealbot_config.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)


def set_region(channel_id, region):
    session = scoped_session(sessionmaker(bind=engine))
    config = RegionConfiguration(channel_id=str(channel_id), region=str(region))
    session.merge(config)
    session.commit()


def get_region(channel_id):
    session = scoped_session(sessionmaker(bind=engine))
    result = session.query(RegionConfiguration).filter_by(channel_id=channel_id).first()
    if result is None:
        return "eu2"
    else:
        return result.region
