#-*- coding: utf-8 -*-

import settings
from sqlalchemy import (
    create_engine,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *

#engine = create_engine(settings.SQLALCHEMY_DB_URI, echo=True)
engine = create_engine(settings.SQLALCHEMY_DB_URI, echo=False)
Model = declarative_base()

Session = sessionmaker(bind=engine)
session = scoped_session(Session)


from sqlalchemy.types import TypeDecorator, String
import json

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
