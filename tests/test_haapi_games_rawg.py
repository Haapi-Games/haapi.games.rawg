"""Test cases for haapi.games.rawg."""
import json
import pathlib
from decimal import Decimal
from typing import List

import pytest
from aioresponses import aioresponses  # type: ignore
from urllib3.util import parse_url  # type: ignore

from haapi.games.rawg import RawGAPIAsync
from haapi.games.rawg.objects import Game


mock_api_key = "foo"
jotun_description_raw = (
    "The graphics solution of the game may seem simple at first glance, but"
    " in fact, it is very addictive and elaborated with the exceptional talent "
    "of the artist. Reminds the best samples from the history of world "
    "animation. There is an impression that the directors and operators of "
    "the highest Hollywood level worked on all the scenes in the game - "
    "the hero's simple passage through the hanging ladder suddenly turns into an "
    "exciting panorama that you want to admire for a long time. Voices speaking "
    "the ancient Scandinavian languages, and beautiful original music help to "
    "create a tangible atmosphere of Nordic folklore and adventure. These "
    "advantages draw attention to the game, despite the lack of continuous "
    "action. There is no such action in the game, but when it does happen, "
    "its epic nature is suited to the world of Nordic fairy tales. Plots of "
    "these tales and a description of the world of Nordic myths are adequately "
    "represented in the game, it is even possible to study this topic. "
    "The gameplay consists of exploring large levels, searching for runes to "
    "enter the next level, avoiding various exotic troubles and rare but "
    "epic and picturesque battles."
)


@pytest.mark.asyncio
async def test_get_game(shared_datadir: pathlib.Path) -> None:
    """JSON game is parsed into proper haapi.games.rawg.objects.game.

    Args:
        shared_datadir: tests/data
    """
    game_slug = "jotun"
    with aioresponses() as mock_response:
        with open((shared_datadir / "rawg_jotun.json"), "r") as read_file:
            payload = json.load(read_file)
        mock_response.get(
            f"https://api.rawg.io/api/games/{game_slug}?key={mock_api_key}",
            payload=payload,
        )
        foo: Game = await RawGAPIAsync(mock_api_key).get_game(game_slug)
        assert foo.id == 15274
        assert foo.slug == "jotun"
        assert foo.rating == Decimal("3.09")
        assert foo.metacritic == 79
        assert foo.esrb_rating is None
        assert foo.released is not None
        assert foo.released.year == 2015
        assert foo.released.month == 9
        assert foo.released.day == 29
        assert (
            foo.background_image == "https://media.rawg.io/media/games/"
            "032/0329db96e252aa41e672da2ba16f914c.jpg"
        )
        assert foo.description_raw == jotun_description_raw

        assert len(foo.genres) == 2
        for genre in foo.genres:
            assert genre.id == 4 or genre.id == 51
            if genre.id == 4:
                assert genre.name == "Action"
                assert genre.slug == "action"
                assert genre.games_count == 106489
                assert (
                    genre.image_background == "https://media.rawg.io/media/games/"
                    "f87/f87457e8347484033cb34cde6101d08d.jpg"
                )
            else:
                assert genre.name == "Indie"
                assert genre.slug == "indie"
                assert genre.games_count == 34336
                assert (
                    genre.image_background == "https://media.rawg.io/media/games/dd5/"
                    "dd50d4266915d56dd5b63ae1bf72606a.jpg"
                )

        assert foo.get_genres_list() == ["Action", "Indie"]
        assert foo.get_api_url() == parse_url("https://api.rawg.io/api/games/jotun")
        assert foo.get_rawg_url() == parse_url("https://rawg.io/games/jotun")
        assert (
            foo.get_description_with_max_length(1000)
            == jotun_description_raw[0:997] + "..."
        )
        assert foo.get_description_with_max_length() == jotun_description_raw


@pytest.mark.asyncio
async def test_search_games(shared_datadir: pathlib.Path) -> None:
    """JSON search returns proper List[haapi.games.rawg.objects.game].

    Args:
        shared_datadir: tests/data
    """
    game_search = "dyson sphere program"
    with aioresponses() as mock_response:
        with open(
            (shared_datadir / "games_search_dyson_sphere_program.json"),
            "r",
            encoding="utf8",
        ) as read_file:
            payload = json.load(read_file)
        mock_response.get(
            f"https://api.rawg.io/api/games?key={mock_api_key}&"
            f"search={game_search.replace(' ', '+')}"
            f"&search_precise=True",
            payload=payload,
        )
        games_return: List[Game] = await RawGAPIAsync(mock_api_key).search_games(
            game_search
        )

        assert games_return
        assert len(games_return) == 20

        best_game = games_return[0]
        assert best_game.slug == "dyson-sphere-program"
        assert best_game.name == "Dyson Sphere Program"
        assert best_game.id == 537744
        assert best_game.released is not None
        assert best_game.released.year == 2021
        assert best_game.released.month == 1
        assert best_game.released.day == 20
        assert best_game.rating == Decimal("0.0")
        assert best_game.metacritic is None
        assert best_game.esrb_rating is None
        assert (
            best_game.background_image == "https://media.rawg.io/media/screenshots/"
            "842/842ab43c709d2acb95691c927de9cb93.jpg"
        )
        assert best_game.description_raw is None  # search does not return a description
        assert len(best_game.genres) == 3
        for genre in best_game.genres:
            assert genre.id == 10 or genre.id == 51 or genre.id == 14

            if genre.id == 10:
                assert genre.name == "Strategy"
                assert genre.slug == "strategy"
            elif genre.id == 14:
                assert genre.name == "Simulation"
                assert genre.slug == "simulation"
            else:
                assert genre.name == "Indie"
                assert genre.slug == "indie"

            assert (
                genre.games_count is None
            )  # search does not return a games count for genres
            assert (
                genre.image_background is None
            )  # search does not return an image_background for genres
