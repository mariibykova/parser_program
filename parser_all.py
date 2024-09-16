import requests
import pandas as pd
import pathlib
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import os
from fake_useragent import UserAgent

def name_addres(): # функция формирования названия файла
   s = "/Users/mariibykova/Desktop/file.txt"
   infile = open(s, 'r+') #cчитали файл file.txt
   lines = infile.readlines()

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
      
def parser12():
   adres = adres_tf.get() #путь, введенный пользователем

   # получение текущей даты и времени
   real_data = datetime.now()
   data = str(real_data.day) + "_" + str(real_data.month) + "_" + str(real_data.year) + "___" 
   data +=  str(real_data.hour) + "_" + str(real_data.minute) + "_" + str(real_data.second) + "___"

   path = os.path.join(adres, data)
   os.chdir(adres) # переходим в нужную директорию
   os.mkdir(data)  # создаем в ней папку
   adres+= "/"+data +"/" # дополняем путь

   s = "/Users/mariibykova/Desktop/file1.txt"
   infile = open(s, 'r+') #cчитали файл file1.txt со всеми ссылками 
   lines = infile.readlines()
   i =0
   os.chdir(adres) # переход в директорию по адресу
   
   while(i<len(lines)): # проход по файлу
      # если встретили цифру - смена университета, иначе парсим
      if(lines[i].strip() == "1"):
         os.mkdir("sgtu")
         adres1 = adres+"/sgtu"
         i+=1
      elif (lines[i].strip()=="4"):
         os.mkdir("sgu")
         adres1 = adres+"/sgu"
         i+=1
      elif (lines[i].strip()=="2"):
         os.mkdir("rtu")
         adres1 = adres+"/rtu"

         i+=1
      elif (lines[i].strip()=="3"):
         os.mkdir("spbgu")
         adres1 = adres+"/spbgu"

         i+=1
      elif (lines[i].strip()=="6"):
         os.mkdir("misis")
         adres1 = adres+"/misis"
         i+=1
      elif (lines[i].strip()=="5"):
         os.mkdir("sgu")
         adres1 = adres+"/sgu"
         i+=1
      elif (lines[i].strip()=="7"):
         os.mkdir("mipt")
         adres1 = adres+"/mipt"
         i+=1
      elif (lines[i].strip()=="8"):
         os.mkdir("mephi_fio")
         adres1 = adres+"/mephi_fio"
         i+=1
      elif (lines[i].strip()=="9"):
         os.mkdir("mephi_snils")
         adres1 = adres+"/mephi_snils"
         i+=1
      
      elif (lines[i].strip()=="10"):
         os.mkdir("guap")
         adres1 = adres+"/guap"
         i+=1
      
      elif (lines[i].strip()=="11"):
         os.mkdir("spbgeu")
         adres1 = adres+"/spbgeu"
         i+=1
      
      elif (lines[i].strip()=="12"):
         os.mkdir("mei")
         adres1 = adres+"/mei"
         i+=1
      elif (lines[i].strip()=="13"):
         os.mkdir("mtusi")
         adres1 = adres+"/mtusi"
         i+=1
      elif (lines[i].strip()=="14"):
         os.mkdir("rudn")
         adres1 = adres+"/rudn"
         i+=1

      elif (lines[i].strip()=="15"):
         os.mkdir("miet")
         adres1 = adres+"/miet"
         i+=1
      
      
      
      else:
         name = lines[i].strip()
         url = lines[i+1].strip()
         parser(name, url,adres1)
         i +=2

   # сообщение, что успешно завершена работа парсера      
   messagebox.showinfo('ParserINFO', f'Файл с данными сформирован!')
   adres_tf.delete(0, END)
   
def parser(name, url, adres):
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

   name = adres +"/"+  name # обновление адреса
   UserAgent().chrome
   s1 = '.csv'            # строка с расширением (для формирования названия)
   page = requests.get(url, headers={'User-Agent': UserAgent().chrome}) 
   soup = BeautifulSoup(page.text, 'lxml') # получаем код html-cтраницы

   table1 = soup.find('table') # поиск первой таблицы
   k = 0 # счетчик таблиц на странице
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
         rows.append(row)  # добавляем строку в массив данных 
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

# оконное приложение
window = Tk() # cоздаём окно приложения
window.title('Parser all') # вызов функции парсеринга
window.geometry('600x300') # размеры окна
frame = Frame(
   window,  # обязательный параметр, указывающий окно для размещения Frame
   padx=10, # отступ по горизонтали
   pady=10  # отступ по вертикали
)
frame.pack(expand=True)

adres_lb = Label( # надпись 
   frame,
   text="Введите путь  ",
)
adres_lb.grid(row=1, column=1)

adres_tf = Entry( # текстовое поле 
   frame,
)
adres_tf.grid(row=2, column=1, pady=4)

pars_btn = Button( # кнопка
   frame,
   text='Спарсить',
   command=parser12,
)
pars_btn.grid(row=3, column=1)

def on_closing(): 
   if messagebox.askokcancel("Выход", "Вы хотите выйти?"):
      window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop() # вызов окна для взаимодействия с пользователем


