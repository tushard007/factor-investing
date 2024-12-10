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
