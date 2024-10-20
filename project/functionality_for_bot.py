"""Functionality for the console bot helper (2.0), which recognizes commands entered from the keyboard, and responds according to the entered command."""
from collections import UserDict
from datetime import datetime, timedelta


class ValidationError(Exception):
    pass


class Field:
    """Base class for record fields."""

    def __init__(self, value: str | datetime):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing contact names."""
    pass


class Phone(Field):
    """Class for storing phone numbers. Validates that the format is 10 digits."""

    def __init__(self, value: str):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValidationError('The phone must have 10 numbers.')


class Birthday(Field):
    """Class for storing birth dates in the format DD.MM.YY."""

    def __init__(self, value: str):
        try:
            birthday = datetime.strptime(value, '%d.%m.%Y')
            super().__init__(self.__validation(birthday))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    @staticmethod
    def __validation(birthday: datetime) -> datetime:
        """Validates the input date."""
        now = datetime.now()
        if birthday.date() <= now.date():
            return birthday
        else:
            raise ValidationError('Incorrect date.')

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')


class Record:
    """Class for storing contact information, including name, phone numbers, and birthday."""

    def __init__(self, name: str, phone: str = None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = None

    def add_birthday(self, birthday: str):
        """Adds a birthday."""
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str):
        """Adds a phone number."""
        if self.find_phone(phone) is None:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """Removes a phone number."""
        i = [v.value for v in self.phones].index(Phone(phone).value)
        self.phones.pop(i)

    def edit_phone(self, old_phone: str, new_phone: str):
        """Edits a phone number."""
        i = [v.value for v in self.phones].index(Phone(old_phone).value)
        if self.find_phone(new_phone) and old_phone != new_phone:
            self.remove_phone(old_phone)
        else:
            self.phones[i] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        """Finds a phone number."""
        res = [p for p in self.phones if p.value == Phone(phone).value]
        if not res:
            return None
        return res[0]

    def __str__(self):
        return (f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)},"
                f" birthday: {str(self.birthday)}")


class AddressBook(UserDict):
    """Class for storing and managing records."""

    def get_upcoming_birthdays(self) -> list[dict]:
        """Determines contacts with birthdays within the next 7 days."""
        now = datetime.now()
        res = []
        for rec in self.data.values():
            if rec.birthday is None:
                continue

            birthday = rec.birthday.value.replace(year=now.year)
            if birthday.date() < now.date():
                birthday = birthday.replace(year=now.year + 1)

            if 0 <= birthday.toordinal() - now.toordinal() <= 7:
                weekday = birthday.weekday()
                if weekday == 5 or weekday == 6:
                    days = 7 - weekday
                    birthday = birthday + timedelta(days=days)
                birthday = birthday.strftime('%d.%m.%Y')
                res.append({'name': str(rec.name), 'birthday': birthday})
        return res

    def add_record(self, record: Record):
        """Adds a record."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """Finds a record by name."""
        return self.data.get(name)

    def delete(self, name: str):
        """Deletes a record by name. """
        self.data.pop(name)

    def __str__(self):
        res = ''
        count_rec = 1
        for key in self.data:
            res += f'{count_rec}. {self.data[key]};\n'
            count_rec += 1
        return res
