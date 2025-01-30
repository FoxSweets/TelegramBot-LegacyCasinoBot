import aiosqlite
import asyncio
import datetime
import types


class BotBD:
    def __init__(self) -> None:
        self.db = None
        self.cursor = None

    async def connect(self):
        self.db = await aiosqlite.connect('data/database/database.db')
        self.cursor = await self.db.cursor()

    async def create_user(self, user_id: int, username: str):
        async with self.db.execute(f"SELECT id FROM users WHERE id = ?", (user_id,)) as cursor:
            if await cursor.fetchone() is None:
                await self.cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                          (user_id, username, 'PLAYER', 'INFINITY', 1, 'INFINITY', 1000, True, 'evil', True,))
        await self.db.commit()

    async def update_status(self, user_id: int, status: str, date_status: str):
        await self.cursor.execute(f"UPDATE users SET status = ?, date_status = ? WHERE id = ?", (status, date_status, user_id,))
        await self.db.commit()

    async def update_character_dealer(self, user_id: int, character_dealer: str):
        await self.cursor.execute(f"UPDATE users SET CharacterDealer = ? WHERE id = ?", (character_dealer, user_id,))
        await self.db.commit()

    async def update_add_coins(self, user_id: int, coins: int):
        await self.cursor.execute(f"UPDATE users SET coins = coins + ? WHERE id = ?", (coins, user_id,))
        await self.db.commit()

    async def update_remove_coins(self, user_id: int, coins: int):
        await self.cursor.execute(f"UPDATE users SET coins = coins - ? WHERE id = ?", (coins, user_id,))
        await self.db.commit()

    async def update_day_wheel(self, user_id: int, day_wheel: bool):
        await self.cursor.execute(f"UPDATE users SET DayWheel = ? WHERE id = ?", (day_wheel, user_id,))
        await self.db.commit()

    async def users_profile(self, user_id: int) -> list[str | int]:
        async with self.db.execute("SELECT username, status, date_status, LocalBoost, date_LocalBoost, coins, CharacterDealer FROM users WHERE id = ?", (user_id,)) as cursor:
            rows = await cursor.fetchall()
        return rows[0]

    async def amount_coins(self, user_id: int) -> int:
        async with self.db.execute(f"SELECT coins FROM users WHERE id=?", (user_id,)) as cursor:
            code = await cursor.fetchone()
        return code[0]

    async def get_character_dealer(self, user_id: int) -> int:
        async with self.db.execute(f"SELECT CharacterDealer FROM users WHERE id=?", (user_id,)) as cursor:
            character_dealer = await cursor.fetchone()
        return character_dealer[0]

    async def get_profile_status(self, user_id: int) -> int:
        async with self.db.execute(f"SELECT status FROM users WHERE id=?", (user_id,)) as cursor:
            status = await cursor.fetchone()
        return status[0]

    async def get_day_wheel(self, user_id: int) -> int:
        async with self.db.execute(f"SELECT DayWheel FROM users WHERE id=?", (user_id,)) as cursor:
            status = await cursor.fetchone()
        return status[0]

    async def get_all_admins(self):
        async with self.db.execute(f"SELECT id FROM users WHERE status = 'ADMIN'") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def get_all_users(self):
        async with self.db.execute(f"SELECT id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def get_all_users_status(self):
        async with self.db.execute(f"SELECT id, date_status FROM users WHERE status != 'PLAYER' AND date_status != 'INFINITY'") as cursor:
            rows = await cursor.fetchall()
            return [row for row in rows]

    async def close_database(self):
        await self.cursor.close()
        await self.db.close()