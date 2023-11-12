from sqlalchemy import MetaData, Integer, String, ForeignKey, Table, Column, Date, Time


metadata = MetaData()

reservation = Table(
    "reservation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("time", Time, nullable=False),
    Column("event", String, nullable=False),
    Column("status", String, nullable=False),
    Column("user_id", Integer, ForeignKey("user.id")),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("full name", String, nullable=False),
    Column("email", String, nullable=False),
)