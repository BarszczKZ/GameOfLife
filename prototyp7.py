#symulacje działają tak jak powinny więc nie trzeba ich zmieniać (chyba że macie pomysł jak je zoptymalizować)
#do ogarniecia na pewno jest design, i rzeczy typu stepcounter, jesli ktos z was wie jak to przepisac by dodac mozliwosc symulowania kilku mrówek to mozna tez to dodać, do poprawienia jest menu tak aby mozna bylo
#bylo wybierać między trybami symulacji, mozna tez dodac możliwosc dobrania prędkości i ilości kroków

from tkinter import *
import time
import sys
window = Tk()
window.title("Game of Life")
window.geometry("700x910")
frame = Frame(window)
frame.grid(sticky="w")
menu_frame = Frame(window)
menu_frame.grid(sticky="w")
size = 2500 #jest to rozmiar siatki, i lepiej tege nie zmieniac bo wszystko sie rozjedzie
btn=[] 
status = [0] * size  #tworzy początkowa liste statusu (każda komórka na starcie jest martwa)
menu_status=0 
orientation=3 #orientacja mrówki, można pomyslec nad opcją wyboru orientacji przed startem symulacji
a_status= [0] * size #tworzy liste statusu na której będzie zapisane w której komórce znajduje sie mrówka
steps=1000  #ilosc kroków w symulacji życia, ale da sie tez ja zrobic dla nieskonczonej ilosci kroków
def simulation():   #to jest funkcja symulacji mrówki
    global menu_status, a_status, size
    while 1>0:
        time.sleep(1)
        window.update()
        for i in range(size):
            if a_status[i]=="m":
                ant_movement(i)
                break
        if menu_status==0:
            break
    return

def click_update(btn,i):   # ta funkcja jest od przycisków na siatce
    def in_func(btn,i):
        global status, menu_status, a_status
        if menu_status==1:
            a_status[i]="m"
            menu_status=2
            menu.config(text="Start Simulation")
        if status[i]==0 and menu_status==0:
            status[i]=1
        elif status[i]==1 and menu_status==0:
            status[i]=0
        if status[i]==1:
            btn.config(bg="black")
        if status[i]==0:
            btn.config(bg="white")
        if a_status[i]=="m":
            btn.config(bg="red")
    return(lambda: in_func(btn,i))

def menu_fun():  #ta funkcja jest od przycisku menu, ale na razie obsługuje tylko symulacje mrówki
    global menu_status, btn, status, a_status, orientation
    if menu_status==0:
        menu_status=1
        print(menu_status)
    if menu_status==3:
        for i in range(size):
            a_status[i]=0
            status[i]=0
            btn[i].config(state=NORMAL,bg="white")
        menu.config(text="Place Ant")
        menu_status=0
        orientation=3
    if menu_status==2:
        for i in range(size):
            btn[i].config(state=DISABLED)
        menu.config(text="Restart Simulation")
        menu_status=3
        simulation()

def which_neighbor(i,ant_neighbors):
    global orientation, status, a_status, btn
    if status[i]==0:
        orientation=(orientation+1)%4
        a_status[i]=0
        a_status[i+ant_neighbors[orientation]]="m"
        btn[i+ant_neighbors[orientation]].config(bg="red")
        btn[i].config(bg="black")
        status[i]=1
        
    elif status[i]==1:
        orientation-=1
        if orientation<0:
            orientation=3
        a_status[i]=0
        a_status[i+ant_neighbors[orientation]]="m"
        btn[i+ant_neighbors[orientation]].config(bg="red")
        btn[i].config(bg="white")
        status[i]=0
        
    
def ant_movement(i):
    
    if i == 2499:
        ant_neighbors = [-49, -2450, -1, -50]
    elif i == 2450:
        ant_neighbors = [+1, -2450, +49, -50]
    elif i ==0:
        ant_neighbors = [+1, +50, +49, +2450]
    elif i==49:
        ant_neighbors = [-49, +50, -1, +2450]
    elif (i + 1) % 50 == 0 and i != 49 and i != 2499:
        ant_neighbors = [-49, +50, -1, -50]
    elif i % 50 == 0 and i != 0 and i != 2450:
        ant_neighbors = [+1, +50, +49, -50]
    elif i < 50 and i != 0 and i != 49:
        ant_neighbors = [+1, +50, -1, +2450]
    elif i > 2450 and i != 2450 and i != 2499:
        ant_neighbors = [+1, -2450, -1, -50]
    elif i < 2450 and i >= 50 and (i + 1) % 50 != 0 and i % 50 != 0:
        ant_neighbors = [+1, +50, -1, -50]
    which_neighbor(i, ant_neighbors)



def color_change(i):    # wsm nie wiem czy gdzies tego użylem, jesli nie to mozna wyjebac
    global btn, status
    if status[i]==0:
        btn[i].config(bg="white")
    elif status[i]==1:
        btn[i].config(bg="white")
def count_neighbors(i, neighbors): # Liczy sąsiadów zadanej komórki i
    global status
    k=0
    for n in range(8):
        if status[i+neighbors[n]]==1:
            k+=1
    return k
def gl_simulation():
    global status, btn,  menu_status
    while True:
        status_copy = [0] *2500
        for i in range(2500):
            k = 0
            if i == 2499:
                neighbors = [-2450, -2499, -2451, -1, -51, -50, -99, -49]
            elif i == 2450:
                neighbors = [-2450, -2401, -2449, +1, -1, -49, -50, +49]
            elif i ==0:
                neighbors = [+2451, +2450, +2499, +1, +99, +50, +49, +51]
            elif i==49:
                neighbors = [+2450, +2401, +2449, +1, -1, -49, +50, +49]
            elif (i + 1) % 50 == 0 and i != 49 and i != 2499:
                neighbors = [-99, -49, +1, +50, +49, -51, -1, -50]
            elif i % 50 == 0 and i != 0 and i != 2450:
                neighbors = [+99, +49, -1, -50, -49, +1, +51, +50]
            elif i < 50 and i != 0 and i != 49:
                neighbors = [+1, -1, +49, +50, +51, +2451, +2449, +2450]
            elif i > 2450 and i != 2450 and i != 2499:
                neighbors = [-2451, -2449, -2450, +1, -1, -50, -51, -49]
            elif i < 2450 and i >= 50 and (i + 1) % 50 != 0 and i % 50 != 0:
                neighbors = [+1, -1, +50, -50, -51, +51, -49, +49]

            k = count_neighbors(i, neighbors)

            if status[i] == 0 and k == 3:
                status_copy[i] = 1
                btn[i].config(bg="black")
            elif status[i] == 1:
                if k != 2 and k != 3:
                    status_copy[i] = 0
                    btn[i].config(bg="white")
                else:
                    status_copy[i] = 1

        status.clear()
        status.extend(status_copy)
        window.update()

    

for i in range(size): #tutaj tworzy sie siatka przycisków
    btn.append(Button(frame,font=("Arial",3),width=2,height=2))
    btn[i].grid(row=int(i//50),column=int(i%50),sticky="w")
    btn[i].config(bg="white", command=click_update(btn[i],i))
menu = Button(menu_frame,text="Place Ant", font=("Arial",20), width=18,height=3, command = menu_fun) #tworzy przycisk menu
menu.grid( sticky="w")
test = Button(window, text="Start", font=("Arial",20),width=5, height=3, command = gl_simulation) #ten przycisk jest tymczasowy, uruchamia symulacje gry w życie
test.place(x=350,y=700)
window.mainloop()
