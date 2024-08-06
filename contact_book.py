from collections import UserDict
from datetime import datetime, timedelta, date
import re


class Field:
    """Клас довільного поля, з чого складаються записи для контактної книги"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Поле імені"""

    def __init__(self, value: str):
        if value == '':
            raise ValueError("Name cannot be empty")
        else:
            super().__init__(value.lower())


class Phone(Field):
    """Поле телефонного номера"""

    def __init__(self, value: str):
        # Верифікація номера (має складатися з 10 цифр)
        if re.match(r'^\d{10}$', value):
            super().__init__(value)
        else:
            raise ValueError("Incorrect phone number")


class Birthday(Field):
    """Поле дня народження"""

    def __init__(self, value):
        try:
            # Верифікація дати
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Клас запису, з яких складатиметься контактна книга"""

    def __init__(self, name):
        # Обов'язкове поле ім'я та список телефонних номерів
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """Додавання номера телефона до запису

        Параметри:
            phone (str): Номер телефону
        """

        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видалення номера телефона із запису

        Параметри:
            phone (str): Номер телефону
        """

        # Змінна для збереження конкретного об'єкта зі списку для видалення (інакше - змінювати метод __eq__)
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, phone_old, phone_new):
        """Редагування номера телефона у записі

        Параметри:
            phone_old (str): Попередній номер телефону
            phone_new (str): Новий номер телефону
        """

        # Ітерація по значеннях Phone об'єктів у списку
        if phone_old in [phone.value for phone in self.phones]:
            self.remove_phone(phone_old)
            self.add_phone(phone_new)
        else:
            raise ValueError(f"Phone number {phone_old} not found")

    def find_phone(self, phone):
        """Пошук номера телефона в записі

        Параметри:
            phone (str): Номер телефону
        """

        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)


class AddressBook(UserDict):
    """Клас контактної книги"""

    def add_record(self, record: Record):
        """Додавання нового запису до контактної книги

        Параметри:
            record (Record): Запис для додавання
        """

        self.data[record.name.value] = record

    def delete(self, name):
        """Видалення запису з контактної книги

        Параметри:
            name (str): ім'я контакту для видалення
        """

        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact with name {name} not found")

    def find(self, name):
        """Пошук запису з контактної книги

        Параметри:
            name (str): ім'я контакту для пошуку
        """

        return self.data.get(name, None)

    def get_upcoming_birthdays(self, days=7):
        """Надає список з контактами для привітання найближчими днями

        Параметри:
            days(int): кількість днів для врахування (7 за замовчуванням)
        """

        # Перетворення рядка в datetime
        def string_to_date(date_string):
            return datetime.strptime(date_string, "%d.%m.%Y").date()

        # Перетворення datetime в рядок
        def date_to_string(date):
            return date.strftime("%d.%m.%Y")

        # Перетворення в підготовчий список з іменами та днями народження
        def prepare_user_list(user_data):
            prepared_list = []
            for key, value in user_data.items():
                if (birthday := value.birthday) is not None:
                    prepared_list.append({"name": key,
                                          "birthday": string_to_date(birthday.value)})
            return prepared_list

        # Пошук наступної дати коли настане заданий день тижня
        def find_next_weekday(start_date, weekday):
            days_ahead = weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return start_date + timedelta(days=days_ahead)

        # Врахування, що ми не можемо привітати у вихідний
        def adjust_for_weekend(birthday):
            if birthday.weekday() >= 5:
                return find_next_weekday(birthday, 0)
            return birthday

        upcoming_birthdays = []
        today = date.today()

        users = prepare_user_list(self.data)
        # Зміна року на той, що зараз
        for user in users:
            birthday_this_year = user["birthday"].replace(year=today.year)
            # Якщо в цьому році дата вде минула, переходимо на наступний
            if birthday_this_year < today:
                birthday_this_year = user["birthday"].replace(year=today.year + 1)
            # Перехід на наступний робочий день, якщо припадає на вихідний
            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = adjust_for_weekend(birthday_this_year)
                congratulation_date_str = date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": user["name"], "congratulation_date": congratulation_date_str})
        return upcoming_birthdays

    def __str__(self):
        decoration = '-'*max([len(str(record)) for record in self.data.values()])
        return decoration + '\n' + "\n".join(str(record) for record in self.data.values()) + '\n' + decoration

