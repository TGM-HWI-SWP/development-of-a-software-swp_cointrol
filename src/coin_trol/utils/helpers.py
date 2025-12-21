def find_user_by_name(name: str) -> int | None:
    """Sucht nach einem Benutzer und gibt seine ID zurück."""
    from coin_trol.model.database import USERS
    for user in USERS:
        if user.name.lower() == name.lower():
            return user.user_id
    return None
