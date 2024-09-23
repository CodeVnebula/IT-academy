from database import Database
from library import Library

def main():
    db = Database()
    db.create_tables()
    library = Library(db, max_authors=500,
                      max_books=1000, add_new_entries=False)
    library.run()

if __name__ == "__main__":
    main()
    