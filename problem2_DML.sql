USE library;

INSERT INTO author (name, country) VALUES
('Naguib Mahfouz', 'Egypt'),
('Jane Austen', 'UK'),
('Gabriel Garcia Marquez', 'Colombia');

INSERT INTO book (title, price, author_id) VALUES
('Palace Walk', 150.00, 1),
('Midaq Alley', 120.50, 1),
('Pride and Prejudice', 90.00, 2),
('Emma', 95.00, 2),
('One Hundred Years of Solitude', 180.00, 3),
('Love in the Time of Cholera', 170.00, 3);
