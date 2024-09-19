import textwrap
from library import Database, Library
from utils import Utils

class RunScript:
    def __init__(self, max_number_of_authors, max_number_of_books, add_new_entries):
        self.max_number_of_authors = max_number_of_authors
        self.max_number_of_books = max_number_of_books
        self.add_new_entries = add_new_entries
        self.db_path = Utils.get_db_path()
        self.db = Database(self.db_path)
        self.db.create_tables()
        self.library = Library(self.db, self.max_number_of_authors, self.max_number_of_books, self.add_new_entries)
        self.db.commit()
        
    def run(self):        
        print("___Library details Management___\n")
        
        while True:
            print("1. Get book/books with most pages")
            print("2. Get average pages")
            print("3. Get youngest author/authors")
            print("4. Get author/authors with no books")
            print("5. Get authors with more than 3 books")
            print("6. Get number of items in library")
            print("7. Exit")
            
            choice = int(input(">> "))
            
            if choice == 1:
                print("Fetch one or all?")
                print("1. One")
                print("2. All")
                fetch_choice = input(">> ")
                if fetch_choice == "1":
                    data = self.library.get_books_with_most_pages(lambda cursor: cursor.fetchone())
                    print("__ Book with most pages __\n")
                elif fetch_choice == "2":
                    data = self.library.get_books_with_most_pages(lambda cursor: cursor.fetchall())
                    print("__ Books with most pages __\n")
                else:
                    print("Invalid choice, fetching one by default.")
                    data = self.library.get_books_with_most_pages(lambda cursor: cursor.fetchone())
                    print("__ Book with most pages __")
                
                self.__print_data(data, 'book') 
                self.__print_line() 
                    
            elif choice == 2:
                print("How many decimal places would you like to include?")
                print("1. 1 decimal places")
                print("2. 2 (default) decimal places")
                print("3. 3 decimal places")
                print("4. 4 decimal places")
                print("5. Custom (enter your own number)")
                decimal_places = int(input(">> "))
                if decimal_places == 1:
                    average_pages = self.library.get_average_pages(fractional_digits=1)
                elif decimal_places == 2:
                    average_pages = self.library.get_average_pages()
                elif decimal_places == 3:
                    average_pages = self.library.get_average_pages(fractional_digits=3)
                elif decimal_places == 4:
                    average_pages = self.library.get_average_pages(fractional_digits=4)
                elif decimal_places == 5:
                    custom_decimal_places = int(input("Enter the number of decimal places: "))
                    average_pages = self.library.get_average_pages(fractional_digits=custom_decimal_places)
                else:
                    print("Invalid choice, defaulting to 2 decimal places.")
                    average_pages = self.library.get_average_pages()
                
                print(f"Average Pages: {average_pages}")
                self.__print_line()
                
            elif choice == 3:
                print("Fetch one or all?")
                print("1. One")
                print("2. All")
                fetch_choice = input(">> ")
                if fetch_choice == "1":
                    data = self.library.get_youngest_authors(lambda cursor: cursor.fetchone())
                    print("__ Youngest Author __\n")
                elif fetch_choice == "2":
                    data = self.library.get_youngest_authors(lambda cursor: cursor.fetchall())
                    print("__ Youngest Authors __\n")
                else:
                    print("Invalid choice, fetching one by default.")
                    data = self.library.get_youngest_authors(lambda cursor: cursor.fetchone())
                    print("__ Youngest Author __")
                
                self.__print_data(data, 'author')
                self.__print_line()
                    
            elif choice == 4:
                print("Fetch one or all?")
                print("1. One")
                print("2. All")
                fetch_choice = input(">> ")
                if fetch_choice == "1":
                    data = self.library.get_authors_with_no_books(lambda cursor: cursor.fetchone())
                    print("__ Author with no books __")
                elif fetch_choice == "2":
                    data = self.library.get_authors_with_no_books(lambda cursor: cursor.fetchall())
                    print("__ Authors with no books __")
                else:
                    print("Invalid choice, fetching one by default.")
                    data = self.library.get_authors_with_no_books(lambda cursor: cursor.fetchone())
                    print("__ Author with no books __")
                self.__print_data(data, 'author')
                self.__print_line()
                
            elif choice == 5:
                print("Fetch one or all?")
                print("1. One")
                print("2. All")
                fetch_choice = input(">> ")
                if fetch_choice == "1":
                    data = self.library.get_authors_with_3_plus_books(lambda cursor: cursor.fetchone())
                    print("__ Author with more than 3 books __")
                elif fetch_choice == "2":
                    data = self.library.get_authors_with_3_plus_books(lambda cursor: cursor.fetchall())
                    print("__ Authors with more than 3 books __")
                else:
                    print("Invalid choice, fetching one by default.")
                    data = self.library.get_authors_with_3_plus_books(lambda cursor: cursor.fetchone())
                    print("__ Author with more than 3 books __")
                self.__print_data(data, 'author')
                self.__print_line()
                
            elif choice == 6:
                print("1. Get number of Books")
                print("2. Get number of authors")
                user_choice = input(">> ")
                if user_choice == '1':
                    result = self.library.get_number_of_items_in_table('book')
                    print(f" -- Number of books in library: {result}")
                elif user_choice == '2':
                    result = self.library.get_number_of_items_in_table('author')
                    print(f" -- Number of authors in library: {result}")
                else:
                    print("Invalid choice, returning number of books by default.")
                    result = self.library.get_number_of_items_in_table('book')
                    print(f" -- Number of books in library: {result}")
            
            elif choice == 7:
                break
            else:
                print("Invalid choice")

        self.db.close()
    
    @staticmethod
    def __print_line():
        print("------------------------------------------------")

    @staticmethod
    def __print_data(data, table):
        if table == 'book':
            book_details_str = textwrap.dedent("""
                                               - Book ID: {book_id}
                                               - Title: {title}
                                               - Category: {category}
                                               - Pages: {pages}
                                               - Publish date: {publish_date}
                                               - Author ID: {author_id}""")
            if isinstance(data, list) and isinstance(data[0], tuple):
                for each_tuple in data:
                    formatted_str = book_details_str.format(book_id=each_tuple[0], title=each_tuple[1], 
                                            category=each_tuple[2], pages=each_tuple[3], 
                                            publish_date=each_tuple[4], author_id=each_tuple[-1])
                    print(formatted_str)
            elif isinstance(data, tuple) and isinstance(data[0], int):
                    formatted_str = book_details_str.format(book_id=data[0], title=data[1], category=data[2], 
                                            pages=data[3], publish_date=data[4], author_id=data[-1])
                    print(formatted_str)
        
        if table == 'author':
            author_details_str = textwrap.dedent("""
                                                 - Author ID: {author_id}
                                                 - First name: {first_name}
                                                 - Last name: {last_name}
                                                 - Birth date: {birth_date}
                                                 - Birth place: {birth_place}""")
            if (isinstance(data, list) or isinstance(data, tuple)) and \
                isinstance(data[0], tuple):
                for each_tuple in data:
                    formatted_str = author_details_str.format(author_id=each_tuple[0], first_name=each_tuple[1], 
                                            last_name=each_tuple[2], birth_date=each_tuple[3], 
                                            birth_place=each_tuple[-1])
                    print(formatted_str)
                    
            elif isinstance(data, tuple) and isinstance(data[0], int):
                formatted_str = author_details_str.format(author_id=data[0], first_name=data[1], 
                                    last_name=data[2], birth_date=data[3], birth_place=data[-1])
                print(formatted_str)
