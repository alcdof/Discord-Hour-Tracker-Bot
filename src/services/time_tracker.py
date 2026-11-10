import datetime

times = {}


def start_tracking(user_id):
    times[user_id] = datetime.datetime.now()


def stop_tracking(user_id):
    times.pop(user_id, None)


def get_elapsed_time(user_id):
    if user_id not in times:
        return None

    elapsed = datetime.datetime.now() - times[user_id]
    return int(elapsed.total_seconds())