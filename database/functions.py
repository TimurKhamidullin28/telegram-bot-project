from typing import Any, List
from database.common.models import User, History


def checkout_user(user_id: int) -> Any:
    res = User.get_or_none(User.user_id == user_id)
    return res


def user_history_info(user: User) -> List[History]:
    return user.history.order_by(-History.history_id).limit(20)
