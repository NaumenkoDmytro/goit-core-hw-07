from collections import UserDict
from datetime import datetime, date

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
		pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("The number is not valid!")
        super().__init__(value)
        self.value = value


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

                             
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_birthday(self, value):
        self.birthday = Birthday(value)
    

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    

    def remove_phone(self, rem_phone):
        for phone in self.phones:
            if phone.value == rem_phone:
                self.phones.remove(phone)
           
    
    def edit_phone(self, old_phone, edited_phone):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[idx] = Phone(edited_phone)
                break
        else:
            raise ValueError ('This number does not exist')
                

    def find_phone(self, current_phone):
        for phone in self.phones:
            if phone.value == current_phone:
                return phone
        return None


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):


    def add_record(self,record):
        self.data[record.name.value] = record
           

    def find(self, name):
        return self.data.get(name)
           
    
    def delete(self,name):
        if name not in self.data:
            raise KeyError ('Name not found')
        else:
            del self.data[name]

    
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday:
                user_birthday = record.birthday.value
                next_birthday = user_birthday.replace(year=today.year) 
            if next_birthday < today:
                next_birthday = user_birthday.replace(year=today.year+1)
            if (next_birthday - today).days <= 7:
                upcoming_birthdays.append({"name": record.name.value, "birthday": next_birthday.strftime("%d.%m.%Y") })
        
        return upcoming_birthdays
    
        


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f'ValueError: {e}'
        except KeyError as e:
            return f"KeyError: {e}"
        except IndexError as e:
            return f"IndexError: {e}"
        

    return inner


@input_error
def add_birthday(args, book:AddressBook):
    if len(args) < 2: #check if we have all arguments to work with from the list
        raise ValueError('Please enter the Name and birthday date')
    name, date = args
    record:Record = book.find(name)
    if record is None:
        return "Sorry no User found"
    else:
        record.add_birthday(date)
        return 'The birthday date was added'



    

@input_error
def show_birthday(args, book:AddressBook):
    if len(args) < 1: #check if we have all arguments to work with from the list
        raise ValueError('Please enter the Name')
    name = args[0] # we do it to ge a string not list :)
    record:Record = book.find(name)
    if record is None or record.birthday is None:
        return "Sorry no data about this user's birthday date"
    else:
        return record.birthday.value

     
    # реалізація

@input_error
def birthdays(book:AddressBook):
    birthday_list = [str(record) for record in book.get_upcoming_birthdays()]
    return '\n'.join(birthday_list) if birthday_list else 'No data available'


@input_error
#Function that show all contacts.
def show_all(book:AddressBook):
    records = [str(record) for record in book.values()]
    records_string = '\n'.join(records) 
    return records_string if records else 'No data available'


@input_error
#Function that show Phone number by users name.
def show_phone(args, book:AddressBook):
    if args:
        name = args[0]
        record:Record = book.find(name)
        if record: #Check if we have this contact in the dictionary
            return book.find(name)
        else:
            raise KeyError("This contacts is not exist, use 'add' command to create a new one")
    else:
        return f'User name was not provided' 


@input_error
#Function that change a phone number by users name.   
def change_contact(args, book:AddressBook):
    if len(args) < 3: #check if we have all arguments to work with from the list
        raise ValueError('To change the contact you need to provide name that exist in phonebook and a new phone')
    name, old_phone, new_phone = args
    record:Record = book.find(name)
    if record:
        record.edit_phone(old_phone,new_phone)
        return f'Contact updated.'


@input_error
def parse_input(user_input):    
        user_input = user_input.strip() 
        cmd, *args = user_input.split()
        cmd = cmd.lower()
        return cmd, *args


@input_error
def add_contact(args, book:AddressBook):
    if len(args) < 2: #check if we have all arguments to work with from the list
        raise ValueError('To add the number you need to provide a name and a personal phone')
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    if phone in [phone.value for phone in record.phones]:
        return "The number is already exist"
    record.add_phone(phone)
    return "Contact added."


@input_error
def main():

    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")



if __name__ == "__main__":
    main()