import aiosqlite
import asyncio
import time

async def async_fetch_users(db):
    """An asynchronous task to fetch all users."""
    # await asyncio.sleep(0.5)  # Simulate a network delay
    async with db.execute("SELECT * FROM user_data") as cursor:
        rows = await cursor.fetchall()
        print("Fetched all users.")
        return rows

async def async_fetch_older_users(db):
    """fetch users lder than 40"""
    async with db.execute("SELECT * FROM user_data WHERE age > ?",(40,)) as cursor:
        results = await cursor.fetchall()
        print("Users older than 40:", results)
        return results


async def fetch_concurrently():
    start_time = time.time()
    async with aiosqlite.connect("ALX_pro_dev.db") as db:
        all_users, older_users = await asyncio.gather(
            async_fetch_users(db),
            async_fetch_older_users(db)
        )
        print("Final results for all users:", all_users)
        print("Final results for older users:", older_users)

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())