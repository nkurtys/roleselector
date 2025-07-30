import random
import json
from collections import defaultdict
from nio import AsyncClient
import os
import asyncio

HOMESERVER = "https://matrix.org"
USER_ID = os.environ["MATRIX_USER_ID"]
ACCESS_TOKEN = os.environ["MATRIX_TOKEN"]
ROOM_ID = os.environ["MATRIX_ROOM_ID"]

# Load people from people.json
with open("src/people.json", encoding="utf-8") as f:
    people_data = json.load(f)
people = [p["name"] for p in people_data]

roles = ['Moderator', 'Notetaker', 'Timekeeper', 'Speaker']

# Load previous weeks from weeks.json
try:
    with open("src/weeks.json", encoding="utf-8") as f:
        weeks_data = json.load(f)
except FileNotFoundError:
    weeks_data = []

# Track role counts per person
role_counts = defaultdict(lambda: defaultdict(int))
last_week = set()

# Populate role_counts and last_week from weeks_data
if weeks_data:
    for week in weeks_data:
        for entry in week["people"]:
            role_counts[entry["name"]][entry["role"]] += 1
    last_week = set(entry["name"] for entry in weeks_data[-1]["people"])

def assign_roles():
    global last_week
    # Pick 4 people not in last week's group
    candidates = [p for p in people if p not in last_week]
    if len(candidates) < 4:
        candidates = people.copy()
    selected = random.sample(candidates, 4)

    # For each role, assign to the selected person who has done it the least
    assignments = []
    used = set()
    for role in roles:
        # Find the selected person with the fewest times in this role, not already assigned this week
        min_count = min(role_counts[p][role] for p in selected if p not in used)
        candidates_for_role = [p for p in selected if p not in used and role_counts[p][role] == min_count]
        person = random.choice(candidates_for_role)
        assignments.append({"name": person, "role": role})
        role_counts[person][role] += 1
        used.add(person)

    last_week = set([a["name"] for a in assignments])
    return assignments

def get_message(new_week):
    msg = f"**Week {new_week['week']} Role Assignments:**\n"
    for entry in new_week["people"]:
        msg += f"- {entry['role']}: {entry['name']}\n"
    return msg

if __name__ == "__main__":
    new_week = {
        "week": len(weeks_data) + 1,
        "people": assign_roles()
    }
    weeks_data.append(new_week)
    with open("src/weeks.json", "w", encoding="utf-8") as f:
        json.dump(weeks_data, f, indent=4, ensure_ascii=False)

    print(json.dumps(new_week, indent=4, ensure_ascii=False))

    # Send to Matrix if credentials are set
    MESSAGE = get_message(new_week)

    async def main():
        if not all([HOMESERVER, USER_ID, ACCESS_TOKEN, ROOM_ID]):
            print("Matrix credentials not set. Skipping Matrix message.")
            return
        client = AsyncClient(HOMESERVER, USER_ID)
        client.access_token = ACCESS_TOKEN
        client.user_id = USER_ID
        client.device_id = "rolesBOT"

        await client.room_send(
            room_id=ROOM_ID,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": MESSAGE}
        )
        await client.close()

    asyncio.run(main())