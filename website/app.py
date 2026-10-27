import os
from decimal import Decimal, InvalidOperation

import pymysql
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")


def run(sql, args=(), fetch=False):
    """Run one statement with parameters; return rows if fetch=True."""
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "library"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return cur.fetchall() if fetch else cur.rowcount
    finally:
        conn.close()


def check_book(form):
    errors = []
    title = form.get("title", "").strip()
    price = form.get("price", "").strip()
    author_id = form.get("author_id", "").strip()
    if not title:
        errors.append("Title is required")
    elif len(title) > 150:
        errors.append("Title is too long (150 characters at most)")
    try:
        if Decimal(price) < 0:
            errors.append("Price cannot be negative")
    except InvalidOperation:
        errors.append("Price must be a number")
    if not author_id.isdigit():
        errors.append("Choose an author")
    return errors, title, price, author_id


def check_author(form):
    errors = []
    name = form.get("name", "").strip()
    country = form.get("country", "").strip()
    if not name:
        errors.append("Name is required")
    elif len(name) > 80:
        errors.append("Name is too long (80 characters at most)")
    if len(country) > 50:
        errors.append("Country is too long (50 characters at most)")
    return errors, name, country


@app.route("/")
def index():
    books = run("SELECT book_id, title, price, author_id FROM book ORDER BY book_id", fetch=True)
    authors = run("SELECT author_id, name, country FROM author ORDER BY author_id", fetch=True)
    return render_template("index.html", books=books, authors=authors)


# ---------- books ----------
@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    authors = run("SELECT author_id, name FROM author ORDER BY name", fetch=True)
    if request.method == "POST":
        errors, title, price, author_id = check_book(request.form)
        if not errors:
            try:
                run("INSERT INTO book (title, price, author_id) VALUES (%s, %s, %s)",
                    (title, price, author_id))
                flash("Book added", "ok")
                return redirect(url_for("index"))
            except pymysql.err.IntegrityError:
                errors.append("This author does not exist")
        for e in errors:
            flash(e, "error")
        return render_template("book_form.html", authors=authors, book=request.form, mode="Add")
    return render_template("book_form.html", authors=authors, book={}, mode="Add")


@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    rows = run("SELECT * FROM book WHERE book_id = %s", (book_id,), fetch=True)
    if not rows:
        flash("Book not found", "error")
        return redirect(url_for("index"))
    authors = run("SELECT author_id, name FROM author ORDER BY name", fetch=True)
    if request.method == "POST":
        errors, title, price, author_id = check_book(request.form)
        if not errors:
            try:
                run("UPDATE book SET title = %s, price = %s, author_id = %s WHERE book_id = %s",
                    (title, price, author_id, book_id))
                flash("Book updated", "ok")
                return redirect(url_for("index"))
            except pymysql.err.IntegrityError:
                errors.append("This author does not exist")
        for e in errors:
            flash(e, "error")
        return render_template("book_form.html", authors=authors, book=request.form, mode="Edit")
    return render_template("book_form.html", authors=authors, book=rows[0], mode="Edit")


@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    run("DELETE FROM book WHERE book_id = %s", (book_id,))
    flash("Book removed", "ok")
    return redirect(url_for("index"))


# ---------- authors ----------
@app.route("/authors/add", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        errors, name, country = check_author(request.form)
        if not errors:
            run("INSERT INTO author (name, country) VALUES (%s, %s)", (name, country or None))
            flash("Author added", "ok")
            return redirect(url_for("index"))
        for e in errors:
            flash(e, "error")
        return render_template("author_form.html", author=request.form, mode="Add")
    return render_template("author_form.html", author={}, mode="Add")


@app.route("/authors/<int:author_id>/edit", methods=["GET", "POST"])
def edit_author(author_id):
    rows = run("SELECT * FROM author WHERE author_id = %s", (author_id,), fetch=True)
    if not rows:
        flash("Author not found", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        errors, name, country = check_author(request.form)
        if not errors:
            run("UPDATE author SET name = %s, country = %s WHERE author_id = %s",
                (name, country or None, author_id))
            flash("Author updated", "ok")
            return redirect(url_for("index"))
        for e in errors:
            flash(e, "error")
        return render_template("author_form.html", author=request.form, mode="Edit")
    return render_template("author_form.html", author=rows[0], mode="Edit")


@app.route("/authors/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    run("DELETE FROM author WHERE author_id = %s", (author_id,))  # books deleted by ON DELETE CASCADE
    flash("Author removed together with their books", "ok")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
