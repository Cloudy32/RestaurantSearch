from app.db.models.user import User

from app.repositories.user_repo import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_or_create_user(
            self,
            telegram_id: int,
            username: str | None,
            first_name: str | None
    ) -> User:

        user = await self.repository.get_by_tg_id(telegram_id)

        if user:
            return user

        created_user = await self.repository.create_user(telegram_id, username, first_name)
        return created_user