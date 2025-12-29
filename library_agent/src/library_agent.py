import json
from pathlib import Path
import requests

class LibraryAgent:

    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.books = self.load_books()


    def load_books(self):
        if not self.data_path.exists():
            return []
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_books(self):
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.books, f, indent=2)

    def add_book(self, title, authors, category, year, rating=0, matched=False):
        book = {
            "title": title,
            "authors": authors,
            "category": category,
            "year": year,
            "rating": rating,
            "matched": matched
        }
        self.books.append(book)
        self.save_books()

    def list_books(self):
        return self.books

    def search_by_title(self, title):
        return [
            book for book in self.books
            if title.lower() in book["title"].lower()
        ]

    def search_by_author(self, author):
        return [
            book for book in self.books
            if any(author.lower() in a.lower() for a in book["authors"])
        ]

    def search_by_category(self, category):
        return [
            book for book in self.books
            if category.lower() in book["category"].lower()
        ]

    def recommend(self, min_rating=4):
        return [
            book for book in self.books
            if book["rating"] >= min_rating
        ]

    # ---------- External API ----------
    def fetch_book_details(self, title):
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": title}

        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            return None

        data = response.json()
        if "items" not in data:
            return None

        info = data["items"][0]["volumeInfo"]

        return {
            "title": info.get("title", "Unknown"),
            "authors": info.get("authors", []),
            "category": ", ".join(info.get("categories", [])),
            "year": int(info.get("publishedDate", "0")[:4] or 0),
            "rating": info.get("averageRating", 0),
            "matched": True
        }

if __name__ == "__main__":
    agent = LibraryAgent("data/books.json")

    while True:
        print("\n1. Add Book Manually")
        print("2. Add Book via API")
        print("3. List Books")
        print("4. Search by Title")
        print("5. Search by Author")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            authors = input("Authors (comma separated): ").split(",")
            category = input("Category: ")
            year = int(input("Year: "))
            agent.add_book(title, authors, category, year)

        elif choice == "2":
            title = input("Enter book name: ")
            book = agent.fetch_book_details(title)
            if book:
                agent.add_book(**book)
                print("Book added from API")
            else:
                print("Book not found")

        elif choice == "3":
            for book in agent.list_books():
                print(book)

        elif choice == "4":
            title = input("Search title: ")
            print(agent.search_by_title(title))

        elif choice == "5":
            author = input("Search author: ")
            print(agent.search_by_author(author))

        elif choice == "6":
            break
