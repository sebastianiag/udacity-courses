-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE tournament (
       id serial primary key,
       name text not null
);

CREATE TABLE players (
       id serial primary key, 
       name text not null, 
       tournament_id int references tournament(id)
);

CREATE TABLE matches (
       match_id serial primary key,
       winner int references players(id),
       loser int references players(id)
);

CREATE VIEW countMatches AS SELECT id, name, count(matches.match_id) AS matches FROM players LEFT JOIN matches ON players.id = matches.winner OR players.id = matches.loser GROUP BY players.id;
 
CREATE VIEW countWins AS SELECT id, name, count(matches.match_id) AS wins FROM players LEFT JOIN matches ON players.id = matches.winner GROUP BY players.id;
