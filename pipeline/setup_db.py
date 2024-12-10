import logging

import psycopg
from dotenv import dotenv_values

from investing.core.db import schema_ddl, table_ddl

logger = logging.getLogger("factor-investing")

config = dotenv_values("../.env")

conn = psycopg.connect(
    f"postgresql://{config['USER']}:{config['PASSWORD']}@localhost:5432/playground"
)
with conn.cursor() as cursor:
    # cursor.execute(database_ddl)
    logger.info(cursor.execute("select * from test.dummy1 limit 1").fetchone())
    logger.info("Database setup complete")
    logger.info(schema_ddl)
    cursor.execute(schema_ddl)
    logger.info("Schema setup complete")
    cursor.execute(table_ddl)
    logger.info("Table setup complete")
    conn.commit()
conn.close()
