import configparser, pysftp, time
import tkinter, os
from datetime import date
from threading import Thread
from tkinter import *
import tkinter.ttk as ttk
from mylib import *

# -*- coding: utf-8 -*-
"""
jsCreator.py
Created on 2023-10-01 12:00:00
as jsSofts  
"""

class application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("jsCreator for PW")
        self.master.geometry("420x250")        
        self.create_widgets()

    def create_widgets(self):
        # Создаем панель для вкладок
        self.Notebook = ttk.Notebook(self.master)
        self.Notebook.pack(fill=BOTH, expand=True)

        self.frame1 = ttk.Frame(self.Notebook)
        self.frame2 = ttk.Frame(self.Notebook)
        self.frame3 = ttk.Frame(self.Notebook)

        self.Notebook.add(self.frame1, text='Обновление')
        self.Notebook.add(self.frame2, text='Дканжи')
        self.Notebook.add(self.frame3, text='Пути')

        self.server = myServer()

        self.status = tkinter.Frame(self.master)
        self.status.pack(side=BOTTOM, fill=X)

        self.sb = tkinter.Label(self.status, text='Отчет : ')
        self.sb.pack(side=LEFT, fill=Y)

        self.panel = Frame(self.master)
        self.panel.pack(side=BOTTOM, fill=X)

        self.instance = ttk.Treeview(self.frame2, columns=("Name", "Coment"), show='headings')
        self.instance.heading("Name", text="Лока")
        self.instance.heading("Coment", text="Цель")
        self.instance.pack(expand=1, fill=BOTH, padx=2, pady=5)
        self.instance.column("Name", width=120)
        self.instance.column("Coment", width=280, anchor = "center")

        self.instance.bind("<Double-Button-1>", self.onMouseClick)

        # Панель для отображения хода работы
        self.tress = ttk.Treeview(self.frame1, columns=("File", "Report"), show='headings')
        self.tress.heading("File", text="Файл")
        self.tress.heading("Report", text="Отчет")
        self.tress.pack(expand=1, fill=BOTH, padx=2, pady=5)
        self.tress.column("File", width=150)
        self.tress.column("Report", width=250, anchor = "center")

         # Добавление вертикальной полосы прокрутки для Treeview
        self.scrollbar = ttk.Scrollbar(self.tress, orient="vertical", command=self.tress.yview)
        self.tress.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)

         # Добавление вертикальной полосы прокрутки для Treeview
        self.scrollbar = ttk.Scrollbar(self.instance, orient="vertical", command=self.instance.yview)
        self.instance.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Настройка тегов для цветовой маркировки
        self.tress.tag_configure('black', background='#000000')
        self.tress.tag_configure('gray', background='#cccccc')
        self.tress.tag_configure('grin', background='#00ff00')
        self.tress.tag_configure('red', background="#ff0000")
        self.tress.tag_configure('blue', background="#0000ff")
        self.tress.tag_configure('yellow', background="#ffff00")
        self.tress.tag_configure('purpure', background="#ff00ff")

        # задаем шаблоны цвета для шрифта
        self.tress.tag_configure('f_black', foreground='#000000')
        self.tress.tag_configure('f_gray', foreground='#cccccc')
        self.tress.tag_configure('f_grin', foreground='#00ff00')
        self.tress.tag_configure('f_red', foreground="#ff0000")
        self.tress.tag_configure('f_blue', foreground="#0000ff")
        self.tress.tag_configure('f_yellow', foreground="#ffff00")
        self.tress.tag_configure('f_purpure', foreground="#ff00ff")

        # Настройка тегов для цветовой маркировки        
        self.instance.tag_configure('grin', foreground='#0000ff')
        self.instance.tag_configure('red', foreground='#ff0000')
        
        # Добавляем меню
        self.menu_bar = tkinter.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        self.settings_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Файл", menu=self.settings_menu)
        self.settings_menu.add_command(label="Обновить", command=self.skan, accelerator="Ctrl+S")
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Открыть настройки", command=lambda: os.startfile('settings.ini'))
        self.settings_menu.add_command(label="Открыть список сервера", command=lambda: os.startfile('serverlist.txt'))
        self.settings_menu.add_command(label="Открыть папку скрипта", command=lambda: os.startfile(os.getcwd()))
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Обновить параметры", command = self.load_settings)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Выход", command=self.master.quit)

        self.master.bind_all("<Control-s>", lambda event: self.skan())

        self.server_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Сервер", menu=self.server_menu)
        self.server_menu.add_command(label="Остановить", command = self.server.sv_stop)
        self.server_menu.add_command(label="Запустить", command = self.server.sv_start)
        self.server_menu.add_command(label="Power Off", command=self.server.sv_poweroff)
        self.server_menu.add_command(label="Создать обновление", command = self.server.sv_update)


        self.load_settings()  # Загрузка настроек при инициализации приложения
        
        self.label = tkinter.Button(self.status, text="Проверка")
        self.label.config(command=self.onTimer)
        self.label.pack(side=LEFT, padx=5, pady=0)

        self.sbtext = tkinter.Label(self.status, text='nill')
        self.sbtext.pack(side=LEFT, fill=Y)

        self.tmr = Thread(target = self.onTimer, daemon=True).start()        

    def onMouseClick(self, event):
            """Обработчик клика мыши по элементу self.instance."""
            item_id = self.instance.identify_row(event.y)
            if item_id:
                values = self.instance.item(item_id, "values")[0]
                self.server.sv_comand(values)
            self.instance.selection_remove(self.instance.selection())

    def onTimer(self):
        while True:            
            try:            
                if self.server.sv_check(self.label):
                    r = self.server.sv_scan()
                    d = 0
                    for items in self.instance.get_children():
                        self.master.update_idletasks()
                        it = self.instance.item(items, 'values')[0]
                        cp = self.instance.item(items, 'values')[1]
                        self.sbtext.config(text=f"Обновление {it}...")
                        if it in r:
                            self.instance.item(items, values=(it, cp), tags=('grin'))
                        else:
                            self.instance.item(items, values=(it, cp), tags=('red'))
                        d += 1
                        if d > 100: break
            finally:
                time.sleep(10)

    def clear_instance(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    # Загрузка настроек из файла
    def load_settings(self):
        # Получаем полный путь к файлу настроек
        self.clear_instance(self.instance)
        self.clear_instance(self.tress)

        fn = os.path.join(os.getcwd(), 'settings.ini')
        if os.path.exists(fn):
            config = configparser.ConfigParser()
            config.read(fn)
            # Загрузка учетных данных            
            self.server.Host = config.get('Settings', 'address', fallback='localhost')
            self.server.User = config.get('Settings', 'username', fallback='User')
            self.server.Passwd = config.get('Settings', 'Password', fallback='qwerty')                  
            self.server.Port = config.get('Settings', 'port', fallback='22')

        List = config.options("Inst")
        for inst in List:
            comit = config.get("Inst", inst, fallback="nill")
            self.instance.insert("", "end", values=(inst, comit))

        SelfPath = os.getcwd()
        ScanPath = SelfPath + '\\new'        
        # Проверяем наличие папки new, если нет, то выходим
        if not os.path.exists(ScanPath): return()
        # Получаем список файлов из папки new
        List = os.listdir(ScanPath)            
        for line in List:            
            line = line.strip()
            if '.bak' in line: continue
            file_name = ScanPath + '\\' + line
            if not os.path.isfile(file_name): continue  # Пропускаем, если это не файл
            hash = config.get(line, 'md5', fallback = 0)            
            if hash != self.server.hash_file(file_name):
                self.tress.insert("", "end", values=(line, "Изменен..."), tags=('gray', 'f_red',))                                
    
    def skan(self):               
        # Получаем путь к папке скрипта
        SelfPath = os.getcwd()
        ScanPath = SelfPath + '\\new'        

        def copy_file_to_server(item, localpath, hash):
            """Копирует файл на сервер."""
            List = open(SelfPath + '\\serverlist.txt', 'r').readlines()
            ls = open('server.log', 'a')
            d = date.today()
            ls.write(f"[{d}]\n")
            self.sbtext.config(text=localpath)
            file_name = os.path.basename(localpath)
            rr = False                        
            for line in List:
                line = line.strip()
                if not line: continue
                if not line.startswith('/'): continue  # Пропускаем, если строка не начинается с '/'
                try:                    
                    if os.path.basename(line) == file_name:
                        with pysftp.Connection(host=self.server.Host, username=self.server.User, password=self.server.Passwd) as sftp:
                            sftp.put(localpath=localpath, remotepath=line, confirm=True)                            
                            self.tress.item(item, values=(file_name, "Файл обновлен..."), tags=('grin', 'f_purpure'))
                            ls.write(f"{file_name} = {line}\n")
                            rr = True
                except Exception as e:
                    ls.write(f"{file_name} - Ошибка: {e}\n")
                    self.tress.item(item, values=(file_name, f"Ошибка : {e}"), tags=('f_red', 'black'))               

            ls.close()
            if rr: 
                config.set(file_name, 'md5', hash)                
                
            with open('settings.ini', 'w') as configfile: config.write(configfile)
            if not rr:
                self.sbtext.config(text=f'Для {file_name} не указаны пути для копирования.')
            return rr

        # чтение списка из файла serverlist.txt        
        for item in self.tress.get_children():
            self.master.update_idletasks()  # Обновляем интерфейс
            file_name = self.tress.item(item, 'values')[0]                        
            # проверка наличия файла в папке скрипта
            file_path = os.path.join(ScanPath, file_name)
            if os.path.exists(file_path):
                # проверяем наличие категории file_name в settings.ini
                config = configparser.ConfigParser()                            
                config.read('settings.ini')
                file_hash = self.server.hash_file(file_path)
                if config.has_section(file_name):                            
                    hash = config.get(file_name, 'md5', fallback = 0) # Читаем старый хеш                    
                    if file_hash == hash:
                        # Файлы совпадают, отмечаем строчку желтым цветом                                    
                        self.tress.item(item, values=(file_name, "Не менялся"), tags=('yellow', 'f_gray'))                        
                    else:
                        # Файлы не совпадают, копируем файл на сервер
                        copy_file_to_server(item, file_path, file_hash)  # Копируем файл на сервер
                else: # Отсутствует секция в настройках                                        
                    if copy_file_to_server(item, file_path, file_hash):  # Копируем файл на сервер
                        config.add_section(file_name)
            else:
                # Файл не найден в папке для обновлений, отмечаем строчку серым цветом
                self.tress.item(item, values=(file_name, "Файл не найден"), tags=('gray',))

        # сканирование завершено, выводим окно с сообщением
        messagebox = tkinter.messagebox.showinfo("Сканирование", "Сканирование завершено. Проверьте результаты в таблице.")              
            
root = Tk()
app = application(master=root)
root.mainloop()