# Library Database Project

This project is a SQLite3 database program that includes creating two tables: books and authors, generating random data, and providing querying functionalities.

## Features

- **Create Book and Author Tables** - Stores information about authors and books.
- **Random Data Generation** - Uses the `Faker` library to randomly generate 500 authors and 1000 books.
- **Book Queries** - Functions to:
  - Find the book with the most pages;
  - Calculate the average number of pages in books;
  - Find the youngest author;
  - List authors who don’t have any books yet.
- **Bonus Feature** - Find authors who have written more than 3 books.

## Installation

1. Make sure you have Python 3.x installed.
2. Install the required libraries:
    ```bash
    pip install faker
    ```
    ```bash
    pip install sqlalchemy
    ```
    

## Usage

1. To run the project, execute the `main.py` file:
    ```bash
    python main.py
    ```
2. Once the program starts, a menu will appear where you can:
    - Search for books with the most pages;
    - Get the average number of pages in books;
    - Find the youngest author;
    - Find authors who have not written any books;
    - Find authors with more than 3 books.

## Database

The database is stored in the `library.sqlite3` file, which is automatically created when the program runs.

## Logging
All the SQL statements executed by SQLAlchemy are saved into a file `Logs\sql_commands.log`

## Requirements

- Python 3.x
- [Faker Library](https://faker.readthedocs.io/en/master/)
- SQLAlchemy

## Author

This project was created as part of a Python homework assignment.
