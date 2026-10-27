# Lab 3 – Foreign Keys and Simple SQL

Omar mohamed Aboalnaja / 2404155  // Amr khaled el sheikh / 2304145

## Technology
Back end: Python 3 + Flask + PyMySQL (plain SQL, always with `%s` parameters).
Front end: HTML (Jinja templates) + CSS. Database: MySQL (databases `company` and `library`).

## Files
| File | Content |
|---|---|
| problem1_DDL.sql / problem1_DML.sql | COMPANY schema (3 tables, 3 foreign keys) and ≥3 rows per table |
| problem1_Answers.txt | SQL, output/error for Q1.1–Q1.3 |
| problem2_DDL.sql / problem2_DML.sql | library schema (`ON DELETE CASCADE`), 3 authors + 6 books |
| website/ | The web site with the new pages (F2.1–F2.5) |

## How to run (step by step)
1. Install **MySQL Server** and **Python 3.10+**.
2. Problem 1:
   ```
   mysql -u root -p < problem1_DDL.sql
   mysql -u root -p < problem1_DML.sql
   mysql -u root -p company      # then run the queries of problem1_Answers.txt
   ```
3. Problem 2 database:
   ```
   mysql -u root -p < problem2_DDL.sql
   mysql -u root -p < problem2_DML.sql
   ```
4. Website:
   ```
   cd website
   python -m venv venv
   venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
   pip install -r requirements.txt
   copy .env.example .env         # Linux/macOS: cp .env.example .env
   ```
   Edit `.env` and write your MySQL password in `DB_PASSWORD`, then:
   ```
   python app.py
   ```
5. Open http://127.0.0.1:5000

## Features
- F2.1 tables of books (with `author_id`) and authors on the home page
- F2.2 add a book / add an author
- F2.3 edit a book / edit an author
- F2.4 remove a book (with confirmation)
- F2.5 remove an author (with confirmation); the books of the author are removed by `ON DELETE CASCADE`
- Validation on the server (empty title, bad price, unknown author…), responsive layout
