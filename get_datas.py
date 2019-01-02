import sqlite3


def get_datas_from_database():
    conn = sqlite3.connect('prize.db')
    curs = conn.cursor()
    curs.execute("SELECT redone, redtwo, redthree, redfour, redfive, redsix, blue from prize")
    datas = curs.fetchall()
    datas = [tuple(da-1 for da in data) for data in datas]
    return datas


if __name__ == '__main__':
    datas = get_datas_from_database()
    print(len(datas))
    print(datas[0:10])
