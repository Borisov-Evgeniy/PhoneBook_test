import json
import os
from typing import List
import random


class Contact:
    def __init__(self, last_name: str, first_name: str, middle_name: str, organization: str, work_phone: str,
                 personal_phone: str):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    def to_dict(self):
        return {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'organization': self.organization,
            'work_phone': self.work_phone,
            'personal_phone': self.personal_phone
        }


class Phonebook:
    def __init__(self) -> None:
        self.contacts: List[Contact] = []

    def load_contacts(self, file_name: str) -> None:
        """Загрузка контактов из файла JSON."""
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r') as file:
                    self.contacts = json.load(file)
            except FileNotFoundError:
                print("Файл не найден.")
            except json.decoder.JSONDecodeError:
                print("Некорректный формат данных в файле.")
        else:
            print("Файл не существует. Создание нового файла.")
            self.contacts = []

    def save_contacts(self, file_name: str) -> None:
        """Сохранение контактов в файл JSON."""
        contacts_data = [contact.__dict__ for contact in self.contacts]
        with open(file_name, 'w') as file:
            json.dump(contacts_data, file, indent=4)

    def add_contact(self, contact: Contact) -> None:
        """Добавление нового контакта в телефонную книгу."""
        self.contacts.append(contact)

    def edit_contact(self, index: int, contact: Contact) -> None:
        """Редактирование существующего контакта в телефонной книге."""
        self.contacts[index] = contact

    def display_contacts(self, page_num: int, page_size: int) -> None:
        """Отображение контактов постранично на экране."""
        start_index = (page_num - 1) * page_size
        end_index = min(start_index + page_size, len(self.contacts))
        for i in range(start_index, end_index):
            print(
                f"{i + 1}. {self.contacts[i].last_name}, {self.contacts[i].first_name}, {self.contacts[i].work_phone}, {self.contacts[i].personal_phone}")

    def generate_contacts(self, num_contacts):
        """Генерация случайных контактов для проверки приложения."""
        first_names = ["Иван", "Петр", "Сергей", "Андрей", "Елена", "Ольга", "Мария", "Александра"]
        last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнова", "Попова", "Козлова", "Новикова"]
        organizations = ["Компания1", "Компания2", "Компания3", "Компания4", "Компания5"]

        for _ in range(num_contacts):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            middle_name = random.choice(["", "Иванович", "Петрович"])
            organization = random.choice(organizations)
            work_phone = f"+7(9{random.randint(10, 99)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
            personal_phone = f"+7(9{random.randint(10, 99)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

            contact = Contact(last_name, first_name, middle_name, organization, work_phone, personal_phone)
            self.add_contact(contact)

class PhonebookApp:
    def __init__(self, phonebook):
        self.phonebook = phonebook

    def run(self):
        while True:
            print("\n1. Вывести записи")
            print("2. Добавить новую запись")
            print("3. Редактировать запись")
            print("4. Поиск записей")
            print("5. Создать и записать 40 случайных контактов в файл")
            print("6. Сохранить и выйти")

            choice = input("Выберите действие: ")
            if choice == '1':
                try:
                    page_num = int(input("Введите номер страницы: "))
                except ValueError:
                    print("Некорректный ввод. Пожалуйста, введите число.")
                    continue
                self.phonebook.display_contacts(page_num, 5)
            elif choice == '2':
                last_name = input("Введите фамилию: ")
                first_name = input("Введите имя: ")
                middle_name = input("Введите отчество: ")
                organization = input("Введите название организации: ")
                work_phone = input("Введите рабочий телефон: ")
                personal_phone = input("Введите личный телефон: ")
                contact = Contact(last_name, first_name, middle_name, organization, work_phone, personal_phone)
                self.phonebook.add_contact(contact)
            elif choice == '3':
                index = int(input("Введите номер записи для редактирования: ")) - 1
                last_name = input("Введите новую фамилию: ")
                first_name = input("Введите новое имя: ")
                middle_name = input("Введите новое отчество: ")
                organization = input("Введите новое название организации: ")
                work_phone = input("Введите новый рабочий телефон: ")
                personal_phone = input("Введите новый личный телефон: ")
                contact = Contact(last_name, first_name, middle_name, organization, work_phone, personal_phone)
                self.phonebook.edit_contact(index, contact)
            elif choice == '4':
                query = input("Введите запрос (фамилия, имя, организация, рабочий телефон, личный телефон): ")
                results = self.phonebook.search_contacts(last_name=query)
                for i, contact in enumerate(results, 1):
                    print(
                        f"{i}. {contact.last_name}, {contact.first_name}, {contact.work_phone}, {contact.personal_phone}")
            elif choice == '5':
                self.phonebook.generate_contacts(40)
                print("Созданы и записаны 40 случайных контактов в файл 'contacts.txt'.")
            elif choice == '6':
                self.phonebook.save_contacts('contacts.txt')
                print("Сохранение контактов...")
                break
            else:
                print("Некорректный ввод. Пожалуйста, повторите.")


def main():
    phonebook = Phonebook()
    app = PhonebookApp(phonebook)
    try:
        app.run()
    except KeyboardInterrupt:
        print("Программа завершена пользователем.")


if __name__ == "__main__":
    main()
