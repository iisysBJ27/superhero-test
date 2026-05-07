import requests

API_URL = "https://akabab.github.io/superhero-api/api/all.json"


def fetch_heroes(url: str = API_URL) -> list:
    """Загружает список героев из API."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_tallest_hero(gender: str, has_work: bool, heroes: list = None) -> dict | None:
    """
    Возвращает самого высокого героя по полу и наличию работы.

    :param gender: "Male" или "Female" (регистр неважен)
    :param has_work: True — есть работа, False — нет работы
    :param heroes: список героев (если не передан, тянется из API)
    :return: словарь героя или None, если никто не подошёл
    """
    if not isinstance(gender, str):
        raise TypeError("gender must be a string")
    if not isinstance(has_work, bool):
        raise TypeError("has_work must be a bool")

    if heroes is None:
        heroes = fetch_heroes()

    gender_normalized = gender.strip().lower()

    def has_occupation(hero: dict) -> bool:
        occupation = hero.get("work", {}).get("occupation", "-")
        return occupation not in ("-", "", None)

    def height_cm(hero: dict) -> float:
        # height = ["6'0", "183 cm"]
        height_list = hero.get("appearance", {}).get("height", ["", ""])
        if len(height_list) < 2:
            return 0.0
        cm_str = height_list[1].replace("cm", "").strip()
        try:
            return float(cm_str)
        except ValueError:
            return 0.0

    filtered = [
        h for h in heroes
        if h.get("appearance", {}).get("gender", "").lower() == gender_normalized
        and has_occupation(h) == has_work
        and height_cm(h) > 0
    ]

    if not filtered:
        return None

    return max(filtered, key=height_cm)


if __name__ == "__main__":
    hero = get_tallest_hero("Male", True)
    if hero:
        print(f"{hero['name']} — {hero['appearance']['height'][1]}")
    else:
        print("Не найдено")