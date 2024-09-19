from datetime import datetime
import sqlite3
import random
from faker import Faker
from utils import Utils


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            birth_place TEXT NOT NULL
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            pages INTEGER NOT NULL,
            publish_date TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES author(id)
        )""")

    def close(self):
        self.conn.close()   
        
    def commit(self):
        self.conn.commit()
        
    def query(self, sql, params=None):
        if params:
            return self.cursor.execute(sql, params)
        return self.cursor.execute(sql)


class Author:
    def __init__(self, first_name, last_name, birth_date, birth_place):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.birth_place = birth_place
        
    def save(self, db: Database):
        sql = """INSERT INTO author (first_name, last_name, birth_date, birth_place)
                VALUES(?, ?, ?, ?)"""
        params = (self.first_name, self.last_name, self.birth_date, self.birth_place)
        db.query(sql, params)


class Book:
    def __init__(self, title, category, pages, publish_date, author_id):
        self.title = title
        self.category = category
        self.pages = pages
        self.publish_date = publish_date
        self.author_id = author_id
    
    def save(self, db: Database):
        sql = """INSERT INTO book (title, category, pages, publish_date, author_id) 
                 VALUES (?, ?, ?, ?, ?)"""
        params = (self.title, self.category, self.pages, self.publish_date, self.author_id)
        db.query(sql, params)
        
class Library:
    def __init__(self, db: Database, number_of_authors=500, number_of_books=1000, add_new_entries=False):
        self.db = db
        self.fake = Faker()
        self.number_of_authors = number_of_authors
        self.number_of_books = number_of_books
        self.add_new_entries = add_new_entries
        self.__update_library()
        
    def __update_library(self):
        num_of_books = self.get_number_of_items_in_table('book')
        num_of_authors = self.get_number_of_items_in_table('author')
        if self.add_new_entries or \
            (num_of_authors < self.number_of_authors and
                num_of_books < self.number_of_books):
                self.__add_random_authors()
                self.__add_random_books()
        
    def __add_random_authors(self):
        for _ in range(self.number_of_authors):        
            author = Author(
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
                # Suppose we got books of authors from past 200 years
                birth_date=self.fake.date_of_birth(minimum_age=10, maximum_age=200).strftime("%Y-%m-%d"),
                birth_place=self.fake.city()
            )
            author.save(self.db)
            
    def __add_random_books(self):
        authors = self.db.query("SELECT id, birth_date FROM author").fetchall()
        book_categories = Utils.get_book_categories()
        
        for _ in range(self.number_of_books):
            random_tuple = random.choice(authors)
            author_birth_date = random_tuple[1]
            
            title=self.fake.sentence(nb_words=3)
            category=random.choice(book_categories)
            pages=random.randint(50, 1500)
            
            while True:
                date_100_years_after = Utils.get_date_100_years_after(author_birth_date)
                publish_date = self.fake.date_between_dates(datetime.strptime(author_birth_date, "%Y-%m-%d").date(), date_100_years_after)
                if publish_date <= datetime.now().date():
                    author_id = random_tuple[0]
                    break
            
            book = Book(
                title=title,
                category=category,
                pages=pages,
                publish_date=publish_date.strftime("%Y-%m-%d"),
                author_id=author_id
            )
            
            book.save(self.db)
        
    def get_books_with_most_pages(self, fetch_function):
        results = fetch_function(self.db.query("SELECT * FROM book WHERE pages = (SELECT MAX(pages) FROM book)"))
        return results        

    def get_average_pages(self, fractional_digits=2):
        result = self.db.query("SELECT AVG(pages) FROM book").fetchone()
        
        if result and result[0] is not None:
            average_pages = f'{result[0]:.{fractional_digits}f}'
        else:
            average_pages = f'0.{"0" * fractional_digits}'
        
        return average_pages
    
    def get_youngest_authors(self, fetch_function):
        youngest_birth_date = self.db.query(
            'SELECT MAX(birth_date) FROM author'
        ).fetchone()[0]
        if youngest_birth_date:
            query = 'SELECT * FROM author WHERE birth_date = ?'
            results = fetch_function(self.db.query(query, (youngest_birth_date,)))
            return results

    def get_authors_with_no_books(self, fetch_function):
        results = fetch_function(self.db.query(
            "SELECT * FROM author WHERE id NOT IN (SELECT author_id FROM book)"
        ))
        return results

    def get_authors_with_3_plus_books(self, fetch_function):
        author_ids = fetch_function(self.db.query("SELECT author_id FROM book GROUP BY author_id HAVING COUNT(*) > 3"))
        if isinstance(author_ids, list) and isinstance(author_ids[0], tuple):
            results = tuple(
                self.db.query("SELECT * FROM author WHERE id = ?", (author_id[0],)).fetchone()
                for author_id in author_ids
            )
        else:
            result = self.db.query("SELECT * FROM author WHERE id = ?", (author_ids[0],)).fetchone()
            results = result if result else ()
        return results 

    def get_number_of_items_in_table(self, table_name):
        query = f"SELECT COUNT(*) FROM {table_name}"
        return self.db.query(query).fetchone()[0]
