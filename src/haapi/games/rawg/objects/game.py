"""Haapi Games Rawg Game."""
import dataclasses
import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict, Optional, Any

import desert
import marshmallow
from urllib3.util import Url, parse_url  # type: ignore

from haapi.games.rawg.constants import BASE_RAWG_URL, BASE_API_URL
from haapi.games.rawg.objects.genre import Genre


@dataclass
class Game:
    """RawG Game.

    Currently only has attributes that are used by other projects.
    See https://api.rawg.io/docs/#operation/games_read for more attributes
    """

    id: int
    slug: str
    name: str
    genres: List[Genre]
    rating: Decimal
    released: Optional[datetime.datetime] = dataclasses.field(
        default=None,
        metadata=desert.metadata(field=marshmallow.fields.DateTime("%Y-%m-%d")),
    )
    background_image: Optional[str] = dataclasses.field(
        default=None,
        metadata=desert.metadata(field=marshmallow.fields.Url()),
    )
    esrb_rating: Optional[Dict[Any, Any]] = None
    description_raw: Optional[str] = None
    metacritic: Optional[int] = None

    def get_description_with_max_length(self, max_length: int = 2048) -> Optional[str]:
        """Get description capping at a certain length.

        Useful for Discord messages or Embeds to make sure it isn't too large

        Args:
            max_length: the length to max at

        Returns:
            description raw at max length if too large
        """
        if self.description_raw is not None and len(self.description_raw) > max_length:
            return self.description_raw[0 : max_length - 3] + "..."
        else:
            return self.description_raw

    def get_rawg_url(self) -> Url:
        """The website URL for this game.

        Returns:
            rawg.io/{slug} Url
        """
        return parse_url(f"{BASE_RAWG_URL}/games/{self.slug}")

    def get_api_url(self) -> Url:
        """The API URL for this game.

        Returns:
            api.rawg.io/{slug} Url
        """
        return parse_url(f"{BASE_API_URL}/games/{self.slug}")

    def get_genres_list(self) -> List[str]:
        """Get just the genres strings not ID's.

        Returns:
            List[str] of genre names
        """
        return [genre.name for genre in self.genres]
