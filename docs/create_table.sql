DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS circle;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS servers;

CREATE TABLE servers(
sid int,
servers_name varchar(128) NOT NULL,
url varchar(128) NOT NULL,
PRIMARY KEY (sid)
);

CREATE TABLE author(
aid varchar(128),
pwd varchar(128) NOT NULL,
sid int default 1,
nick_name varchar(128) NOT NULL,
PRIMARY KEY (aid, sid),
FOREIGN KEY (sid) REFERENCES servers (sid)
);

CREATE TABLE post(
aid varchar(128),
dates date NOT NULL,
title varchar(128) NOT NULL,
message varchar(1024),
type enum('html','txt','markdown') NOT NULL,
permission enum('me', 'user', 'friends', 'friends of friends', 'friends on my host', 'public') NOT NULL,
PRIMARY KEY (aid, dates),
FOREIGN KEY (aid) REFERENCES author (aid)
);

CREATE TABLE circle(
aid varchar(128),
fid varchar(128),
sid int,
PRIMARY KEY (aid, fid, sid),
FOREIGN KEY (aid) REFERENCES author (aid),
FOREIGN KEY (fid) REFERENCES author (aid),
FOREIGN KEY (sid) REFERENCES servers (sid)
);
