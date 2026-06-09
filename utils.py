SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

# center of word frame of referance
WORLD_0X = SCREEN_WIDTH // 2
WORLD_0Y = SCREEN_HEIGHT - 10

HEART_EVENT = 32867
FLY_EVENT = 32869
ITEM_ON_GROUND_EVENT = 32868
UPDATE_PET_EVENT = 32870

ITEM_CHOSEN = None

MAX_HEALTH = 5


def world_to_screen(x, y):
    px = x + WORLD_0X
    py = WORLD_0Y - y
    return (px, py)


def screen_to_word(px, py):
    x = px - WORLD_0X
    y = WORLD_0Y - py
    return (x, y)


def calculateFoodToGive(db):
    return len([item for item in db.get_tasks_cached() if item["status"] == "done"])


def calculate_energy(db):
    penalty = sum(
        5 if task["status"] in ("todo", "done")
        else 10 if task["status"] == "expired"
        else 0
        for task in db.get_tasks_cached()
    )

    return max(100 - penalty, 0)


def getPetName(db):
    return db.pet_cache['name'] if db.pet_cache else ""


def calculateMood(energy: int):
    if energy < 10:
        return 'sleepy'
    if energy < 50:
        return 'sad'
    if energy < 80:
        return 'neutral'

    return 'happy'


async def decreaseTasks(db):
    done_task = next(
        (task for task in db.tasks_cache.values()
         if task["status"] == "done"),
        None
    )

    if done_task is None:
        return False

    task_id = done_task["id"]

    print(done_task)

    await (
        db.table("tasks")
        .update({"status": "exhausted"})
        .eq("id", task_id)
        .execute()
    )

    userID = done_task["assigned_to_user_id"]

    await db.add_points_to_user(userID, 10)

    return True
