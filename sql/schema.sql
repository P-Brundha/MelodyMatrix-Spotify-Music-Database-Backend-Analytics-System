CREATE DATABASE IF NOT EXISTS mus_db;
USE mus_db;

CREATE TABLE IF NOT EXISTS artists (
    id VARCHAR(50) PRIMARY KEY,
    followers INT NOT NULL DEFAULT 0,
    genres TEXT,
    name VARCHAR(255) NOT NULL,
    popularity INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tracks (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    popularity INT NOT NULL DEFAULT 0,
    duration_ms INT NOT NULL DEFAULT 0,
    explicit BOOLEAN NOT NULL DEFAULT FALSE,
    artists TEXT,
    id_artists TEXT,
    release_date DATE,
    danceability FLOAT NOT NULL DEFAULT 0,
    energy FLOAT NOT NULL DEFAULT 0,
    `key` INT NOT NULL DEFAULT 0,
    loudness FLOAT NOT NULL DEFAULT 0,
    mode INT NOT NULL DEFAULT 0,
    speechiness FLOAT NOT NULL DEFAULT 0,
    acousticness FLOAT NOT NULL DEFAULT 0,
    instrumentalness FLOAT NOT NULL DEFAULT 0,
    liveness FLOAT NOT NULL DEFAULT 0,
    valence FLOAT NOT NULL DEFAULT 0,
    tempo FLOAT NOT NULL DEFAULT 0,
    time_signature INT NOT NULL DEFAULT 0
);





