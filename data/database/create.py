import aiosqlite


async def create_database():
	async with aiosqlite.connect("data/database/database.db") as db:
		cursor = await db.cursor()

		query = """
		CREATE TABLE IF NOT EXISTS "users" (
			"id"	INTEGER,
			"username"	TEXT,
			"status"	TEXT,
			"date_status"	TEXT,
			"LocalBoost"	INTEGER,
			"date_LocalBoost"	TEXT,
			"coins"	INTEGER,
			"DayWheel"	BOOL,
			"CharacterDealer"	TEXT, 
			"NotificationsPayments"	BOOL
		);
		"""

		await cursor.executescript(query)
		await db.commit()