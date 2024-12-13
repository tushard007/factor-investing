create table if not exists factor_investing.ticker_history
(
    date   date,
    ticker text,
    key    text primary key,
    open   double precision,
    high   double precision,
    low    double precision,
    close  double precision
);

create index idx_key
    on factor_investing.ticker_history (key);
