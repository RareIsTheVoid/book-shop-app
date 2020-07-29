from tkinter import *
import sqlite3

window = Tk(className="Book shop")


def closeApp():
    window.destroy()


def insertBook():
    listBox.delete(0, END)
    conn=sqlite3.connect("booksdb.db")
    curs=conn.cursor()
    curs.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (enTitleVal.get(), enAuthorVal.get(), enISBNVal.get(), int(enYearVal.get())))
    conn.commit()
    curs.execute("SELECT * FROM books")
    rows=curs.fetchall()
    for row in rows:
        listBox.insert(END, row[0] +", "+row[1]+", "+row[2]+", "+str(row[3]))
    conn.close()
    enTitle.delete(0, END)
    enYear.delete(0, END)
    enISBN.delete(0, END)
    enAuthor.delete(0, END)


def updateBook():
    arr = list(str(listBox.get(ANCHOR)).split(", "))
    conn=sqlite3.connect("booksdb.db")
    curs=conn.cursor()
    curs.execute("UPDATE books SET title=?, author=?, isbn=?, year=? WHERE isbn=?", (enTitleVal.get(), enAuthorVal.get(), enISBNVal.get(), int(enYearVal.get()), arr[2]))
    conn.commit()
    listBox.delete(0, END)
    curs.execute("SELECT * FROM books")
    rows=curs.fetchall()
    for row in rows:
        listBox.insert(END, row[0] +", "+row[1]+", "+row[2]+", "+str(row[3]))
    conn.close()
    enTitle.delete(0, END)
    enAuthor.delete(0, END)
    enISBN.delete(0, END)
    enYear.delete(0, END)

def deleteBook():
    arr=list(str(listBox.get(ANCHOR)).split(", "))
    conn=sqlite3.connect("booksdb.db")
    curs=conn.cursor()
    curs.execute("DELETE FROM books WHERE isbn=?", [arr[2]])
    conn.commit()
    listBox.delete(0, END)
    curs.execute("SELECT * FROM books")
    rows=curs.fetchall()
    for row in rows:
        listBox.insert(END, row[0] +", "+row[1]+", "+row[2]+", "+str(row[3]))
    conn.close()
    enTitle.delete(0, END)
    enAuthor.delete(0, END)
    enISBN.delete(0, END)
    enYear.delete(0, END)


def onSelect(event):
    w=event.widget
    enTitle.delete(0, END)
    enAuthor.delete(0, END)
    enYear.delete(0, END)
    enISBN.delete(0, END)
    arr=str(w.get(ANCHOR)).split(", ")
    conn=sqlite3.connect("booksdb.db")
    curs=conn.cursor()
    curs.execute("SELECT * FROM books WHERE isbn=?", [arr[2]])
    row=curs.fetchall()
    enTitle.insert(END, row[0][0])
    enAuthor.insert(END, row[0][1])
    enISBN.insert(END, row[0][2])
    enYear.insert(END, row[0][3])


lbTitle=Label(window, text="Title:")
lbTitle.grid(row=0, column=0)

lbAuthor=Label(window, text="Author:")
lbAuthor.grid(row=1, column=0)

lbISBN=Label(window, text="ISBN:")
lbISBN.grid(row=2, column=0)

lbYear=Label(window, text="Year:")
lbYear.grid(row=3, column=0)

lbEmpt1=Label(window, width=5)
lbEmpt1.grid(row=0, column=2)

lbEmpt2=Label(window)
lbEmpt2.grid(row=5, column=0)

lbEmpt3=Label(window)
lbEmpt3.grid(row=7, column=0)

enTitleVal=StringVar()
enTitle=Entry(window, textvariable=enTitleVal)
enTitle.grid(row=0, column=1)

enAuthorVal=StringVar()
enAuthor=Entry(window, textvariable=enAuthorVal)
enAuthor.grid(row=1, column=1)

enISBNVal=StringVar()
enISBN=Entry(window, textvariable=enISBNVal)
enISBN.grid(row=2, column=1)

enYearVal=StringVar()
enYear=Entry(window, textvariable=enYearVal)
enYear.grid(row=3, column=1)

btnAdd=Button(window, text="Add book", width=15, command=insertBook)
btnAdd.grid(row=0, column=3)

btnUpdate=Button(window, text="Update selected", width=15, command=updateBook)
btnUpdate.grid(row=1, column=3)

btnDelete=Button(window, text="Delete selected", width=15, command=deleteBook)
btnDelete.grid(row=2, column=3)

btnClose=Button(window, text="Close", width=15, command=closeApp)
btnClose.grid(row=3, column=3)

listBox=Listbox(window, height=15, width=50, selectmode=SINGLE)
listBox.grid(row=6, column=0, columnspan=4)
listBox.bind("<<ListboxSelect>>", onSelect)


conn = sqlite3.connect("booksdb.db")
curs = conn.cursor()
curs.execute("CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, isbn TEXT, year INTEGER)")
conn.commit()
curs.execute("SELECT * FROM books")
rows=curs.fetchall()
for row in rows:
    listBox.insert(END, row[0] +", "+row[1]+", "+row[2]+", "+str(row[3]))
conn.close()

window.mainloop()
