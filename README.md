[![Flake8](https://github.com/ArtichaTM/workmate_test/actions/workflows/flake8.yml/badge.svg)](https://github.com/ArtichaTM/workmate_test/actions/workflows/flake8.yml)
[![Coverage](https://coveralls.io/repos/github/ArtichaTM/workmate_test/badge.svg)](https://coveralls.io/github/ArtichaTM/workmate_test)
[![Tests](https://github.com/ArtichaTM/workmate_test/actions/workflows/tests.yml/badge.svg)](https://github.com/ArtichaTM/workmate_test/actions/workflows/tests.yml)

# Описание
Работа выполнялась с целью упрощения расширения функционала в сторону каких-то статистик или добавления новых `float|int|date` колонок.
- Колонка `name` (в csv `student`) стала обязательной как primary key.
- Приложение построен с помощью [uv](docs.astral.sh/uv), однако можно и воспользоваться pip
- Минимальный python 3.10 (можно было попробовать и ниже, функционал базовый)
- Используется архитектура пакетов python, поэтому возможна загрузка в pypi, Что даже проще через [uv](https://docs.astral.sh/uv/guides/package/)
- Используется библиотека `pre-commit` (устанавливается только при `uv sync --dev`) с flake8 и isort

## Примерные команды запуска
```bash
uv run -m csv_printer --files temp/math.csv temp/physics.csv  # Запускает компиляцию отчётов в колонки по умолчанию `name, mean_coffee_spent`
python -m csv_printer --files temp/math.csv temp/physics.csv  # Аналог команды выше
```

# Примечания
## Неодновременная сдача экзаменов
По исходным данным, все экзамены проходят все студенты одновременно, например:
```
Мария Соколова,2024-06-01,100,8.0,3,отл,Математика
Мария Соколова,2024-06-02,120,8.5,2,отл,Математика
Мария Соколова,2024-06-03,150,7.5,4,отл,Математика
Павел Новиков,2024-06-01,380,5.0,10,норм,Математика
Павел Новиков,2024-06-02,420,4.5,11,устал,Математика
Павел Новиков,2024-06-03,470,4.0,13,устал,Математика
```

Однако в библиотеке предполагается, что это может быть не так

## Обязательное колонка
Имя считается обязательной колонкой (*primary key*), которую нельзя исключить


## Указание обычных колонок при агрегации
Экзаменов много, а имя одно. Если указывается обычное поле, выдаётся предупреждение и колонка пропускается