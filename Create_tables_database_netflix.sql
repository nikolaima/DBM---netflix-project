CREATE database dbm_netflix_project;
USE dbm_netflix_project;

CREATE table shows(
show_id int primary key NOT NULL,
type ENUM('Movie','TV Show') NOT NULL,
title varchar(200) NOT NULL,
date_added datetime,
release_year int,
rating_code varchar(15),
duration int,
season_count int,
description varchar (500),
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

#table genre with 2 columns genre_id + genre + last_update
CREATE TABLE genre(
genre_id smallint primary key NOT NULL,
genre varchar(100) NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

#table actor with 3 columns actor_id + actor + last_update
CREATE TABLE actor(
actor_id int primary key NOT NULL,
actor varchar(100) NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

#table director with 3 columns director_id, director + last_update
CREATE TABLE director(
director_id int primary key NOT NULL,
director varchar(100) NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

#table rating with 3 columns rating_id, rating_description + las_update
CREATE TABLE rating(
rating_code varchar(100) primary key NOT NULL,
rating_description varchar(200) NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

#table for country w countryId, country + last_update
CREATE table country(
country_id smallint primary key NOT NULL,
country varchar(100) NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

#table to connect n:m relationship between shows
CREATE table show_country(
show_id int NOT NULL,
country_id smallint NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (show_id,country_id),
CONSTRAINT `fk_show_country_show` FOREIGN KEY (show_id) REFERENCES shows(show_id),
CONSTRAINT `fk_show_country_country` FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE table show_director(
show_id int NOT NULL,
director_id int NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (show_id, director_id),
CONSTRAINT `fk_show_director_show` FOREIGN KEY (show_id) REFERENCES shows(show_id),
CONSTRAINT `fk_show_director_director` FOREIGN KEY (director_id) REFERENCES director(director_id)
);

CREATE table show_actor(
show_id int NOT NULL,
actor_id int NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (show_id, actor_id),
CONSTRAINT `fk_show_actor_show` FOREIGN KEY (show_id) REFERENCES shows(show_id),
CONSTRAINT `fk_show_actor_actor` FOREIGN KEY (actor_id) REFERENCES actor(actor_id)
);

CREATE table show_genre(
show_id int NOT NULL,
genre_id smallint NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY(show_id, genre_id),
CONSTRAINT `fk_show_genre_show` FOREIGN KEY (show_id) REFERENCES shows(show_id),
CONSTRAINT `fk_show_genre_genre` FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

CREATE TABLE users (
  user_name varchar(100) NOT NULL PRIMARY KEY,
  password varchar(100) NOT NULL,
  last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE table users_shows(
	user_name varchar(100) NOT NULL,
    show_id int NOT NULL,
    last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_name, show_id),
    CONSTRAINT `fk_users_shows_user` FOREIGN KEY (`user_name`) REFERENCES `users` (`user_name`) ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT `fk_users_shows_shows` FOREIGN KEY (`show_id`) REFERENCES `shows` (`show_id`) ON DELETE RESTRICT ON UPDATE CASCADE
);


#not necesaary,just an option for loading all the data in one big table without normalization etc.
CREATE TABLE netflix_stage (
  `show_id` bigint DEFAULT NULL,
  `type` text,
  `title` text,
  `director` text,
  `cast` text,
  `country` text,
  `date_added` datetime DEFAULT NULL,
  `release_year` bigint DEFAULT NULL,
 `rating` text,
  `duration` text,
  `listed_in` text,
  `description` text,
  `season_count` text
) ;
