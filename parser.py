import requests
import pandas as pd
import pathlib
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from fake_useragent import UserAgent

def name_addres(): # функция формирования названия файла и адреса
   s = "/Users/mariibykova/Desktop/file.txt"
   infile = open(s, 'r+') #cчитали файл file.txt
   lines = infile.readlines()
   if lines==[]:
      lines=["",""]
   name1 = lines[0].strip() #название, записанное в файле file.txt
   addr1 = lines[1].strip() #путь, записанный в файле file.txt
   infile.close()
   infile = open(s,'w')
   infile.close()
   infile = open(s, 'r+') #очистили файл file.txt
   name = name_tf.get()   #название, введенное пользователем
   adres = adres_tf.get() #путь, введенный пользователем
   if name == "": #если пользователь не ввел название файла
      name = name1
   else:
      name1=name
   if adres == "":#если пользователь не ввел путь
      adres = addr1
   else:
      addr1=adres
   lines = [name1, addr1]
   for  line in lines: #сохраняем данные в файл file.txt
      infile.write(line + '\n')
   return lines
      


def parser():
   # получение текущей даты и времени
   real_data = datetime.now()
   data = "___" + str(real_data.day) + "_" + str(real_data.month) + "_" + str(real_data.year) + "___" 
   data +=  str(real_data.hour) + "_" + str(real_data.minute) + "_" + str(real_data.second) + "___"

   url = url_tf.get()    # получаем ссылку на сайт

   # выгрузка имени и адреса
   a = []
   a = name_addres()
   name = a[0]
   adres= a[1]

   # проверка возможных ошибок 
   if (url == ""):    
      messagebox.showinfo('ParserINFO', f'Не введен адрес ссылки!')
      return
   if (name == ""):
      messagebox.showinfo('ParserINFO', f'Не введено название файла!')
      return
   if (adres == ""): 
      messagebox.showinfo('ParserINFO', f'Не введен путь!')
      return
   
   # обновление адреса
   name += data
   name = adres +"/"+  name
   
   # парсинг
   UserAgent().chrome
   s1 = '.csv'            # строка с расширением (для формирования названия)
   page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
   print(page.text)
   soup = BeautifulSoup(page.text, 'lxml') # получаем код html-cтраницы
   table1 = soup.find('table') # поиск первой таблицы
   k = 0 # счетчик таблиц
   mydata1 = pd.DataFrame() # определяем фрейм данных
   add = []
   rows = [] # список для строк таблиц
   for table1 in soup.find_all('table',): # пока на странице есть таблицы
      headers = [] # пустой список для колонок таблицы
      for i in table1.find_all('th'): # пока есть колонки
         title = i.text
         headers.append(title) # добавляем колонку в список
      mydata = pd.DataFrame(columns = headers) # определяем в фрейме столбцы
      mydata3 = pd.DataFrame(columns = headers)
      k = 0
      row = ""
      for j in table1.find_all('tr')[1:]: # строка находится внутри тега <tr>
         row_data = j.find_all('td')     # элементы — внутри тега <td>
         row = [i.text for i in row_data] #получаем данные и сохраняем их
         rows.append(row) # добавляем строку в массив данных
           #length = len(mydata)
           #mydata.loc[length] = row
           #mydata = mydata.append(row, ignore_index = False )
      k +=1
      # записываем все в фрейм
      mydata = pd.DataFrame(rows, columns=[""]*max(len(i) for i in rows))
       #mydata1 = pd.concat([mydata1, mydata3]) # склеиване двух фреймов
       #mydata1 = pd.concat([mydata1, mydata])
      add.append(mydata)
      s = name+s1 # формирование строки с названием
      mydata.to_csv(s, index=False) # экспорт данныx в CSV-файл
      # если на странице больше одной таблицы, то делим их в разные файлы
      s = ''
      k = 1
      if (len(add)>1):
         for i in add:
            s =name+str(k)+s1
            k += 1
            i.to_csv(s, index=False)

   # сообщение об успешном завершении работы парсера          
   messagebox.showinfo('ParserINFO', f'Файл с данными сформирован!')
   url_tf.delete(0, END)
   name_tf.delete(0, END)
   adres_tf.delete(0, END)

# оконное приложение
window = Tk() # cоздаём окно приложения
window.title('Parser') # вызов функции парсеринга
window.geometry('600x300') # размеры окна
frame = Frame(
   window,  # обязательный параметр, указывающий окно для размещения Frame
   padx=10, # отступ по горизонтали
   pady=10  # отступ по вертикали
)
frame.pack(expand=True)

url_lb = Label( # надпись 1
   frame,
   text="Введите адрес ссылки  "
)
url_lb.grid(row=4, column=2)

url_tf = Entry( # текстовое поле 1
   frame,
)
url_tf.grid(row=5, column=2, pady=4)

name_lb = Label( # надпись 2
   frame,
   text="Введите название файла  ",
)
name_lb.grid(row=1, column=1)

name_tf = Entry( # текстовое поле 2 
   frame,
)
name_tf.grid(row=2, column=1, pady=4)

adres_lb = Label( # надпись 3
   frame,
   text="Введите путь  ",
)
adres_lb.grid(row=1, column=3)

adres_tf = Entry( # текстовое поле 3
   frame,
)
adres_tf.grid(row=2, column=3, pady=4)

pars_btn = Button( # кнопка
   frame,
   text='Спарсить',
   command=parser
)
pars_btn.grid(row=7, column=2)

def on_closing(): # оконное приложение
   if messagebox.askokcancel("Выход", "Вы хотите выйти?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop() # вызов окна для взаимодействия с пользователем


