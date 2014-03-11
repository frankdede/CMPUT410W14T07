
INSERT INTO servers values(1,'localhost','localhost');
INSERT INTO servers values(2,'remote','192.178.0.2');

INSERT INTO author values('111111','frank','12345',1,'Frank Huang');
INSERT INTO author values('222222','mark','12345',1,'Mark Duan');
INSERT INTO author values('333333','pual','12345',1,'Pual Xu');
INSERT INTO author values('444444','owen','12345',1,'Owen Zhao');

INSERT INTO post values('p1','111111',NULL,'Sun Shine','What a beautiful day','text','public');
INSERT INTO post values('p2','222222',NULL,'Rainnig Day','You need an unberlla','text','public');
INSERT INTO post values('p3','333333',NULL,'Party','The city of Edmonton is hosting a BBQ party','text','public');
INSERT INTO post values('p4','333333',NULL,'LRT is Out of Service today','We apologize for the inconvenience','text','public');

INSERT INTO message VALUES(NULL,'frank','mark',0);
INSERT INTO message VALUES(NULL,'frank','pual',0);
