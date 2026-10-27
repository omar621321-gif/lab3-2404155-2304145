DROP DATABASE IF EXISTS library;
CREATE DATABASE library;
USE library;

CREATE TABLE author (
  author_id INT         NOT NULL AUTO_INCREMENT,
  name      VARCHAR(80) NOT NULL,
  country   VARCHAR(50),
  PRIMARY KEY (author_id)
);

CREATE TABLE book (
  book_id   INT           NOT NULL AUTO_INCREMENT,
  title     VARCHAR(150)  NOT NULL,
  price     DECIMAL(10,2) NOT NULL,
  author_id INT           NOT NULL,
  PRIMARY KEY (book_id),
  FOREIGN KEY (author_id) REFERENCES author(author_id)
    ON DELETE CASCADE
);
