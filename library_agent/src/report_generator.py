import csv
from pathlib import Path
from collections import Counter, defaultdict

class ReportGenerator:

    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)
        self.records = self.load_records()

    def load_records(self):
        with open(self.csv_path, newline='', encoding="utf-8") as f:
            return list(csv.DictReader(f))

    # ---------- Reports ----------

    def total_issues(self):
        return len(self.records)

    def books_issued_count(self):
        return Counter(record["bookTitle"] for record in self.records)

    def student_issue_count(self):
        return Counter(record["studentName"] for record in self.records)

    def books_issued_by_student(self, student_name):
        return [
            record["bookTitle"]
            for record in self.records
            if record["studentName"].lower() == student_name.lower()
        ]

if __name__ == "__main__":
    report = ReportGenerator("data/students.csv")

    print("Total Books Issued:", report.total_issues())
    print("Book-wise Count:", report.books_issued_count())
    print("Student-wise Count:", report.student_issue_count())
    print("Books issued to Asha:", report.books_issued_by_student("Asha"))
