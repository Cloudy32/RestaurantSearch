from app.db.models.favorite import Favorite

from app.repositories.favorite_repo import FavoriteRepository


class FavoriteService:

    def __init__(self, repository: FavoriteRepository) -> None:
        self.repository = repository

    async def get_or_create_favorite(self, user_id: int, restaurant_id: int) -> Favorite:

        favorite = await self.repository.get_by_user_and_restaurant(user_id, restaurant_id)

        if favorite:
            return favorite

        created_favorite = await self.repository.create_favorite(user_id, restaurant_id)
        return created_favorite

    async def get_all(self, user_id: int) -> list[Favorite]:

        all_favorite = await self.repository.get_all_favorites(user_id)
        return all_favorite

    async def remove_favorite(self, user_id: int, restaurant_id: int) -> bool:

        favorite = await self.repository.get_by_user_and_restaurant(user_id, restaurant_id)

        if favorite is None:
            return False

        await self.repository.delete_favorite(favorite)
        return True

