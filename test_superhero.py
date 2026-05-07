import pytest
from unittest.mock import patch
from superhero import get_tallest_hero, fetch_heroes
@pytest.fixture
def fake_heroes():
    return [
        {
            "id": 1, "name": "Tall Male Worker",
            "appearance": {"gender": "Male", "height": ["7'0", "213 cm"]},
            "work": {"occupation": "Engineer"}
        },
        {
            "id": 2, "name": "Short Male Worker",
            "appearance": {"gender": "Male", "height": ["5'5", "165 cm"]},
            "work": {"occupation": "Doctor"}
        },
        {
            "id": 3, "name": "Male No Work",
            "appearance": {"gender": "Male", "height": ["6'5", "196 cm"]},
            "work": {"occupation": "-"}
        },
        {
            "id": 4, "name": "Tall Female Worker",
            "appearance": {"gender": "Female", "height": ["6'2", "188 cm"]},
            "work": {"occupation": "Scientist"}
        },
        {
            "id": 5, "name": "Female No Work",
            "appearance": {"gender": "Female", "height": ["5'9", "175 cm"]},
            "work": {"occupation": "-"}
        },
        {
            "id": 6, "name": "Bad Height Hero",
            "appearance": {"gender": "Male", "height": ["0'0", "0 cm"]},
            "work": {"occupation": "Hero"}
        },
    ]


def test_tallest_male_with_work(fake_heroes):
    hero = get_tallest_hero("Male", True, heroes=fake_heroes)
    assert hero["name"] == "Tall Male Worker"


def test_tallest_male_without_work(fake_heroes):
    hero = get_tallest_hero("Male", False, heroes=fake_heroes)
    assert hero["name"] == "Male No Work"


def test_tallest_female_with_work(fake_heroes):
    hero = get_tallest_hero("Female", True, heroes=fake_heroes)
    assert hero["name"] == "Tall Female Worker"


def test_tallest_female_without_work(fake_heroes):
    hero = get_tallest_hero("Female", False, heroes=fake_heroes)
    assert hero["name"] == "Female No Work"


def test_gender_case_insensitive(fake_heroes):
    hero = get_tallest_hero("male", True, heroes=fake_heroes)
    assert hero["name"] == "Tall Male Worker"

def test_no_match_returns_none(fake_heroes):
    result = get_tallest_hero("Unknown", True, heroes=fake_heroes)
    assert result is None


def test_empty_heroes_list_returns_none():
    assert get_tallest_hero("Male", True, heroes=[]) is None


def test_invalid_gender_type(fake_heroes):
    with pytest.raises(TypeError):
        get_tallest_hero(123, True, heroes=fake_heroes)


def test_invalid_has_work_type(fake_heroes):
    with pytest.raises(TypeError):
        get_tallest_hero("Male", "yes", heroes=fake_heroes)


def test_zero_height_excluded(fake_heroes):
 
    hero = get_tallest_hero("Male", True, heroes=fake_heroes)
    assert hero["id"] != 6


def test_real_api_returns_hero():
    hero = get_tallest_hero("Male", True)
    assert hero is not None
    assert "name" in hero
    assert hero["appearance"]["gender"].lower() == "male"


def test_fetch_heroes_called_when_no_list_passed(fake_heroes):
    with patch("superhero.fetch_heroes", return_value=fake_heroes) as mock_fetch:
        hero = get_tallest_hero("Male", True)
        mock_fetch.assert_called_once()
        assert hero["name"] == "Tall Male Worker"