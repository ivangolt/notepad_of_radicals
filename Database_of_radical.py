import tkinter
from tkinter import ttk
import sqlite3
from tkinter import Frame, Text


#######################################################################################################

# Создаем Окно с базой данных, содержащую в себе данные о радикалах
class Main(tkinter.Frame):

    def __init__(self, root):
        'конструктор класса'
        super().__init__(root)
        self.init_main()
        self.db = db  # экземпляр класса DB
        self.view_records()

    def init_main(self):
        toolbar = tkinter.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tkinter.TOP, fill=tkinter.X)

        # Добавляем кнопку "Добавить человека"
        self.add_img = tkinter.PhotoImage(file='add.png')
        btn_open_dialog = tkinter.Button(toolbar, text='Добавить человека', command=self.open_dialog, bg='#d7d7e0',
                                         bd=0,
                                         compound=tkinter.TOP, image=self.add_img)

        btn_open_dialog.pack(side=tkinter.LEFT)

        # Добавляем кнопку "Редактировать"

        self.update_img = tkinter.PhotoImage(file='add.png')
        btn_edit_dialog = tkinter.Button(toolbar, text=' Редактировать', bg='#d7d7e0', bd=0,
                                         image=self.update_img,
                                         compound=tkinter.TOP,
                                         command=self.open_update_dialog)

        btn_edit_dialog.pack(side=tkinter.LEFT)

        self.delete_img = tkinter.PhotoImage(file='img_delete.png')

        btn_delete = tkinter.Button(toolbar,
                                    text='Удалить позицию',
                                    bg='#d7d7e0', bd=0,
                                    image=self.delete_img,
                                    compound=tkinter.TOP,
                                    command=self.delete_records)

        btn_delete.pack(side=tkinter.LEFT)

        self.search_img = tkinter.PhotoImage(file='add.png')
        btn_search = tkinter.Button(toolbar,
                                    text='Поиск человека',
                                    bg='#d7d7e0', bd=0,
                                    image=self.search_img,
                                    compound=tkinter.TOP,
                                    command=self.open_search_dialog)

        btn_search.pack(side=tkinter.LEFT)

        self.refresh_img = tkinter.PhotoImage(file='add.png')
        btn_refresh = tkinter.Button(toolbar,
                                     text='Обновить',
                                     bg='#d7d7e0', bd=0,
                                     image=self.refresh_img,
                                     compound=tkinter.TOP,
                                     command=self.view_records)

        btn_refresh.pack(side=tkinter.LEFT)

        self.help_img = tkinter.PhotoImage(file='img_textBox0.png')
        btn_help = tkinter.Button(toolbar,
                                  bg='#d7d7e0', bd=0,
                                  image=self.help_img,
                                  compound=tkinter.TOP,
                                  command=self.open_help_dialog)

        btn_help.pack(side=tkinter.RIGHT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'surname', 'appear', 'emotions', 'work_place',
                                                'temperament',
                                                'base_radical',
                                                'second_radical'),
                                 height=100,

                                 show='headings', )

        self.tree.column('ID', width=30, anchor=tkinter.CENTER)
        self.tree.column('name', width=150, anchor=tkinter.CENTER)
        self.tree.column('surname', width=150, anchor=tkinter.CENTER)
        self.tree.column('appear', width=100, anchor=tkinter.CENTER)
        self.tree.column('emotions', width=200, anchor=tkinter.CENTER)
        self.tree.column('work_place', width=200, anchor=tkinter.CENTER)
        self.tree.column('temperament', width=150, anchor=tkinter.CENTER)
        self.tree.column('base_radical', width=110, anchor=tkinter.CENTER)
        self.tree.column('second_radical', width=130, anchor=tkinter.CENTER)

        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='Имя')
        self.tree.heading('surname', text='Фамилия')
        self.tree.heading('appear', text='Внешность')
        self.tree.heading('emotions', text='Мимика\Жесты')
        self.tree.heading('work_place', text='Рабочее пространство')
        self.tree.heading('temperament', text='Темперамент')
        self.tree.heading('base_radical', text='Радикал')
        self.tree.heading('second_radical', text='Вторичный радикал')

        self.tree.pack(side=tkinter.LEFT)

        scroll = tkinter.Scrollbar(self, command=self.tree.yview())
        scroll.pack(side=tkinter.LEFT, fill=tkinter.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, name, surname, appear, emotions, work_place, temperament, base_radical, second_radical):
        self.db.insert_data(name, surname, appear, emotions, work_place, temperament, base_radical, second_radical)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM database ORDER BY surname''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def update_record(self, name, surname, appear, emotions, work_place, temperament, base_radical, second_radical):
        self.db.c.execute(
            '''UPDATE database SET name=?, surname=?, appear=?, emotions=?, work_place=?,  temperament=?, base_radical=?, second_radical=? WHERE ID=?''',
            (name, surname, appear, emotions, work_place, temperament, base_radical, second_radical,
             self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM database WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, surname):
        surname = ('%' + surname + '%',)
        self.db.c.execute('''SELECT * FROM database WHERE surname LIKE ?''', surname)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_help_dialog(self):
        Help()


class Child(tkinter.Toplevel):  # Дочернее окно

    # создаем конструктор класса

    def __init__(self):
        super().__init__(root)  # КОНСТРУКТОР КЛАССА
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить человека в базу')
        self.geometry('700x400')
        self.resizable(True, True)

        # Labels
        label_name = tkinter.Label(self, text='Имя')
        label_name.place(x=40, y=40)

        label_surname = tkinter.Label(self, text='Фамилия')
        label_surname.place(x=40, y=60)

        label_appear = tkinter.Label(self, text='Внешность')
        label_appear.place(x=40, y=80)

        label_work_place = tkinter.Label(self, text='Мимика\Жесты')
        label_work_place.place(x=40, y=100)

        label_work_place = tkinter.Label(self, text='Оформление рабочего пространства')
        label_work_place.place(x=40, y=120)

        label_work_place = tkinter.Label(self, text='Темперамент')
        label_work_place.place(x=40, y=140)

        label_radikal = tkinter.Label(self, text='Радикал')
        label_radikal.place(x=40, y=160)

        label_second_radikal = tkinter.Label(self, text='Вторичный радикал')
        label_second_radikal.place(x=40, y=180)

        # Buttons
        self.btn_ok = ttk.Button(self, text='Добавить человека')
        self.btn_ok.place(x=450, y=350)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_surname.get(),
                                                                       self.entry_appear.get(),
                                                                       self.entry_emotions.get(),
                                                                       self.entry_work_place.get(),
                                                                       self.entry_temperament.get(),
                                                                       self.radical_combobox.get(),
                                                                       self.second_radical_combobox.get()))

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=565, y=350)

        # Entry_fields
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=300, y=40, width=300)

        self.entry_surname = ttk.Entry(self)
        self.entry_surname.place(x=300, y=60, width=300)

        self.entry_appear = ttk.Entry(self)
        self.entry_appear.place(x=300, y=80, width=300)

        self.entry_emotions = ttk.Entry(self)
        self.entry_emotions.place(x=300, y=100, width=300)

        self.entry_work_place = ttk.Entry(self)
        self.entry_work_place.place(x=300, y=120, width=300)

        self.entry_temperament = ttk.Entry(self)
        self.entry_temperament.place(x=300, y=140, width=300)

        # Comboboxes
        self.radical_combobox = ttk.Combobox(self, values=[u'Выберите радикал', u'Истероид', u'Эпилептоид',
                                                           u'Параноял', u'Гипертим', u'Эмотив', u'Тревожный',
                                                           u'Шизоид'])
        self.radical_combobox.current(0)
        self.radical_combobox.place(x=300, y=160)

        self.second_radical_combobox = ttk.Combobox(self, values=[u'Выберите радикал', u'Истероид', u'Эпилептоид',
                                                                  u'Параноял', u'Гипертим', u'Эмотив', u'Тревожный',
                                                                  u'Шизоид', u'-'])
        self.second_radical_combobox.current(0)
        self.second_radical_combobox.place(x=300, y=180)

        # перехватываем все события в дочернем окне чтобы главным было дочернее окно!
        self.grab_set()
        self.focus_set()


class Search(tkinter.Toplevel):

    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('400x100+400+300')
        self.resizable(True, True)

        label_search = tkinter.Label(self, text='Фамилия')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск человека')
        btn_search.place(x=85, y=50)

        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class Help(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()

    def init_search(self):
        self.title('Справка')
        self.geometry('500x400+1300+2')
        self.resizable(True, True)

        self.help_notebook = ttk.Notebook(self)
        self.help_notebook.pack(fill='both', expand=1)

        # Истероидный радикал
        self.text_isteroid = open('Истероид.txt', encoding='utf-8').readlines()
        self.text_isteroid = ''.join(self.text_isteroid)

        self.frame_isteroid = Frame(self.help_notebook,
                                    width=40,
                                    height=30)

        self.frame_isteroid.pack(fill='both', expand=True)
        self.help_notebook.add(self.frame_isteroid, text="Истероид")

        self.text_frame_isteroid = Text(self.frame_isteroid, width=10, height=10)
        self.text_frame_isteroid.insert('end', self.text_isteroid)
        self.text_frame_isteroid.pack(expand=1, fill='both')

        # Эпилептоидный радикал

        # Считывание из файла описания Эпилептоида
        self.text_epileptoid = open('Эпилептоид.txt', encoding='utf-8').readlines()
        self.text_epileptoid = ''.join(self.text_epileptoid)

        self.frame_epileptoid = Frame(self.help_notebook,
                                      width=40,
                                      height=30)

        self.frame_epileptoid.pack(fill='both', expand=True)
        self.help_notebook.add(self.frame_epileptoid, text="Эпилептоид")

        self.text_frame_epileptoid = Text(self.frame_epileptoid, width=10, height=10)
        self.text_frame_epileptoid.insert('end', self.text_epileptoid)
        self.text_frame_epileptoid.pack(expand=1, fill='both')

        # Считывание из файла описания Паранояла
        self.text_paranoyal = open('Параноял.txt', encoding='utf-8').readlines()
        self.text_paranoyal = ''.join(self.text_paranoyal)

        self.frame_paranoyal = Frame(self.help_notebook,
                                     width=40,
                                     height=30)

        self.frame_paranoyal.pack(fill='both', expand=True)
        self.help_notebook.add(self.frame_paranoyal, text="Пароноял")

        self.text_frame_paranoyal = Text(self.frame_paranoyal, width=10, height=10)
        self.text_frame_paranoyal.insert('end', self.text_paranoyal)
        self.text_frame_paranoyal.pack(expand=1, fill='both')

        # Считывание из файла описания Гипертима

        self.text_gipertim = open('Гипертим.txt', encoding='utf-8')
        self.text_gipertim = ''.join(self.text_gipertim)

        self.frame_gipertim = Frame(self.help_notebook,
                                    width=40,
                                    height=30)

        self.frame_gipertim.pack(fill='both', expand=True)
        self.help_notebook.add(self.frame_gipertim, text="Гипертим")

        self.text_frame_gipertim = Text(self.frame_gipertim, width=10, height=10)
        self.text_frame_gipertim.insert('end', self.text_gipertim)
        self.text_frame_gipertim.pack(expand=1, fill='both')

        # Считывание из файла описания Эмотива
        self.text_emotiv = open('Эмотив.txt', encoding='utf-8')
        self.text_emotiv = ''.join(self.text_emotiv)

        self.frame_emotiv = Frame(self.help_notebook,
                                  width=40,
                                  height=30)

        self.frame_emotiv.pack(fill='both', expand=True)
        self.help_notebook.add(self.frame_emotiv, text="Эмотив")

        self.text_frame_emotiv = Text(self.frame_emotiv, width=10, height=10)
        self.text_frame_emotiv.insert('end', self.text_emotiv)
        self.text_frame_emotiv.pack(expand=1, fill='both')

        # Считывание из файла описания Тревожный
        self.text_trevozhniy = open('Тревожный.txt', encoding='utf-8').readlines()
        self.text_trevozhniy = ''.join(self.text_trevozhniy)

        self.frame_trevozhniy = Frame(self.help_notebook,
                                      width=40,
                                      height=30)

        self.frame_trevozhniy.pack(fill='both', expand=True)
        self.help_notebook.add(self.frame_trevozhniy, text="Тревожный")

        self.text_frame_trevozhniy = Text(self.frame_trevozhniy, width=10, height=10)
        self.text_frame_trevozhniy.insert('end', self.text_trevozhniy)
        self.text_frame_trevozhniy.pack(expand=1, fill='both')

        # Считывание из файла описания Шизиод
        self.text_shizoid = open('Шизоид.txt', encoding='utf-8').readlines()
        self.text_shizoid = ''.join(self.text_shizoid)

        self.frame_shizoid = Frame(self.help_notebook,
                                   width=40,
                                   height=30)

        self.frame_shizoid.pack(fill='both', expand=True)
        self.help_notebook.add(self.frame_shizoid, text="Шизоид")

        self.text_frame_shizoid = Text(self.frame_shizoid, width=10, height=10)
        self.text_frame_shizoid.insert('end', self.text_gipertim)
        self.text_frame_shizoid.pack(expand=1, fill='both')


class Update(Child):
    # конструктор класса
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=475, y=350)

        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_surname.get(),
                                                                          self.entry_appear.get(),
                                                                          self.entry_emotions.get(),
                                                                          self.entry_work_place.get(),
                                                                          self.entry_temperament.get(),
                                                                          self.radical_combobox.get(),
                                                                          self.second_radical_combobox.get()))

        self.btn_ok.destroy()


class Define(tkinter.Toplevel):
    def __init__(self):
        super().__init__()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")  # соединяемся с базой данных
        self.c = self.conn.cursor()  # создаем курсор базы данных
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS database(id integer primary key, name text, surname text,
            appear text, emotions text, work_place text, temperament text, base_radical text, second_radical text)''')
        self.conn.commit()

    def insert_data(self, name, surname, appear, emotions, work_place, temperament, base_radical, second_radical):
        # execute выполняет запрос в SQL
        self.c.execute(
            '''INSERT INTO database(name, surname, appear, emotions, work_place, temperament, base_radical, second_radical) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, surname, appear, emotions, work_place, temperament, base_radical, second_radical))

        self.conn.commit()  # сохраняем все результаты в базу данных


if __name__ == "__main__":
    root = tkinter.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('База данных радикалов')
    root.geometry('1250x800')
    root.resizable(True, True)
    root.mainloop()

