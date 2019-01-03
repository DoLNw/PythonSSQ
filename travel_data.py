# # coding=utf-8
import sqlite3

# # 连接
# conn = sqlite3.connect('travel_data.db')
# conn.text_factory = str
# c = conn.cursor()

# # 创建表
# c.execute('''DROP TABLE IF EXISTS travel''')
# c.execute('''CREATE TABLE travel (name text, place text, time text)''')

# # 数据
# # 格式：月份,蒸发量,降水量
# some = [('李四', '香港', '星期二'),
#         ('爱丽丝', '北京', '星期五')
#         ]

# # 插入数据
# c.executemany('INSERT INTO travel VALUES (?,?,?)', some)

# # 提交！！！
# conn.commit()



# # 查询方式一
# for row in c.execute('SELECT * FROM travel'):
#     print(row)

# # 查询方式二
# c.execute('SELECT * FROM travel')
# print(c.fetchall())

# # 查询方式二_2
# res = c.execute('SELECT * FROM travel')
# print(res.fetchall())



# # 关闭
# conn.close()


# conn = sqlite3.connect('travel_data.db')
# query = 'INSERT INTO travel VALUES (?,?,?)'
# value = [('张三', '杭州', '星期六')]
# conn.cursor().executemany(query, value)
# conn.commit()
# conn.close()

# conn = sqlite3.connect('travel_data.db')
# for row in conn.cursor().execute('SELECT * FROM travel'):
#     print(row)
# value = list(conn.cursor().execute('SELECT * FROM travel'))
# print(value)
# # value = conn.cursor().fetchall()
# conn.close()


conn = sqlite3.connect('travel_data.db')
values = list(conn.cursor().execute('SELECT * FROM travel'))
print(values)
place11 = (conn.cursor().execute("SELECT count(place) FROM travel where place='杭州'").fetchall())[0][0]
print(place11)
conn.close()

