import sqlite3


def print_coins():
    for row in cur.execute('''SELECT * FROM coins_table'''):
        print(row)


def get_coins(id: int):
    cur.execute("""SELECT coins FROM coins_table WHERE UserID=?""", (id,))
    x = cur.fetchone()
    if x is None:
        cur.execute("""INSERT INTO coins_table VALUES (?, 100)""", (id,))
        con.commit()
        return 100
    return x[0]


def add_coins(id: int, newCoins: int):
    cur.execute("""
        INSERT INTO coins_table VALUES (?, 100 + ?)
            ON CONFLICT(UserID) DO UPDATE SET coins=coins + ?;
        """, (id, newCoins, newCoins))
    con.commit()


con = sqlite3.connect('jiggly_database.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS coins_table 
            (UserID int primary key, coins int)''')
