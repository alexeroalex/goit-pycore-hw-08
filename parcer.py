"""
    Форматує рядок введений користувачем під програму.

    Параметри:
    user_input (str): Рядок із запитом.

    Повертає:
    tuple[str]: Кортеж з назвою команди користувача та списком наступних введених ним аргументів.
    """


def parse_input(user_input):
    if not user_input:
        return ['', '']
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args
