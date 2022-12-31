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
                          NOT NULL,
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

CREATE TABLE yf_info (
    [index]                      BIGINT,
    zip                          TEXT,
    sector                       TEXT,
    longBusinessSummary          TEXT,
    city                         TEXT,
    country                      TEXT,
    website                      TEXT,
    maxAge                       BIGINT,
    address1                     TEXT,
    industry                     TEXT,
    address2                     TEXT,
    ebitdaMargins                FLOAT,
    profitMargins                FLOAT,
    grossMargins                 FLOAT,
    operatingCashflow            FLOAT,
    revenueGrowth                FLOAT,
    operatingMargins             FLOAT,
    ebitda                       BIGINT,
    targetLowPrice               FLOAT,
    recommendationKey            TEXT,
    grossProfits                 BIGINT,
    freeCashflow                 FLOAT,
    targetMedianPrice            FLOAT,
    currentPrice                 FLOAT,
    earningsGrowth               FLOAT,
    currentRatio                 FLOAT,
    returnOnAssets               FLOAT,
    numberOfAnalystOpinions      FLOAT,
    targetMeanPrice              FLOAT,
    debtToEquity                 FLOAT,
    returnOnEquity               FLOAT,
    targetHighPrice              FLOAT,
    totalCash                    BIGINT,
    totalDebt                    BIGINT,
    totalRevenue                 BIGINT,
    totalCashPerShare            FLOAT,
    financialCurrency            TEXT,
    revenuePerShare              FLOAT,
    quickRatio                   FLOAT,
    recommendationMean           FLOAT,
    exchange                     TEXT,
    shortName                    TEXT,
    longName                     TEXT,
    exchangeTimezoneName         TEXT,
    exchangeTimezoneShortName    TEXT,
    isEsgPopulated               BOOLEAN,
    gmtOffSetMilliseconds        TEXT,
    quoteType                    TEXT,
    symbol                       TEXT,
    messageBoardId               TEXT,
    market                       TEXT,
    annualHoldingsTurnover       TEXT,
    enterpriseToRevenue          FLOAT,
    beta3Year                    TEXT,
    enterpriseToEbitda           FLOAT,
    [52WeekChange]               FLOAT,
    morningStarRiskRating        TEXT,
    forwardEps                   FLOAT,
    revenueQuarterlyGrowth       TEXT,
    sharesOutstanding            BIGINT,
    fundInceptionDate            TEXT,
    annualReportExpenseRatio     TEXT,
    totalAssets                  TEXT,
    bookValue                    FLOAT,
    sharesShort                  TEXT,
    sharesPercentSharesOut       TEXT,
    fundFamily                   TEXT,
    lastFiscalYearEnd            BIGINT,
    heldPercentInstitutions      FLOAT,
    netIncomeToCommon            BIGINT,
    trailingEps                  FLOAT,
    lastDividendValue            FLOAT,
    SandP52WeekChange            FLOAT,
    priceToBook                  FLOAT,
    heldPercentInsiders          FLOAT,
    nextFiscalYearEnd            BIGINT,
    yield                        TEXT,
    mostRecentQuarter            BIGINT,
    shortRatio                   TEXT,
    sharesShortPreviousMonthDate TEXT,
    floatShares                  BIGINT,
    beta                         FLOAT,
    enterpriseValue              BIGINT,
    priceHint                    BIGINT,
    threeYearAverageReturn       TEXT,
    lastSplitDate                FLOAT,
    lastSplitFactor              TEXT,
    legalType                    TEXT,
    lastDividendDate             FLOAT,
    morningStarOverallRating     TEXT,
    earningsQuarterlyGrowth      FLOAT,
    priceToSalesTrailing12Months FLOAT,
    dateShortInterest            TEXT,
    pegRatio                     FLOAT,
    ytdReturn                    TEXT,
    forwardPE                    FLOAT,
    lastCapGain                  TEXT,
    shortPercentOfFloat          TEXT,
    sharesShortPriorMonth        TEXT,
    impliedSharesOutstanding     BIGINT,
    category                     TEXT,
    fiveYearAverageReturn        TEXT,
    previousClose                FLOAT,
    regularMarketOpen            FLOAT,
    twoHundredDayAverage         FLOAT,
    trailingAnnualDividendYield  FLOAT,
    payoutRatio                  FLOAT,
    volume24Hr                   TEXT,
    regularMarketDayHigh         FLOAT,
    navPrice                     TEXT,
    averageDailyVolume10Day      BIGINT,
    regularMarketPreviousClose   FLOAT,
    fiftyDayAverage              FLOAT,
    trailingAnnualDividendRate   FLOAT,
    open                         FLOAT,
    toCurrency                   TEXT,
    averageVolume10days          BIGINT,
    expireDate                   TEXT,
    algorithm                    TEXT,
    dividendRate                 FLOAT,
    exDividendDate               FLOAT,
    circulatingSupply            TEXT,
    startDate                    TEXT,
    regularMarketDayLow          FLOAT,
    currency                     TEXT,
    trailingPE                   FLOAT,
    regularMarketVolume          BIGINT,
    lastMarket                   TEXT,
    maxSupply                    TEXT,
    openInterest                 TEXT,
    marketCap                    BIGINT,
    volumeAllCurrencies          TEXT,
    strikePrice                  TEXT,
    averageVolume                BIGINT,
    dayLow                       FLOAT,
    ask                          BIGINT,
    askSize                      FLOAT,
    volume                       BIGINT,
    fiftyTwoWeekHigh             FLOAT,
    fromCurrency                 TEXT,
    fiveYearAvgDividendYield     FLOAT,
    fiftyTwoWeekLow              FLOAT,
    bid                          FLOAT,
    tradeable                    BOOLEAN,
    dividendYield                FLOAT,
    bidSize                      FLOAT,
    dayHigh                      FLOAT,
    coinMarketCapLink            TEXT,
    regularMarketPrice           FLOAT,
    logo_url                     TEXT,
    fullTimeEmployees            FLOAT,
    phone                        TEXT,
    fax                          TEXT,
    FOREIGN KEY (
        symbol
    )
    REFERENCES stock (yf_symbol),
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
