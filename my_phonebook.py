import sqlite3

# Создать таблицу Entries


def main():
    conn = sqlite3.connect('phonebook.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Entries (ItemID INTEGER PRIMARY KEY NOT NULL,
                Number INTEGER,
                Name TEXT)''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
