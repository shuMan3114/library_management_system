CREATE TABLE books(
  BookID VARCHAR(256) PRIMARY KEY,
  name VARCHAR(256),
  author VARCHAR(256),
  ISBN VARCHAR(256),
  publication VARCHAR(256),
  genre VARCHAR(256),
  price INTEGER,
  quantity INTEGER,
  books_borrowed INTEGER,
  times_borrowed INTEGER,
  unavailable BOOLEAN
);

CREATE TABLE User(
  UserID varchar(256) PRIMARY KEY,
  fname varchar(256),
  lname varchar(256),
  contact varchar(256),
  borrowedList TEXT,
  wishlist TEXT,
  password varchar(256)
);

CREATE TABLE Admin(
  admnID varchar(256) PRIMARY KEY,
  f_name varchar(256),
  l_name varchar(256),
  contact varchar(256),
  password varchar(256)
);

INSERT INTO books VALUES
('B20230001','It Ends With Us','9781501110368','Colleen Hoover','Simon & Schuster','Love',25,12,24,9,TRUE),
('B20230002','Shatter Me','780062085481','Tahereh Mafi','HarperCollins Publisher','Philosophical',21,23,25,21,TRUE),
('B20230003','Shadow and bone','9780805094596','Leigh Bardugo','Macmillan Publishers','Mystery',30,32,50,20,TRUE),
('B20230004','To Kill a Mockingbird','9780805094596','Harper Lee','J.B. LIppincott & Co.','Philosophical',20,10,9,3,TRUE),
('B20230005','Frankenstein','9780582541542','Mary Shelley','Harding','fiction',13,50,150,49,TRUE),
('B20230006','Crime And Punishment','9788420741468','Fyodor Dostoevsky','The Russian Messenger','Mystery',24,23,26,10,TRUE),
('B20230007','The Other Side of Night','9781797146072','Adam Hamdy','Simon & Schuster','Love',20,25,50,25,TRUE),
('B20230008','Everything Everything','9780553496673','Nicola Yoon','Delacorte Books','Philosphical',23,45,23,2,TRUE),
('B20230009','Looking For Alaska','9780525428022','John Green','Dutton Juvenile','Philosphical',26,32,34,1,TRUE),
('B20230010','The Sun is also a Star','9780553496710','Nicola Yoon','Delacorte Books','Philosphical',28,64,43,23,TRUE),
('B20230011','Flawed','9781250104311','Cecilia Ahern','Square Fish','Love',27,76,124,32,TRUE),
('B20230012','The Toymakers','9781785036354','Robert Dinsdale','Random House','Mystery',21,89,133,31,TRUE),
('B20230013','Paper Towns','9780142414934','John Green','Dutton Juvenile','fiction',23,10,15,21,TRUE),
('B20230014','Verity','9781538724736','Colleen Hoover','Sphere','fiction',24,25,12,3,TRUE),
('B20230015','City of Ashes','9781481455978','Cassandra Clare','Magaret K McElderry','fiction',26,49,24,21,TRUE),
('B20230016','The ABC Murders','9780062073587','Agatha Christie','HarperCollins Publisher','Mystery',27,34,34,34,TRUE),
('B20230017','The Great Gatsby','9798745274824','F.Scott','Charles Scribners Sons','Mystery',23,21,20,20,FALSE),
('B20230018','Jane Eyre','9781435171664','Charlotte Bronte','Smith,Elder and Co.','Love',30,67,21,10,TRUE),
('B20230019','Beloved','9781400033416','Toni Morrison','Alfred A.Knopf Inc.','Love',10,39,12,12,TRUE),
('B20230020','Hamlet','9780743477123','James Robert','Simon&Schuster','Love',12,15,5,5,TRUE),
('B20230021','The Sun also Rises','9781501121968','Ernest Hemingway',"Scribner's",'Philosphical',12,34,12,12,TRUE),
('B20230022','Madame Bovary','9780140449129','Gustave Flaubert',"Revue de Paris",'Love',15,70,23,23,TRUE),
('B20230023','Invisible Man','9780451531674','Ralph Ellison',"Random House",'fiction',20,35,40,5,TRUE),
('B20230024','Murder on the Orient express','9780062073495','Agatha Christie','HarperCollins Publisher','fiction',23,20,25,5,TRUE),
('B20230025','Lord of Shadows','9781442468412','Cassandra Clare',"Simon & Schuster",'fiction',24,23,21,2,TRUE);

