CREATE TABLE IF NOT EXISTS users(
    id INT(11) NOT NULL AUTO_INCREMENT,
	username VARCHAR(30) NOT NULL,
	pwd VARCHAR(255) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key (id)
);

CREATE TABLE IF NOT EXISTS movies(
    vendor varchar(32) not null,
    title varchar(256) not null,
    current_price real not null,
    previous_price real not null,
    sale real,
    status varchar(32),
    img_src varchar(256),
    list_src varchar(256)
);

