# -*- coding: UTF-8 -*-
import sqlite3
import xlrd    #读取excel
import xlwt    #写入excel


#若prize数据库不存在则创建并连接，存在则直接连接
conn = sqlite3.connect('prize.db')
curs = conn.cursor()

try:
	#若prize表单不存在则创建，存在则不处理
	curs.execute('''CREATE TABLE IF NOT EXISTS prize(
		id           TEXT  PRIMARY KEY,
		prizedate    TEXT,
		redone       INT,
		redtwo       INT,
		redthree     INT,
		redfour      INT,
		redfive      INT,
		redsix       INT,
		blue         INT,
		bettingprize INT,
		totalprize   INT,
		first        INT,
		firstprize   INT,
		second       INT,
		secondprize  INT,
		third        INT,
		thirdprize   INT,
		forth        INT,
		forthprize   INT,
		fifth        INT,
		fifthprize   INT,
		six          INT,
		sixprize     INT
	)''')
except:
	print("create table prize failed")


# #乱序
# with xlrd.open_workbook(r'ssq.xls') as file_object:
# 	sheet = file_object.sheet_by_name('data')
# 	for i in range(2, 2208):
# 		query = r'INSERT INTO prize VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
# 		line = sheet.row_values(i)
# 		curs.execute(query, [str(int(line[0])), line[1], int(line[9]),                  \
# 		int(line[10]), int(line[11]), int(line[12]), int(line[13]), int(line[14]),      \
# 		int(line[8]),int(line[15]), int(line[16]), int(line[17]), int(line[18]),        \
# 		int(line[19]), int(line[20]), int(line[21]), int(line[22]), int(line[23]),      \
# 		int(line[24]), int(line[25]), int(line[26]), int(line[27]), int(line[28])])

#顺序
with xlrd.open_workbook(r'ssq.xls') as file_object:
	sheet = file_object.sheet_by_name('data')
	for i in range(2, 2227):
		query = r'INSERT INTO prize VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
		line = sheet.row_values(i)
		curs.execute(query, [str(int(line[0])), line[1], int(line[2]),             \
		int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7]),      \
		int(line[8]),int(line[15]), int(line[16]), int(line[17]), int(line[18]),   \
		int(line[19]), int(line[20]), int(line[21]), int(line[22]), int(line[23]), \
		int(line[24]), int(line[25]), int(line[26]), int(line[27]), int(line[28])])

conn.commit()
conn.close()



