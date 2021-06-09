from tkinter import *
from tkinter import messagebox as msgb
from tkinter import ttk as ttk
import sqlite3



root = Tk()
subject = StringVar()
grade = DoubleVar()
grade2 = DoubleVar()
average = DoubleVar()
id = None
insertWindow = None
updateWindow = None

def database():
    conn = sqlite3.connect('./av2/Notas.db')
    cur = conn.cursor()
    conn.execute("""CREATE TABLE IF NOT EXISTS notas(
                    idnota INTEGER PRIMARY KEY AUTOINCREMENT,
                    materia TEXT NOT NULL,
                    nota DOUBLE NOT NULL,
                    nota2 DOUBLE NOT NULL,
                    media DOUBLE NOT NULL)""")
    cur.execute('SELECT * FROM notas ORDER BY materia')
    fetch = cur.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cur.close()
    conn.close()


def insertNota(materia, nota, nota2, media):
    conn = sqlite3.connect('./av2/Notas.db')
    cur = conn.cursor()
    conn.execute('INSERT INTO notas (materia, nota, nota2, media) VALUES(?, ?, ?, ?)',(materia, nota, nota2, media))
    conn.commit()
    cur.execute('SELECT * FROM notas ORDER BY materia')
    fetch = cur.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cur.close()
    conn.close()


def updateNota(materia, nota, nota2, media, idnota):
    conn = sqlite3.connect('./av2/Notas.db')
    cur = conn.cursor()
    conn.execute('UPDATE notas SET materia = ?, nota = ?, nota2 = ?, media = ? WHERE idnota = ?',(materia, nota, nota2, media, idnota))
    conn.commit()
    cur.execute('SELECT * FROM notas ORDER BY materia')
    fetch = cur.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cur.close()
    conn.close()


def deleteNota(idnota):
    conn = sqlite3.connect('./av2/Notas.db')
    cur = conn.cursor()
    conn.execute('DELETE FROM notas WHERE idnota = ?', (idnota, ))
    conn.commit()
    conn.close()

def deleteData():
    if not tree.selection():
        msgb.showwarning("Nenhum item selecionado...", "Porfavor selecione o item que deseja deletar!", icon="warning")
    else:
        ask = msgb.askquestion("Tem certeza?", "Tem certeza que quer deletar esse item? Será irreversível!", icon="warning")
        if ask == 'yes':            
            selectItem = tree.focus()
            content = (tree.item(selectItem))
            selectedItem = content["values"]
            tree.delete(selectItem)
            id = selectedItem[0]
            deleteNota(id)

def updateData():
    tree.delete(*tree.get_children())
    average.set((grade.get()+grade2.get())/2)
    updateNota(subject.get(), grade.get(), grade2.get(), average.get(), id)
    subject.set("")
    grade.set("")
    grade2.set("")
    average.set("")
    updateWindow.destroy()

def onSelected(event):
    global id, updateWindow
    selectItem = tree.focus()
    content = (tree.item(selectItem))
    selectedItem = content["values"]
    id = selectedItem[0]
    subject.set(selectedItem[1])
    grade.set(selectedItem[2])
    grade2.set(selectedItem[3])
    average.set(selectedItem[4])
    updateWindow = Toplevel()
    updateWindow.title("Atualizar notas")
    width = 480
    height = 200
    sc_width = updateWindow.winfo_screenwidth()
    sc_height = updateWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    updateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateWindow.resizable(0, 0)
    registerTitle = Frame(updateWindow)
    registerTitle.pack(side=TOP)
    registerContact = Frame(updateWindow)
    registerContact.pack(side=TOP, pady=10)
    lblTitle = Label(registerTitle, text="Atualizar Notas",font=("consolas", 25), bg="#7cbb63", width=300)
    lblTitle.pack(fill=X)
    lblsubject = Label(registerContact, text="Nome da Materia", font=("consolas", 11))
    lblsubject.grid(row=0, sticky=W)
    lblNota = Label(registerContact,text="Primeira Avaliacao", font=("consolas", 11))
    lblNota.grid(row=1, sticky=W)
    lblNota2 = Label(registerContact, text="Segunda Avaliacao", font=("consolas", 11))
    lblNota2.grid(row=2, sticky=W)
    subjectEntry = Entry(registerContact, textvariable=subject, font=('arial', 12))
    subjectEntry.grid(row=0, column=1)
    notaEntry = Entry(registerContact, textvariable=grade, font=('arial', 12))
    notaEntry.grid(row=1, column=1)
    nota2Entry = Entry(registerContact, textvariable=grade2,font=('arial', 12))
    nota2Entry.grid(row=2, column=1)
    bttnInsert = Button(registerContact, text="Atualizar",width=50, command=updateData)
    bttnInsert.grid(row=4, columnspan=2, pady=10)
    insertWindow.mainloop()

def submitData():
    if grade.get() == None or subject.get() == "" or grade2.get() == None:
        result = msgb.showwarning("Campo vazio!", "Você esqueceu de preencher algum campo.", icon="warning")
    else:
        tree.delete(*tree.get_children())
        average.set((grade.get()+grade2.get())/2)
        insertNota(subject.get(), grade.get(), grade2.get(), average.get())
        subject.set("")
        grade.set("")
        grade2.set("")
        average.set("")

def insertData():
    subject.set("")
    grade.set("")
    grade2.set("")
    insertWindow = Toplevel()
    insertWindow.title("Inserir Nota")
    width = 480
    height = 200
    sc_width = insertWindow.winfo_screenwidth()
    sc_height = insertWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    insertWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    insertWindow.resizable(0, 0)
    registerTitle = Frame(insertWindow)
    registerTitle.pack(side=TOP)
    registerContact = Frame(insertWindow)
    registerContact.pack(side=TOP, pady=10)
    lblTitle = Label(registerTitle, text="Insira as Notas",font=("consolas", 25), bg="#7cbb63", width=300)
    lblTitle.pack(fill=X)
    lblsubject = Label(registerContact, text="Nome da Materia", font=("consolas", 11))
    lblsubject.grid(row=0, sticky=W)
    lblNota = Label(registerContact, text="Primeira Avaliacao",font=("consolas", 11))
    lblNota.grid(row=1, sticky=W)
    lblNota2 = Label(registerContact, text="Segunda Avaliacao", font=("consolas", 11))
    lblNota2.grid(row=2, sticky=W)
    subjectEntry = Entry(registerContact, textvariable=subject, font=('arial', 12))
    subjectEntry.grid(row=0, column=1)
    notaEntry = Entry(registerContact, textvariable=grade, font=('arial', 12))
    notaEntry.grid(row=1, column=1)
    nota2Entry = Entry(registerContact, textvariable=grade2, font=('arial', 12))
    nota2Entry.grid(row=2, column=1)
    bttnInsert = Button(registerContact, text="Inserir",width=50, command=submitData)
    bttnInsert.grid(row=4, columnspan=2, pady=10)
    insertWindow.mainloop()

root.title('Gerenciador de notas')
width = 1024
height = 600
scWidth = root.winfo_screenwidth()
scHeight = root.winfo_screenheight()
x = (scWidth/2) - (width/2)
y = (scHeight/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.config(bg='#26547C')
root.resizable(0,0)
top = Frame(root, width=1250, bd=1, relief=SOLID)
top.pack(side=TOP)
mid = Label(text="Gerenciador de Notas", font=("consolas", 25),  bg="#6666ff") 
mid.pack(side=TOP)
midLeft = Frame(mid, width=250)
midLeft.pack(side=LEFT)
midLeftPadding = Frame(mid, width=750, bg="")
midLeftPadding.pack(side=LEFT)
midRight = Frame(mid, width=250)
midRight.pack(side=RIGHT)
bottom = Frame(root, width=500)
bottom.pack(side=BOTTOM)
tableMargim = Frame(root, width=1250)
tableMargim.pack(side=TOP)
bttn_add = Button(midLeft, text="Inserir", bg="OliveDrab1", command=insertData)
bttn_add.pack()
bttn_del = Button(midRight, text="Deletar", bg="orange red", command=deleteData)
bttn_del.pack(side=RIGHT)
scrollX = Scrollbar(tableMargim, orient=HORIZONTAL)
scrollY = Scrollbar(tableMargim, orient=VERTICAL)
tree = ttk.Treeview(tableMargim, columns=("ID", "MATERIA", "NOTA 1", "NOTA 2", "MEDIA"), height=400, selectmode="extended", yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)
scrollY.config(command=tree.yview)
scrollY.pack(side=RIGHT, fill=Y)
scrollX.config(command=tree.xview)
scrollX.pack(side=BOTTOM, fill=X)
tree.heading("ID", text="ID", anchor=W)
tree.heading("MATERIA", text="Materia", anchor=W)
tree.heading("NOTA 1", text="AV1", anchor=W)
tree.heading("NOTA 2", text="AV2", anchor=W)
tree.heading("MEDIA", text="Media", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=3)
tree.column('#1', stretch=NO, minwidth=0, width=50)
tree.column('#2', stretch=NO, minwidth=0, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=250)
tree.column('#4', stretch=NO, minwidth=0, width=155)
tree.pack()
tree.bind('<Double-Button-1>', onSelected)

if __name__ == '__main__':
    database()
    root.mainloop()
