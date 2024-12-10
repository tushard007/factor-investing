# Factor Investing

TODO: Add a proper description of the project.
Factor Investing is a strategy that involves selecting securities based on attributes that are associated with higher returns. The most common factors are value, size, momentum, low volatility, quality, and dividend yield.

## Introduction

The repository contains the code for the Factor Investing project. The project is divided into the following sections:

1. `Python library` for factor investing
2. `REST API` to interact with the data produced by the Factor Investing.

## Installation

1. **`Step 1`** - Clone the repository
2. **`Step 2`** - Setup [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
3. **`Step 3`** - Install project as library

```bash
cd path/to/factor-investing
poetry install
```

4. **`Step 4`** - Setup the database
 - Install Postgres database
 - Create a database named `playground` or use [create database](investing/core/db/_database.sql) sql script
 - Create a schema named `factor_investing` or use [create schema](investing/core/db/_schema.sql) sql script
 - Create all tables using [create table](investing/core/db/_table.sql) sql script
 - Create a .env file in the root directory and add the following environment variables
   - USER
   - PASSWORD
  

## Usage

1. **`Run the REST API`**

```bash
cd path/to/factor-investing
poetry run uvicorn main:app --reload
```

2. **`Ticker data insert pipeline`**

```bash
cd path/to/factor-investing
poetry run python pipeline/ticker_history_data_insert.py
```
