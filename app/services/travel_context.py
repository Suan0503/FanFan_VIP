from __future__ import annotations


travel_awaiting_location: dict[str, bool] = {}
travel_last_location: dict[str, tuple[float, float]] = {}


def mark_awaiting_location(user_id: str) -> None:
    travel_awaiting_location[user_id] = True


def consume_awaiting_location(user_id: str) -> bool:
    if not travel_awaiting_location.get(user_id):
        return False
    travel_awaiting_location.pop(user_id, None)
    return True


def set_last_location(user_id: str, latitude: float, longitude: float) -> None:
    travel_last_location[user_id] = (latitude, longitude)


def get_last_location(user_id: str) -> tuple[float, float] | None:
    return travel_last_location.get(user_id)
