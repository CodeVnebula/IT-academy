import textwrap
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

author_book = Table('author_book', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('book_id', Integer, ForeignKey('book.id'))
)

class Author(Base):
    __tablename__ = 'author'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)
    
    books = relationship('Book',
                         secondary=author_book,
                         back_populates='authors')
    
    def __init__(self, first_name, last_name, birth_date, birth_place):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.birth_place = birth_place
        
    def __repr__(self):
        return textwrap.dedent(f""" 
                                - First name = {self.first_name}
                                - Last name = {self.last_name}
                                - Birth date = {self.birth_date}
                                - Birth place = {self.birth_place}
                               """)


class Book(Base):
    __tablename__ = 'book'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    pages = Column(Integer)
    publish_date = Column(Date)
    
    authors = relationship('Author',
                           secondary=author_book,
                           back_populates='books')
    
    def __init__(self, title, category, pages, publish_date):
        self.title = title
        self.category = category
        self.pages = pages
        self.publish_date = publish_date
    
    def __repr__(self):
        return textwrap.dedent(f"""
                                - Title = {self.title}
                                - Pages = {self.pages}
                                - Category = {self.category}
                                - Publish date = {self.publish_date}
                               """)
    