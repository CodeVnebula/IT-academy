from datetime import datetime
from pathlib import Path


class Utils:
    @staticmethod
    def get_db_path():
        script_dir = Path(__file__).parent
        return script_dir / 'library.sqlite3'

    @staticmethod
    def get_book_categories():
        book_categories = [
            "Fiction",
            "Literary Fiction",
            "Science Fiction",
            "Fantasy",
            "Mystery",
            "Thriller",
            "Historical Fiction",
            "Romance",
            "Horror",
            "Adventure",
            "Dystopian",
            "Magical Realism",
            "Graphic Novels",
            "Short Stories",
            "Non-fiction",
            "Biographies",
            "Autobiographies",
            "Memoirs",
            "Self-help",
            "Motivational",
            "Philosophy",
            "Psychology",
            "Sociology",
            "True Crime",
            "Political Science",
            "History",
            "Travel",
            "Science",
            "Technology",
            "Mathematics",
            "Economics",
            "Business",
            "Personal Finance",
            "Health",
            "Fitness",
            "Cookbooks",
            "Art",
            "Photography",
            "Music",
            "Poetry",
            "Religion",
            "Spirituality",
            "Education",
            "Textbooks",
            "Parenting",
            "Law",
            "Linguistics",
            "Anthropology",
            "Essays",
            "Humor",
            "Crafts",
            "Home Improvement",
            "Gardening",
            "Sports",
            "Politics",
            "Environment",
            "Medical",
            "Journalism",
            "Social Media",
            "Programming",
            "Engineering",
            "Astronomy",
            "Architecture"
        ]
        return book_categories

    @staticmethod
    def get_date_100_years_after(date_str):
        date_format = "%Y-%m-%d"
        
        date = datetime.strptime(date_str, date_format).date()
        
        try:
            date_plus_100_years = date.replace(year=date.year + 100)
        except ValueError:
            date_plus_100_years = date.replace(year=date.year + 100, day=date.day - 1)
        
        return date_plus_100_years
    