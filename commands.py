from contact_book import AddressBook, Record


def input_error(func):
    """Декоратор для handler функцій"""
    def inner(*args, **kwargs):
        """Перевіряє наявність KeyError, ValueError, IndexError в будь-якій з команд.

            Параметри:
                args (list[str]): Позиційні аргументи функції.
                kwargs (dict): Ключові аргументи функції.

            Повертає:
                str: Повідомлення про помилку.
            """

        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please indicate the required arguments"
        except KeyError:
            return "No such contact found."
        except IndexError:
            return "Please indicate the required arguments"
        except AttributeError:
            return "No such contact found."

    return inner


@input_error
def add_contact(args, book: AddressBook):
    """Додає контакт до книги.

        Параметри:
        args (list[str]): Список з іменем та номером бажаного контакту.
        book (AddressBook): Контактна книга із записами.

        Повертає:
        str: Результат додавання контакту.
        """

    name, phone, *_ = args
    record: Record = book.find(name)
    message = "Contact updated."
    if record is None:
        record: Record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    """Змінює номер телефону контакту у книзі.

        Параметри:
        args (list[str]): Список з іменем та номером бажаного контакту.
        book (AddressBook): Контактна книга із записами.

        Повертає:
        str: Результат зміни контакту або результат невдачі.
        """

    name, old_phone, new_phone, *_ = args

    record: Record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact changed"


@input_error
def phone_contact(args, book: AddressBook):
    """ "Телефонує" заданому контакту з книги.

        Параметри:
        args (list[str]): Список з іменем бажаного контакту.
        book (AddressBook): Контактна книга із записами.

        Повертає:
        list[str]: Список номерів телефонів контакту або результат невдачі.
        """

    name, *_ = args
    return [str(phone) for phone in book.find(name).phones]


@input_error
def show_contact(args, book: AddressBook):
    """Відображає номер телефону контакту у книзі.

        Параметри:
        args (list[str]): Список з іменем бажаного контакту.
        book (AddressBook): Контактна книга із записами.

        Повертає:
        Record: Запис контакту або результат невдачі.
        """

    name, *_ = args
    return book.find(name)


@input_error
def delete_contact(args, book: AddressBook):
    """Видаляє контакт у книзі.

        Параметри:
        args (list[str]): Список з іменем бажаного контакту.
        book (AddressBook): Контактна книга із записами.

        Повертає:
        str: Результат видалення контакту або результат невдачі.
        """

    name, *_ = args
    book.delete(name)
    return "Contact deleted."


@input_error
def add_birthday(args, book: AddressBook):
    """Додає дату народження контакту у книзі.

        Параметри:
        args (list[str]): Список з іменем та датою народження бажаного контакту.
        book (AddressBook): Контактна книга із записами.

        Повертає:
        str: Результат додавання контакту або результат невдачі.
        """

    name, birthday, *_ = args
    record: Record = book.find(name)
    record.add_birthday(birthday)
    return "Contact's birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    """Відображає дату народження контакту у книзі.

        Параметри:
        args (list[str]): Список з іменем та датою народження бажаного контакту.
        book (AddressBook): Контактна книга із записами.

        Повертає:
        Birthday: Поле дня народження або результат невдачі.
        """

    name, *_ = args
    record: Record = book.find(name)
    return record.birthday


@input_error
def birthdays(book: AddressBook):
    """Відображає імена контактів та дату, коли їх треба привітати з днем народження.

            Параметри:
            book (AddressBook): Контактна книга із записами.

            Повертає:
            dict: Словник з іменами як ключі та датами привітання як значення або результат невдачі.
            """

    return book.get_upcoming_birthdays()
