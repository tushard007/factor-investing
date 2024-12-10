from pathlib import Path

from ._db_utils import *
from ._sql_query import *

current_dir = Path(__file__).parent

_database_ddl = current_dir / "_database.sql"
database_ddl = Path(_database_ddl).read_text()

_schema_ddl = current_dir / "_schema.sql"
schema_ddl = Path(_schema_ddl).read_text()

_table_ddl = current_dir / "_table.sql"
table_ddl = Path(_table_ddl).read_text()
