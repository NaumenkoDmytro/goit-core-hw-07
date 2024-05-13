from collections import UserDict


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

                             
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []


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