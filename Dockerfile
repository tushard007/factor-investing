FROM python:3.12-slim

ARG PACKAGE=factor_investing-0.3.1-py3-none-any.whl

WORKDIR /app

COPY dist/${PACKAGE} ${PACKAGE}
COPY main.py main.py

RUN apt update -y && apt upgrade && \
    apt --no-install-recommends -y install gcc g++ && \
    apt purge -y && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install ${PACKAGE}

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
