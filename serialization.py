import pickle
from contact_book import AddressBook


def save_data(book, filename="addressbook.pkl"):
    """Зберігає об'єкт контактної книги за допомогою модуля pickle.

            Параметри:
            book (AddressBook): Контактна книга із записами.
            filename (str): Шлях до файла, в який треба зберегти дані
                            ("addressbook.pkl" за замовчуванням).
            """

    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """Завантажує об'єкт контактної книги з попередньої сесії за допомогою модуля pickle.

                Параметри:
                book (AddressBook): Контактна книга із записами.
                filename (str): Шлях до файла, з якого завантажується книга
                                ("addressbook.pkl" за замовчуванням).
                """

    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
