#-*- coding: utf-8 -*-

import settings
from sqlalchemy import (
    create_engine,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.SQLALCHEMY_DB_URI, echo=True)
Model = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
