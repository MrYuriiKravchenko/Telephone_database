import sqlite3

MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5


def main():
    choice = 0
    while choice != EXIT:
        display_menu()
        choice = get_menu_choice()

        if choice == CREATE:
            create()
        elif choice == READ:
            read()
        elif choice == UPDATE:
            update()
        elif choice == DELETE:
            delete()

# Функция display_menu выводит на экран главное меню.


def display_menu():
    print('\n------Меню ведения телефонной книги------')
    print('1. Добавить новый номер')
    print('2. Просмотреть искомый номер')
    print('3. Изменить номер')
    print('4. Удалить номер')
    print('5. Выйти из программы')
    print()

# Функция get_menu_choice получает от пользователя пункт меню.


def get_menu_choice():
    choice = int(input('Введите ваш вариант: '))

    while choice < MIN_CHOICE or choice > MAX_CHOICE:
        print(f'Допустимые варианты таковы: {MIN_CHOICE} - {MAX_CHOICE}.')
        choice = int(input('Введите ваш вариант: '))

    return choice

# Функция create создает новый контакт


def create():
    print('Добавить новый номер телефона')
    name = input('Имя: ')
    phone = int(input('Номер телефона: '))
    insert_row(name, phone)

# Функция read читает существующий контакт


def read():
    name = input('Введите имя искомого номера: ')
    num_found = display_item(name)
    print(f'{num_found} контакт найден')

# Функция update изменяет данные существующего контакта


def update():
    read()

    selected_id = int(input('Выберите ID обновляемого контакта: '))
    name = input('Введите новое имя контакта: ')
    phone = input('Введите новый номер: ')

    num_updated = update_row(selected_id, name, phone)
    print(f'{num_updated} контакт изменен.')

# Функция delete удаляет контакт


def delete():
    read()
    selected_id = int(input('Выберите ID удаляемого контакта: '))

    sure = input('Вы уверены, что хотите удалить эту позицию? (д/н): ')
    if sure.lower() == 'д':
        num_deleted = delete_row(selected_id)
        print(f'{num_deleted} контакт удален')

# Функция insert_row вставляет строку в таблицу Entries


def insert_row(name, phone):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO Entries (Name, Number)
                    VALUES (?, ?)''',
                    (name, phone))
        conn.commit()
    except sqlite3.Error as err:
        print('Ошибк базы данных', err)
    finally:
        if conn != None:
            conn.close()

# Функция display_item выводит на экран все контакты


def display_item(name):
    conn = None
    results = []
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Entries
                    WHERE Name == ?''',
                    (name,))
        results = cur.fetchall()

        for row in results:
            print(f'ID: {row[0]:<3} Номер: {row[1]:<15} '
                  f'Имя: {row[2]:<6}')
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()
        return len(results)

# Функция update_row обновляет существующую строку новыми
# именем и номером


def update_row(itemid, name, phone):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''UPDATE Entries
                    SET Name = ?, Number = ?
                    WHERE ItemID == ?''',
                    (name, phone, itemid))
        conn.commit()
        num_updated = cur.rowcount
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()

        return num_updated

# Функция delete_row удаляет существующий контакт.


def delete_row(itemid):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM Entries
                    WHERE ItemID == ?''',
                    (itemid,))
        conn.commit()
        num_deleted = cur.rowcount
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()

        return num_deleted


if __name__ == '__main__':
    main()
