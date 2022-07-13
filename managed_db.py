import sqlite3
conn = sqlite3.connect("userdata.db")
c = conn.cursor()


def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(kullanici_adi TEXT,parola TEXT)')


def add_userdata(kullanici_adi,parola):
	c.execute('INSERT INTO userstable(kullanici_adi,parola) VALUES (?,?)',(kullanici_adi,parola))
	conn.commit()

def login_user(kullanici_adi,parola):
	c.execute('SELECT * FROM userstable WHERE kullanici_adi =? AND parola = ?',(kullanici_adi,parola))
	data = c.fetchall()
	return data



def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data