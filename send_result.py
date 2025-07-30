from nio import AsyncClient
import os
import asyncio

HOMESERVER = "https://matrix.org"
ACCESS_TOKEN = os.getenv("MATRIX_TOKEN")
USER_ID = os.getenv("MATRIX_USER_ID")  # e.g., @botuser:matrix.org
ROOM_ID = os.getenv("MATRIX_ROOM_ID")

MESSAGE = "✅ GitHub action ran successfully."

async def main():
    client = AsyncClient(HOMESERVER, USER_ID)
    client.access_token = ACCESS_TOKEN
    client.user_id = USER_ID
    client.device_id = "GITHUBBOT"  # Optional, can be anything

    await client.room_send(
        room_id=ROOM_ID,
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": MESSAGE}
    )
    await client.close()

asyncio.run(main())
