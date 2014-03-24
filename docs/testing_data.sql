
INSERT INTO servers values(1,'localhost','localhost');
INSERT INTO servers values(2,'remote','192.178.0.2');

INSERT INTO author values('111111','frank','Frank Huang','12345',1,'frank@gmail.com','male','edmonton','1992-01-01','/frank/1.jpg');
INSERT INTO author values('222222','jack','Jack Wong','12345',1,'jack@gmail.com','male','toronto','1994-01-01','/jack/1.jpg');
INSERT INTO author values('333333','william','William Zhang','12345',1,'william@gmail.com','male','calgary','1994-01-01','/william/1.jpg');
INSERT INTO author values('444444','mark','Mark Duan','12345',1,'mark@gmail.com','male','edmonton','1992-01-01','/mark/1.jpg');
INSERT INTO author values('555555','paul','Paul Xu','12345',1,'paul@gmail.com','male','edmonton','1992-01-01','/paul/1.jpg');
INSERT INTO author values('666666','rose','Rose Xiang','12345',1,'rose@gmail.com','male','calgary','1993-01-01','/rose/1.jpg');

INSERT INTO post values('1','444444',NULL,'Today is a brand new day','hello everyone','text','public');
INSERT into post values('5','777777',NULL,'belong to 777777','test permission fomh','text','fomh');
INSERT INTO author values('777777','ET','ET','12345','192.178.0.2','rose@gmail.com','male','calgary','1993-01-01','/rose/1.jpg');
INSERT INTO circle values('111111','222222');
INSERT INTO circle values('222222','111111');

INSERT INTO circle values('111111','333333');
INSERT INTO circle values('333333','111111');

INSERT INTO circle values('222222','444444');
INSERT INTO circle values('444444','222222');

INSERT INTO circle values('333333','444444');
INSERT INTO circle values('444444','333333');

INSERT INTO circle values('333333','555555');
INSERT INTO circle values('555555','333333');
 
INSERT INTO request values(NULL,'111111','222222');
INSERT INTO request values(NULL,'111111','333333');
INSERT INTO request values(NULL,'111111','444444');
INSERT INTO request values(NULL,'111111','555555');
insert into post values('2','111111',NULL,'Today is a brand new day','hello everyone','text','me');
INSERT into post values('1','444444',NULL,'Today is a brand new day','hello everyone','text','public');
INSERT into post values('3','333333',NULL,'belong to 333333','test permission friends','text','friends');
INSERT into post values('4','333333',NULL,'belong to 333333','test permission fof','text','fof');
