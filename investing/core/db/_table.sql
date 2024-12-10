create table if not exists factor_investing.ticker_history
(
    date         date,
    ticker       text,
    key          text,
    open         double precision,
    high         double precision,
    low          double precision,
    close        double precision,
    volume       double precision,
    stock_splits double precision
)
