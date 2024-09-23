from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import Utils
from models import Base
from logger import setup_sql_logging

class Database:
    def __init__(self):
        setup_sql_logging(Utils.get_log_path(file_name='sql_commands.log'))
        self.engine = create_engine(
            f'sqlite:///{Utils.get_db_path()}', echo=False)
        self.Session = sessionmaker(bind=self.engine)  
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    @contextmanager
    def get_session(self):
        session = self.Session() 
        try:
            yield session
            session.commit() 
        except:
            session.rollback()
            raise  
        finally:
            session.close()  
    
    def add_all(self, objs):
        with self.get_session() as session:
            session.add_all(objs)  
    
    def add(self, obj):
        with self.get_session() as session:
            session.add(obj) 
