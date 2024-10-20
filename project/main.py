"""Console bot helper (2.0) that recognizes commands entered from the keyboard,
                                    and responds according to the entered command."""

from project.functionality_for_bot import AddressBook, Record, ValidationError
import pickle


def save_data(book: AddressBook, filename: str = "addressbook.pkl"):
    """
    Saves the notebook(book) to the file(filename).

    :param book: Record book to store.
    :param filename: Name of the file to save.
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """
    Downloading a notebook from a file (filename).

    :param filename: The name of the file to download.
    :return: Saved notebook on successful download.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    """Decorator for handling exceptions."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as ex:
            return ex
        except (ValueError, IndexError) as ex:
            if str(ex)[1:11].isdigit() or str(ex).startswith('Invalid date'):
                return str(ex) + '.'
            else:
                return 'Enter the argument for the command.'
        except (AttributeError, KeyError):
            return 'Contact not found.'

    return inner


@input_error
def parse_input(user_input: str) -> tuple[str, str] | str:
    """
    Parser of user-driven commands from the console.

    :param user_input:
    :return: A tuple with processed user input.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Adds a contact to the notebook.

    :param args: List with user input.
    :param book: Desired notebook.
    :return: The login string for the user.
    """

    name, phone = args[:2] if len(args[:2]) == 2 else (args[0], None)
    record = book.find(name)
    msg = 'Contact update.'
    if record is None:
        record = Record(name)
        book.add_record(record)
        msg = 'Contact added.'
    if phone:
        record.add_phone(phone)
    return msg


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """
    Changes the phone number.

    :param args: List with user input.
    :param book: Desired notebook.
    :return: The login string for the user.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return 'Contact changed.'


@input_error
def remove_phone(args: list[str], book: AddressBook) -> str:
    """
    Deletes a phone number.

    :param args: List with user input.
    :param book: Desired notebook.
    :return: The login string for the user.
    """
    name, phone, *_ = args
    record = book.find(name)
    record.remove_phone(phone)
    return 'Phone remove.'


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """
    Deletes a contact.

    :param args: List with user input.
    :param book: Desired notebook.
    :return: The login string for the user.
    """
    name, *_ = args
    book.delete(name)
    return 'Contact delete.'


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """
    Returns the phone numbers of the desired contact.

    :param args: List with user input.
    :param book: Desired notebook.
    :return: A string with phone numbers.
    """
    name, *_ = args
    record = book.find(name)
    return f'Phones: {'; '.join(str(p) for p in record.phones)}'


@input_error
def show_all_contacts(book: AddressBook) -> AddressBook:
    """
    Returns a notebook for printing all entries.

    :param book: Desired notebook.
    :return: An address book object of type AddressBook.
    """
    return book


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """
    Adds a date of birth to a contact.

    :param args: List with user input.
    :param book: Desired notebook.
    :return: The login string for the user.
    """
    name, birthday, *_ = args
    record = book.find(name)
    msg = 'Birthday update.'
    if record.birthday is None:
        msg = 'Birthday added.'
    record.add_birthday(birthday)
    return msg


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """
    Returns the birthday of the desired contact.

    :param args: List with user input.
    :param book: Desired notebook.
    :return: A string with the date of birth.
    """
    name, *_ = args
    record = book.find(name)
    return f'Birthday: {str(record.birthday)}'


@input_error
def birthdays(book: AddressBook) -> str:
    """
    Identifies contacts whose birthday is 7 days ahead of the current day.

    :param book: Desired notebook.
    :return: A string with the greeting names and dates.
    """
    res = ''
    count_rec = 1
    for d in book.get_upcoming_birthdays():
        res += f'{count_rec}. Contact name: {d['name']}, birthday: {d['birthday']};\n'
        count_rec += 1
    return res


def main():
    """Main function."""
    book = load_data()
    print('Welcome to the assistant bot!')
    while True:
        user_input = input('Enter a command:')
        command, *args = parse_input(user_input)

        if command in ['close', 'exit']:
            print('Good bye!')
            break
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'remove-phone':
            print(remove_phone(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'all':
            print(show_all_contacts(book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthdays':
            print(birthdays(book))
        elif command == 'delete':
            print(delete_contact(args, book))
        else:
            print('Invalid command.')

    save_data(book)


if __name__ == '__main__':
    main()
