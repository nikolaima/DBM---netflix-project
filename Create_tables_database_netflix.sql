CREATE database dbm_netflix_project;
USE dbm_netflix_project;

CREATE table shows(
show_id int primary key,
type ENUM('Movie','TV Show'),
title varchar(200),
date_added datetime,
release_year int,
rating_code varchar(15),
duration int,
season_count int,
description varchar (500)
);

#table genre with 2 columns genre_id + genre + last_update
CREATE TABLE genre(
genre_id int primary key,
genre varchar(100),
last_update datetime default now()
);

#table actor with 3 columns actor_id + actor + last_update
CREATE TABLE actor(
actor_id int primary key,
actor varchar(100),
last_update datetime default now()
);

#table director with 3 columns director_id, director + last_update
CREATE TABLE director(
director_id int primary key,
director varchar(100),
last_update datetime default now()
);

#table rating with 3 columns rating_id, rating_description + las_update
CREATE TABLE rating(
rating_code varchar(100),
rating_description varchar(200),
last_update datetime default now()
);

#table for country w countryId, country + last_update
CREATE table country(
country_id int primary key,
country varchar(100),
last_update datetime default now()
);

#table to connect n:m relationship between shows
CREATE table show_country(
show_id int,
country_id int,
last_update datetime default now(),
FOREIGN KEY (show_id) REFERENCES shows(show_id),
FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE table show_director(
show_id int,
director_id int,
last_update datetime default now(),
FOREIGN KEY (show_id) REFERENCES shows(show_id),
FOREIGN KEY (director_id) REFERENCES director(director_id)
);

CREATE table show_actor(
show_id int,
actor_id int,
last_update datetime default now(),
FOREIGN KEY (show_id) REFERENCES shows(show_id),
FOREIGN KEY (actor_id) REFERENCES actor(actor_id)
);

CREATE table show_genre(
show_id int,
genre_id int,
last_update datetime default now(),
FOREIGN KEY (show_id) REFERENCES shows(show_id),
FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);



#not necesaary,just an option for loading all the data in one big data without normalization etc.
#CREATE TABLE netflix_stage (
#  `show_id` bigint DEFAULT NULL,
#  `type` text,
#  `title` text,
#  `director` text,
#  `cast` text,
#  `country` text,
#  `date_added` datetime DEFAULT NULL,
#  `release_year` bigint DEFAULT NULL,
# `rating` text,
#  `duration` text,
#  `listed_in` text,
#  `description` text,
#  `season_count` text
#) ;