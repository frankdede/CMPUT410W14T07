USE c410;
DROP TABLE IF exists image;
DROP TABLE if exists signup_request;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS post_permission;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS circle;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS servers;

CREATE TABLE servers(
sid int,
name varchar(128) NOT NULL,
url varchar(128) NOT NULL,
PRIMARY KEY (sid)
);

CREATE TABLE author(
aid varchar(128) NOT NULL UNIQUE,
name varchar(128) NOT NULL ,
nick_name varchar(128),
pwd varchar(128) NOT NULL,
sid int default 1 NOT NULL,
email varchar(128),
gender varchar(128),
city varchar(128),
birthday varchar(128),
img_path varchar(128),
FULLTEXT(name,nick_name),
PRIMARY KEY (aid),
CONSTRAINT name_sid UNIQUE (name,sid),
FOREIGN KEY (sid) REFERENCES servers (sid)
);
/* fof firends of friend 
  fomh friends of my host
 */
CREATE TABLE post(
pid varchar(128) NOT NULL,
aid varchar(128) NOT NULL,
time TIMESTAMP NOT NULL,
title varchar(128) NOT NULL,
content varchar(1024),
type enum('html','text','markdown','picture') NOT NULL,
permission varchar(128) NOT NULL,
PRIMARY KEY (pid),
FOREIGN KEY (aid) REFERENCES author(aid) ON DELETE CASCADE
);

CREATE TABLE post_permission(
pid varchar(128) NOT NULL,
aid varchar(128) NOT NULL,
PRIMARY KEY(pid),
FOREIGN KEY(pid) REFERENCES post(pid)ON DELETE CASCADE,
FOREIGN KEY(aid) REFERENCES author(aid) ON DELETE CASCADE
);

CREATE TABLE circle(
aid1 varchar(128) NOT NULL,
aid2 varchar(128) NOT NULL,
PRIMARY KEY (aid1, aid2),
FOREIGN KEY (aid1) REFERENCES author(aid) ON DELETE CASCADE,
FOREIGN KEY (aid2) REFERENCES author(aid) ON DELETE CASCADE
);

CREATE TABLE request(
time timestamp,
recipient_id varchar(128) NOT NULL,
sender_id varchar(128) NOT NULL,
PRIMARY KEY (recipient_id,sender_id),
FOREIGN KEY (recipient_id) REFERENCES author(aid) ON DELETE CASCADE,
FOREIGN KEY (sender_id) REFERENCES author(aid) ON DELETE CASCADE
);

CREATE TABLE comments (
  cid varchar(128) NOT NULL,
  pid varchar(128) NOT NULL,
  aid varchar(128) NOT NULL, 
  time TIMESTAMP,
  content varchar(128),
  PRIMARY KEY(cid),
  FOREIGN KEY(pid) references post(pid) ON DELETE CASCADE,
  FOREIGN KEY(aid) references author(aid) ON DELETE CASCADE
);
CREATE TABLE signup_request(
	requester varchar(128) UNIQUE,
	primary key(requester)
);
CREATE TABLE image(
	image_id varchar(128),
	time timestamp,
	path varchar(128),
	aid varchar(128),
	pid varchar(128),
	primary key (image_id),
	FOREIGN KEY (aid) references author(aid) ON DELETE CASCADE,
	FOREIGN KEY (pid) references post(pid) ON DELETE CASCADE
);
