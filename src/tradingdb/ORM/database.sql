--
-- File generated with SQLiteStudio v3.3.3 on Wed Apr 27 08:35:23 2022
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: currency
CREATE TABLE currency (
    ID   INTEGER   PRIMARY KEY
                   UNIQUE
                   NOT NULL,
    NAME CHAR (20) NOT NULL
                   UNIQUE
);


-- Table: exchange
CREATE TABLE exchange (
    ID          INTEGER   PRIMARY KEY
                          NOT NULL
                          UNIQUE,
    NAME        CHAR (50) UNIQUE
                          NOT NULL
);


-- Table: period
CREATE TABLE period (
    NAME              STRING  UNIQUE
                              NOT NULL,
    CONVERSION_IN_SEC INTEGER NOT NULL,
    ID                INTEGER UNIQUE
                              NOT NULL
                              PRIMARY KEY
);


-- Table: stock
CREATE TABLE stock (
    id          INTEGER PRIMARY KEY,
    symbol      TEXT    NOT NULL
                        UNIQUE,
    yf_symbol   TEXT    NOT NULL
                        UNIQUE,
    company     TEXT    NOT NULL,
    exchange_id INT     REFERENCES exchange (ID) NOT NULL,
    CURRENCY_ID INTEGER   CONSTRAINT STOCK_ID_CURRENCY_ID REFERENCES currency (ID) 
);


-- Table: stock_price
CREATE TABLE stock_price (
    id             INTEGER PRIMARY KEY,
    stock_id       INTEGER,
    date           REAL    NOT NULL,
    open           REAL    NOT NULL,
    high           REAL    NOT NULL,
    low            REAL    NOT NULL,
    close          REAL    NOT NULL,
    adjusted_close REAL    NOT NULL,
    volume         REAL    NOT NULL,
    period_id      INTEGER REFERENCES period (ID) 
                           NOT NULL,
    FOREIGN KEY (
        stock_id
    )
    REFERENCES stock (id),
    UNIQUE (
        stock_id,
        date,
        period_id
    )
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
