from sqlalchemy import Text, Table, Column, Integer, MetaData, TIMESTAMP, func

def table(metadata: MetaData, table_name: str):
	tasks_table = Table(
		table_name, metadata,
		Column("id", Integer, primary_key=True),
		Column("title", Text),
		Column("description", Text),
		Column("status", Text),
		Column("created_at", TIMESTAMP, server_default=func.now()),
		Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.now())
	)
	return tasks_table
