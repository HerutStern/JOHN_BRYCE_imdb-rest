INSERT INTO public.actors
     ("id", "name",birth_year) VALUES
	 (1, 'David Craig',1968),
	 (5, 'Edward Norton',1969),
	 (6, 'John Travolta',1954),
	 (7, 'Uma Thurman',1970),
	 (8, 'Samuel L. Jackson',1948),
	 (9, 'Sam Worthington',1976),
	 (10,'Zoe Saldana',1978),
	 (11,'Jamie Foxx',1967),
	 (12,'Leonardo DiCaprio',1974);

INSERT INTO public.movies ("id", "name",description,duration,"year",pic_url) VALUES
	 (1,'Glass Onion','Famed Southern detective Benoit Blanc travels to Greece for his latest case.',139.0,2022,'https://upload.wikimedia.org/wikipedia/en/6/62/Glass_Onion_poster.jpg'),
	 (3,'Pulp Fiction','The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',154.0,1994,'https://www.imdb.com/title/tt0110912/mediaviewer/rm1959546112/?ref_=tt_ov_i'),
	 (4,'Inception','A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster.',148.0,2010,NULL),
	 (5,'The Departed','An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.',151.0,2006,NULL),
	 (6,'Guardians of the Galaxy','A group of intergalactic criminals must pull together to stop a fanatical warrior with plans to purge the universe.',121.0,2014,NULL),
	 (7,'Avatar','A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.',162.0,2010,NULL),
	 (8,'Django Unchained','With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal plantation-owner in Mississippi.',165.0,2014,NULL);

INSERT INTO public.movie_actors (salary,main_role,actor_id,movie_id) VALUES
	 (2000000,true,1,1),
	 (500000,false,5,1),
	 (12000000,true,6,3),
	 (3000000,true,7,3),
	 (3500000,false,8,3),
	 (2300000,true,9,4),
	 (4200000,true,10,4),
	 (9000000,true,11,5),
	 (3450000,false,12,5),
	 (2450000,true,12,6);

INSERT INTO public.movie_actors (salary,main_role,actor_id,movie_id) VALUES
	 (5500000,false,12,7),
	 (5700000,true,10,8);

INSERT INTO public.ratings (rating,rating_date,movie_id) VALUES
	 (9,'2023-01-17',1),
	 (8,'2022-01-17',1),
	 (9,'2022-05-17',1),
	 (7,'2023-01-01',3),
	 (10,'2023-01-10',3),
	 (9,'2022-01-16',4),
	 (6,'2022-04-15',4),
	 (5,'2021-02-14',4),
	 (9,'2023-01-12',5),
	 (8,'2023-01-11',5);

INSERT INTO public.ratings (rating,rating_date,movie_id) VALUES
	 (7,'2021-01-17',6),
	 (10,'2022-02-17',7),
	 (9,'2022-01-13',7),
	 (4,'2022-06-17',7),
	 (5,'2023-01-18',7),
	 (6,'2023-01-20',8);

insert into public.directors ("id","name",birth_year) values
	(1, 'Steven Spielberg', 1946),
	(2, 'Martin Scorsese', 1942),
	(3, 'Alfred Hitchcock', 1899),
	(4, 'James Cameron', 1954),
	(5, 'Spike Lee', 1957);

insert into public.oscars (nomination,ceremony_year,actor_id,director_id,movie_id) values
	('BEST PICTURE',1999,null,null,1),
	('VISUAL EFFECTS',2000,null,null,5),
	('ACTOR IN A SUPPORTING ROLE',1999,1,null,6),
	('ACTRESS IN A LEADING ROLE',2003,4,null,7),
	('DIRECTOR',2002,3,1,8),
	('DIRECTOR',2003,5,2,9);

ALTER SEQUENCE actors_id_seq RESTART WITH 100;
ALTER SEQUENCE movies_id_seq RESTART WITH 100;
ALTER SEQUENCE ratings_id_seq RESTART WITH 100;
ALTER SEQUENCE movie_actors_id_seq RESTART WITH 100;
ALTER SEQUENCE directors_actors_id_seq RESTART WITH 100;
ALTER SEQUENCE oscars_actors_id_seq RESTART WITH 100;

commit;

rollback;
