CREATE DATABASE BradBotDB;

USE BradBotDB;

CREATE TABLE Matches (
    match_id    BIGINT          NOT NULL PRIMARY KEY,
    kills       INTEGER         NOT NULL,
    assists     INTEGER         NOT NULL,
    deaths      INTEGER         NOT NULL
);

CREATE TABLE Users (
    user_id     BIGINT          NOT NULL PRIMARY KEY,
    user_name   VARCHAR(128)    NOT NULL,
    uses        INTEGER         NOT NULL
);

CREATE TABLE Images (
    image_id    INTEGER         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    image_url   VARCHAR(512)    NOT NULL UNIQUE
);

CREATE TABLE Quotes (
    quote_id    INTEGER         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    match_id    BIGINT          NOT NULL,
    quote       VARCHAR(255)    NOT NULL,
    CONSTRAINT quote_match FOREIGN KEY (match_id) REFERENCES Matches(match_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE MessageID (
    message_id  BIGINT          NOT NULL PRIMARY KEY,
    guild_id    BIGINT          NOT NULL,
    guild_name  VARCHAR(128)    NOT NULL,
    message_txt VARCHAR(2500)   NOT NULL,
    quote_id    INTEGER         NOT NULL,
    req_id      BIGINT          NOT NULL,
    CONSTRAINT quote_msg FOREIGN KEY (quote_id) REFERENCES Quotes(quote_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT user_msg FOREIGN KEY (req_id) REFERENCES Users(user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

