import json  # Импорт модуля json для работы с JSON
import os  # Импорт модуля os для работы с файловой системой ( используетс os.path.exists)
from typing import List  # Импорт List из модуля typing для типизации
import random  # Импорт модуля random для генерации случайных данных( используется def generate_contacts)

class Contact:
    def __init__(self, last_name: str, first_name: str, middle_name: str, organization: str, work_phone: str,
                 personal_phone: str):
        # Инициализация атрибутов объекта контакта
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    def to_dict(self):
        # Преобразование данных контакта в словарь
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
        # Инициализация списка контактов
        self.contacts: List[Contact] = []

    def load_contacts(self, file_name: str) -> None:
        """Загрузка контактов из файла JSON."""
        # Проверка наличия файла и загрузка контактов
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r') as file:
                    self.contacts = json.load(file)  # Загрузка контактов из файла
            except FileNotFoundError:
                print("Файл не найден.")
            except json.decoder.JSONDecodeError:
                print("Некорректный формат данных в файле.")
        else:
            print("Файл не существует. Создание нового файла.")
            self.contacts = []

    def save_contacts(self, file_name: str) -> None:
        """Сохранение контактов в файл JSON."""
        # Сохранение списка контактов в файл JSON
        contacts_data = [contact.__dict__ for contact in self.contacts]  # Преобразование контактов в формат JSON
        with open(file_name, 'w') as file:
            json.dump(contacts_data, file, indent=4)  # Запись контактов в файл JSON

    def add_contact(self, contact: Contact) -> None:
        """Добавление нового контакта в телефонную книгу."""
        # Добавление контакта в список контактов
        self.contacts.append(contact)

    def edit_contact(self, index: int, contact: Contact) -> None:
        """Редактирование существующего контакта в телефонной книге."""
        # Редактирование контакта по индексу
        self.contacts[index] = contact

    def display_contacts(self, page_num: int, page_size: int) -> None:
        """Отображение контактов постранично на экране."""
        # Отображение списка контактов с пагинацией. page_num - это номер страницы, который указывает пользователь.
        # page_size - это количество записей, которые должны быть отображены на каждой странице.
        # Индексы для выборки записей из общего списка данных.
        start_index = (page_num - 1) * page_size
        end_index = min(start_index + page_size, len(self.contacts))
        for i in range(start_index, end_index):
            print(
                f"{i + 1}. {self.contacts[i].last_name}, {self.contacts[i].first_name}, {self.contacts[i].work_phone}, {self.contacts[i].personal_phone}")

    def search_contacts(self, query: str) -> List[Contact]:
        """Поиск контактов по различным характеристикам."""
        # Поиск контактов по запросу
        results = []
        query = query.lower()  # Приводим запрос к нижнему регистру
        for contact in self.contacts:
            # Собираем данные контакта в одну строку для поиска
            contact_data = ' '.join(contact.to_dict().values()).lower()
            # Проверяем, содержится ли запрос в данных контакта
            if query in contact_data:
                results.append(contact)
        return results

    def generate_contacts(self, num_contacts):
        """Генерация случайных контактов для проверки приложения."""
        # Генерация случайных контактов
        first_names = ["Иван", "Петр", "Сергей", "Андрей", "Елена", "Ольга", "Мария", "Александра"]
        last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнова", "Попова", "Козлова", "Новикова"]
        organizations = ["Компания1", "Компания2", "Компания3", "Компания4", "Компания5"]

        for _ in range(num_contacts):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            middle_name = random.choice(["", "Иванович", "Петрович"])
            organization = random.choice(organizations)
            # Генерация случайных телефонов
            work_phone = f"+7(9{random.randint(10, 99)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
            personal_phone = f"+7(9{random.randint(10, 99)}){random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

            contact = Contact(last_name, first_name, middle_name, organization, work_phone, personal_phone)
            self.add_contact(contact)

class PhonebookApp:
    def __init__(self, phonebook):
        # Инициализация приложения телефонной книги
        self.phonebook = phonebook

    def run(self):
        # Запуск основного цикла приложения
        while True:
            # Вывод меню действий
            print("\n1. Вывести записи")
            print("2. Добавить новую запись")
            print("3. Редактировать запись")
            print("4. Поиск записей")
            print("5. Создать и записать 40 случайных контактов в файл")
            print("6. Сохранить и выйти")

            choice = input("Выберите действие: ")  # Получение выбора пользователя
            if choice == '1':
                try:
                    page_num = int(input("Введите номер страницы: "))  # Получение номера страницы для вывода
                except ValueError:
                    print("Некорректный ввод. Пожалуйста, введите число.")
                    continue
                self.phonebook.display_contacts(page_num, 10)  # Вывод контактов с пагинацией
            elif choice == '2':
                # Добавление нового контакта
                last_name = input("Введите фамилию: ")
                first_name = input("Введите имя: ")
                middle_name = input("Введите отчество: ")
                organization = input("Введите название организации: ")
                work_phone = input("Введите рабочий телефон: ")
                personal_phone = input("Введите личный телефон: ")
                contact = Contact(last_name, first_name, middle_name, organization, work_phone, personal_phone)
                self.phonebook.add_contact(contact)
            elif choice == '3':
                # Редактирование существующего контакта
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
                # Поиск контактов по запросу
                query = input("Введите запрос (фамилия, имя, организация, рабочий телефон, личный телефон): ")
                print(f"Выполняется поиск по запросу: {query}")
                results = self.phonebook.search_contacts(query)
                if results:
                    for i, contact in enumerate(results, 1):
                        print(
                            f"{i}. {contact.last_name}, {contact.first_name}, {contact.work_phone}, {contact.personal_phone}")
                else:
                    print("Ничего не найдено.")
            elif choice == '5':
                # Генерация случайных контактов и запись их в файл
                self.phonebook.generate_contacts(40)
                print("Созданы и записаны 40 случайных контактов в файл 'contacts.txt'.")
            elif choice == '6':
                # Сохранение контактов и завершение работы приложения
                self.phonebook.save_contacts('contacts.txt')
                print("Сохранение контактов...")
                break
            else:
                print("Некорректный ввод. Пожалуйста, повторите.")


def main():
    # Инициализация телефонной книги и запуск приложения
    phonebook = Phonebook()
    app = PhonebookApp(phonebook)
    try:
        app.run()
    except KeyboardInterrupt:
        print("Программа завершена пользователем.")


if __name__ == "__main__":
    main()
