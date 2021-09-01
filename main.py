import sqlite3
from tkinter import *
import random
from threading import Thread
from pyperclip import copy

contributors_count = 0

def get_db_connection():
    con = sqlite3.connect('contributors.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS contributors(
        firstname text,
        lastname text,
        phone text UNIQUE
    );''')
    
    return con, cur

def add_contributor():
    con, cur = get_db_connection()
    firstname = get_firstname.get()
    lastname = get_lastname.get()
    phone = get_phone.get()
    if firstname != '' and lastname != '' and phone != '':
        values = (firstname, lastname, phone)
        sql = "INSERT INTO contributors(firstname, lastname, phone) VALUES (?, ?, ?)"
        cur.execute(sql, values)
        con.commit()
    get_firstname.delete(0, END)
    get_lastname.delete(0, END)
    get_phone.delete(0, END)

def lottery():
    con, cur = get_db_connection()
    all_contributors = cur.execute("SELECT * FROM contributors ").fetchall()
    winners = ''
    if all_contributors != []:
        for i in range(1, 11):
            winner = random.choice(all_contributors)
            if winner[2] not in winners:
                winners += f"{winner[0]}-{winner[1]}-{winner[2]} "
    
    copy(winners)


def get_contributors_count():
    global contributors_count
    con, cur = get_db_connection()
    while True:
        contributors_count = str(cur.execute("SELECT COUNT(*) FROM contributors").fetchall()[0][0])
        lbl_count['text'] = contributors_count
        

def delete_all():
    con, cur = get_db_connection()
    cur.execute("DELETE FROM contributors")
    con.commit()
        

root = Tk()

root.title('نرم افزار قرعه کشی')
root.geometry('150x250')
root.resizable(False, False)

lbl_firstname = Label(root, text=':نام')
get_firstname = Entry(root)
lbl_lastname = Label(root, text=':نام خانوادگی')
get_lastname = Entry(root)
lbl_phone = Label(root, text=':شماره تلفن')
get_phone = Entry(root)
send_btn = Button(root, text='اضافه کردن', command=add_contributor)
lottery_btn = Button(root, text='قرعه کشی', command=lottery)
delete_btn = Button(root, text='حذف همه', command=delete_all)
lbl_all = Label(root, text=':تعداد کل شرکت کنندگان')
lbl_count = Label(root, text=contributors_count)

lbl_firstname.grid()
get_firstname.grid()
lbl_lastname.grid()
get_lastname.grid()
lbl_phone.grid()
get_phone.grid()
send_btn.grid()
lottery_btn.grid()
delete_btn.grid()
lbl_all.grid()
lbl_count.grid()

Thread(target=get_contributors_count).start()

root.mainloop()
