from datetime import datetime

import db
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


DATABASE_URI = 'sqlite:///app.db'    # const не можна перезаписувати, сюди  вказуємо шдях до нашої БД


engine = create_engine(DATABASE_URI) # обєкт який відповідає за підключення до БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    db = SessionLocal()             #  створюємо обєкт
    try:
        yield db                    # db генерує повертає обєкт дб
    finally:
        db.close()



class ModelMetaDatesMixin(Base):    # розширити функціонал іншого Mixin

    __abstract__ = True             # ми не додаємо цей модуль в бд, але наслідуємо його в інших. Не дістаємо дані звідси і тд

    start_at = Column(DateTime, default=datetime.utcnow)
    end_at = Column(DateTime, default=datetime.utcnow)





class Tour(Base):
    __tablename__ = 'tour'          # як буде називатись табл в SQl

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = Column(DateTime, nullable=False)



class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True, nullable=False)
    user = relationship("User", backref="admin")