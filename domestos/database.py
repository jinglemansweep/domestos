from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.databases import mysql 

DB_APP = "sqlite"
DB_FILENAME = "/tmp/domestos.db"
DB_CONN = "%s:///%s" % (DB_APP, DB_FILENAME)
DB_ECHO = False

engine = create_engine(DB_CONN, echo=DB_ECHO)

metadata = MetaData()
devices_table = Table("device", metadata,
    Column("id", Integer, primary_key=True),
    Column("address", String),
    Column("description", String),
)

metadata.create_all(engine) 

