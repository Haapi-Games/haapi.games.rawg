"""Haapi Games Async Rawg API."""
from typing import List

import aiohttp
import desert
import marshmallow

from haapi.games.rawg.constants import BASE_API_URL
from haapi.games.rawg.objects import Game


class RawGAPIAsync:
    """Async RawG API."""

    def __init__(self, api_key: str) -> None:
        """Initialize RawGAPIAsync with api_key.

        Args:
            api_key: api_key for RawG. See https://rawg.io/apidocs
        """
        self.api_key = api_key
        self._game_schema_class = desert.schema_class(
            Game, meta={"unknown": marshmallow.EXCLUDE}
        )

    async def search_games(self, search_string: str) -> List[Game]:
        """Simple search of rawg games.

        Passes search={search_string} and search_precise=True as parameters

        Args:
            search_string: search to send to rawg

        Returns:
            List of games matching search
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self._get_url("games")}&search={search_string}&search_precise={True}'
            ) as response:
                json_response = await response.json()
                game_schema = self._game_schema_class()
                found_games: List[Game] = game_schema.load(
                    json_response["results"], many=True
                )
                return found_games

    def _get_url(self, path: str) -> str:
        """Get URL with API key already included.

        Args:
            path: the full path for the URL of rawg

        Returns:
            str {RawGAsync.BASE_URL}/{path}?key={self.api_key}

        """
        return f"{BASE_API_URL}/{path}?key={self.api_key}"

    async def get_game(self, slug: str) -> Game:
        """Gets game based on slug.

        Args:
            slug: game slug for rawg game

        Returns:
            Game for slug

        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self._get_url("games/" + slug)}') as response:
                json_response = await response.json()
                game_schema = self._game_schema_class()
                found_game: Game = game_schema.load(json_response)
                return found_game
