USE c410;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS user_permission;
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

/*CREATE TABLE comments (
  time TIMESTAMP,
  pid varchar(128),
  aid varchar(128),
  content varchar(128),
  FOREIGN KEY(pid) references post(pid),
  FOREIGN KEY(aid) references author(aid));
*/
CREATE TABLE author(
aid varchar(128) NOT NULL UNIQUE,
author_name varchar(128) NOT NULL UNIQUE,
pwd varchar(128) NOT NULL,
sid int default 1,
nick_name varchar(128),
PRIMARY KEY (aid, sid),
FOREIGN KEY (sid) REFERENCES servers (sid)
);
/* fof firends of friend 
  fomh friends of my host
 */
CREATE TABLE post(
pid varchar(128) NOT NULL,
aid varchar(128),
time TIMESTAMP NOT NULL,
title varchar(128) NOT NULL,
message varchar(1024),
type enum('html','text','markdown','picture') NOT NULL,
permission enum('me', 'user', 'friends', 'fof', 'fomh', 'public') NOT NULL,
PRIMARY KEY (pid),
FOREIGN KEY (aid) REFERENCES author (aid)
);
CREATE TABLE user_permission(
pid char(128) NOT NULL,
aid char(128) NOT NULL,
FOREIGN KEY(pid) REFERENCES post(pid),
FOREIGN KEY(aid) REFERENCES author(aid)
);

CREATE TABLE circle(
name1 varchar(128),
name2 varchar(128),
sid int,
PRIMARY KEY (name1, name2, sid),
FOREIGN KEY (name1) REFERENCES author (author_name),
FOREIGN KEY (name2) REFERENCES author (author_name),
FOREIGN KEY (sid) REFERENCES servers (sid)
);

CREATE TABLE message(
time timestamp,
recipient varchar(128),
sender varchar(128),
status boolean,
PRIMARY KEY (recipient,sender),
FOREIGN KEY (recipient) REFERENCES author(author_name),
FOREIGN KEY (sender) REFERENCES author(author_name)
);
