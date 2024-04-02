import re
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Invalid phone number format. It should contain 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        if old_phone not in [str(p) for p in self.phones]:       # Чи існує старий номер телефону
            raise ValueError("Old phone number does not exist.")
        try:
            new_phone = Phone(new_phone)  # перевырка нового номеру
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        except ValueError as e:
            raise ValueError("Invalid new phone number format.") from e

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None
    
    #def find_phone(self, phone):
        #return phone if Phone(phone) in self.phones else None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        del self.data[name]

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            if isinstance(e, KeyError):
                return "No contact found with this name."
            elif isinstance(e, ValueError):
                return "Invalid input. Please provide a valid input."
            elif isinstance(e, IndexError):
                return "Invalid number of arguments. Please provide the correct number of arguments."
            else:
                return "An error occurred while processing your request."
    return wrapper

def main():
    book = AddressBook()

    while True:
        user_input = input("Enter a command (add, find, delete, exit): ").strip().lower()

        if user_input == "exit":
            print("Goodbye!")
            break
        elif user_input == "add":
            name = input("Enter the name: ").strip()
            record = Record(name)
            while True:
                phone = input("Enter the phone number (10 digits): ").strip()
                try:
                    record.add_phone(phone)
                    add_more = input("Do you want to add another phone number? (yes/no): ").strip().lower()
                    if add_more != "yes":
                        break
                except ValueError as e:
                    print(e)
            book.add_record(record)
            print("Contact added.")
        elif user_input == "find":
            name = input("Enter the name to find: ").strip()
            record = book.find(name)
            if record:
                print(record)
            else:
                print("Contact not found.")
        elif user_input == "delete":
            name = input("Enter the name to delete: ").strip()
            if name in book.data:
                book.delete(name)
                print("Contact deleted.")
            else:
                print("Contact not found.")
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
