# Імпорт модулів з реалізованими командами та парсером
import parcer as p
import commands as cmd
from contact_book import AddressBook
from serialization import load_data, save_data


def main():
    """Функція main з усією логікою інтерфейсу бота для обробки телефонної книги."""

    print("Welcome to the assistant bot!")
    book = load_data()  # Завантаження даних з pkl файлу

    # Запуск циклу обробки введеного користувачем запита.
    while True:
        user_input = input().strip().lower()
        # Форматування запиту для отримання параметрів команди.
        command, parsed_input = p.parse_input(user_input)

        # Виконання команди з перевіркою її валідності
        try:
            # Привітання
            if command == 'hello':
                print("How can I help you?")

            # Додавання контакту або номера телефону до нього
            elif command == 'add':
                print(cmd.add_contact(parsed_input, book))

            # Зміна контакту
            elif command == 'change':
                print(cmd.change_contact(parsed_input, book))

            # Відображення контакту
            elif command == 'phone':
                print(cmd.phone_contact(parsed_input, book))

            # Видалення контакту
            elif command == 'delete':
                print(cmd.delete_contact(parsed_input, book))

            # Виведення контакту за іменем
            elif command == 'show':
                print(cmd.show_contact(parsed_input, book))

            # Додавання дня народження контакту
            elif command == 'add-birthday':
                print(cmd.add_birthday(parsed_input, book))

            # Відображення дня народження контакту
            elif command == 'show-birthday':
                print(cmd.show_birthday(parsed_input, book))

            # Список з контактами для привітання
            elif command == 'birthdays':
                print(cmd.birthdays(book))

            # Виведення всієї книги
            elif command == 'all':
                print(book)

            # Вихід з бота
            elif user_input == 'exit' or user_input == 'close':
                save_data(book)  # Збереження книги перед виходом
                print("Good bye!")
                exit(0)

            else:
                print("Invalid command.")

        except ValueError as ve:
            print(f"Error: {ve}")


# Виклик функції main, якщо скрипт запущений як основне завдання.
if __name__ == "__main__":
    main()
