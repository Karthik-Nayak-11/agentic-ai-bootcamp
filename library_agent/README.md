# Mini Library Management System

This project implements a simple **Library Management System** using Python.  
It allows users to store, organize, search, and manage book records with **persistent storage** using JSON files.  
An optional report generator processes CSV data to generate simple library usage insights.

---

## Features

### Library Manager
- Add books manually
- Add books using Google Books API
- Persistent storage using JSON
- List all books
- Search books by title
- Search books by author
- Recommend books based on rating

### Optional Extension – Report Generator
- Reads a CSV file containing `studentName` and `bookTitle`
- Generates:
  - Total books issued
  - Book-wise issue count
  - Student-wise issue count
  - Books issued to a specific student

---

## Project Structure
```text
library_agent/
│
├── src/
│ ├── library_agent.py
│ ├── report_generator.py
│ └── data/
│ ├── books.json
│ └── issue_report.csv
│
├── requirements.txt
└── README.md