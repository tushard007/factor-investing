import logging
from pathlib import Path

from dotenv import dotenv_values
from psycopg import connect

from investing.core.db import schema_ddl, table_ddl

logger = logging.getLogger("factor-investing")
current_path = Path(__file__).resolve()
config = dotenv_values(current_path.parent.parent / ".env")

conn = connect(
    f"postgresql://{config['USER']}:{config['PASSWORD']}@localhost:5432/postgres",
)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'playground'")
if exists := cursor.fetchone():
    logger.info("Database 'playground' already exists")

else:
    cursor.execute("CREATE DATABASE playground")
    logger.info("Database 'playground' created")
cursor.close()
conn.close()

# Connect to the newly created database
conn = connect(
    f"postgresql://{config['USER']}:{config['PASSWORD']}@localhost:5432/playground",
)
cursor = conn.cursor()

cursor.execute(schema_ddl)
logger.info("Schema setup complete")
conn.commit()

cursor.execute(table_ddl)
logger.info("Table setup complete")
conn.commit()
