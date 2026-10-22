import os

from game.clicker import RandomClicker
from game.exceptions import NotEnoughMoney
from game.game import Game
from game.models import Food, Medicine
from game.tamagochi import Tamagochi

MIN_INCOME = 10
MAX_INCOME = 20


def main() -> None:
    """Запускает игровой цикл и обрабатывает команды игрока"""
    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Салат", satiety=10, price=20),
        Food(name="Яблоко", satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(name="Ибупрофен", price=30, heal_hp=20, number_of_uses=2),
    ]

    tamagochi = Tamagochi()
    clicker = RandomClicker(MIN_INCOME, MAX_INCOME)
    game = Game(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )
    print("Добро пожаловать в Тамагочи-кликер!")
    output = ""

    while game.tamagochi.is_alive():
        print(output)

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(
            f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, "
            f"энергия {status['energy']}, монет {status['coins']}\n"
        )
        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")

        try:
            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f"Вы заработали {income} монет"
                case "2":
                    game.buy_food()
                    output = "Вы купили еду"
                case "3":
                    game.buy_medicine()
                    output = "Вы купили лекарство"
                case "4":
                    game.feed_tamagochi()
                    output = "Вы покормили питомца"
                case "5":
                    game.heal_tamagochi()
                    output = "Вы вылечили питомца"
                case "6":
                    game.play_with_tamagochi()
                    output = "Вы поиграли с питомцем"
                case "7":
                    game.rest_tamagochi()
                    output = "Питомец отдохнул"
                case "0":
                    break
                case _:
                    output = "Неверная команда"
        except (NotEnoughMoney, ValueError) as error:
            output = str(error)

        os.system("clear")

    if not game.tamagochi.is_alive():
        print("Тамагочи погиб. Игра окончена")


if __name__ == "__main__":
    main()
