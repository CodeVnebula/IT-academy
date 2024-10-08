import random
from datetime import datetime
from faker import Faker
from models import Author, Book
from utils import Utils
from sqlalchemy import func


class Library:
    def __init__(self, db, max_authors=500,
                 max_books=1000, add_new_entries=False):
        self.fake = Faker()
        self.max_authors = max_authors
        self.max_books = max_books
        self.db = db
        self.add_new_entries = add_new_entries
        self.__update_library()
        
    def __update_library(self):
        num_of_books = self.get_number_of_items_in_table(Book)
        num_of_authors = self.get_number_of_items_in_table(Author)
        if self.add_new_entries or \
            (num_of_authors < self.max_authors and
                num_of_books < self.max_books):
                self.__add_random_authors()
                self.__add_random_books()

    def __add_random_authors(self):
        with self.db.get_session() as session:
            for _ in range(self.max_authors):        
                author = Author(
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    birth_date=self.fake.date_of_birth(
                    minimum_age=10, maximum_age=200),
                    birth_place=self.fake.city()
                )
                session.add(author)

    def __add_random_books(self):
        with self.db.get_session() as session:
            authors = session.query(Author).all()
            for _ in range(self.max_books):
                author = random.choice(authors)
                author_birth_date = author.birth_date

                title = self.fake.sentence(nb_words=3)
                category = random.choice(Utils.get_book_categories())
                pages = random.randint(50, 1500)

                while True:
                    date_100_years_after = Utils.get_date_100_years_after(
                        author_birth_date)
                    publish_date = self.fake.date_between_dates(
                        date_start=author_birth_date,
                        date_end=date_100_years_after
                    )
                    if publish_date <= datetime.now().date():
                        break

                book = Book(
                    title=title,
                    category=category,
                    pages=pages,
                    publish_date=publish_date
                )

                book.authors.append(author)
                
                additional_authors = random.sample([a for a in authors
                                                    if a != author],
                                                   random.randint(0, 3))
                for additional_author in additional_authors:
                    book.authors.append(additional_author)
                    
                session.add(book)
      
    def get_number_of_items_in_table(self, model_class):
        with self.db.get_session() as session:
            return session.query(model_class).count()
    
    def get_books_with_most_pages(self):
        with self.db.get_session() as session:
            max_pages = session.query(Book.pages).order_by(Book.pages.desc())\
                .first()[0]
            books = session.query(Book).filter(Book.pages == max_pages).all()
            print(*books) 

    def get_average_pages(self):
        with self.db.get_session() as session:
            average_pages = session.query(func.avg(Book.pages)).scalar()
            print(average_pages)
        
    def get_youngest_authors(self):
        with self.db.get_session() as session:
            youngest_birth_date = session.query(func.max(Author.birth_date))\
                .scalar()
            youngest_authors = session.query(Author)\
                .filter(Author.birth_date == youngest_birth_date).all()
            print(*youngest_authors)
            
    def get_authors_with_no_books(self):
        with self.db.get_session() as session:
            authors_with_no_books = session.query(Author)\
                .filter(~Author.books.any()).all()
            print(*authors_with_no_books)      

    def get_authors_with_more_than_3_books(self):
        with self.db.get_session() as session:
            authors_with_more_than_3_books = session\
                .query(Author).join(Author.books)\
                .group_by(Author.id)\
                .having(func.count(Book.id) > 3).all()
            print(*authors_with_more_than_3_books)

    
    def run(self):
        print("___ Library details Management ___")
        
        while True:
            print("1. Get book/books with most pages")
            print("2. Get average pages")
            print("3. Get youngest author/authors")
            print("4. Get author/authors with no books")
            print("5. Get authors with more than 3 books")
            print("6. Get number of items in library")
            print("7. Exit")
            
            choice = input(">> ")
            
            if choice == '1':
                print("Book/books with most pages:")
                self.get_books_with_most_pages()
            elif choice == '2':
                print("Average pages:")
                self.get_average_pages()
            elif choice == '3':
                print("Youngest author/authors:")
                self.get_youngest_authors()
            elif choice == '4':
                print("Author/authors with no books:")
                self.get_authors_with_no_books()
            elif choice == '5':
                print("Authors with more than 3 books:")
                self.get_authors_with_more_than_3_books()
            elif choice == '6':
                print("Number of items in library:")
                print("Authors:", self.get_number_of_items_in_table(Author))
                print("Books:", self.get_number_of_items_in_table(Book))
            elif choice == '7':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
            
            print("---------------------------------------------\n")
