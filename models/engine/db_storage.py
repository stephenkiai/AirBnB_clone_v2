#!/usr/bin/python3
"""module that defines a class to manage airbnb clone"""
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """defines a class storage"""
    __engine = None
    __session = None

    def __init__(self):
        """initializes the sql database storge"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER,
                                              HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST,
                                              HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)"""
        if cls is None:
            objs_query = self.__session.query(State).all()
            objs_query.extend(self.__session.query(City).all())
            objs_query.extend(self.__session.query(User).all())
            objs_query.extend(self.__session.query(Place).all())
            objs_query.extend(self.__session.query(Review).all())
            objs_query.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs_query = self.__session.query(cls)
        return {"{}.{}".format(type(objt).__name__, objt.id):
                objt for objt in objs_query}

    def new(self, obj):
        """add the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of current database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)
        (WARNING: all classes who inherit frm Base must imported before calling
        Base.metadata.create_all(engine))
        create the current database session (self.__session) from the engine
        (self.__engine)"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute """
        self.__session.close()
