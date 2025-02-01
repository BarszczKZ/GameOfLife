#symulacje działają tak jak powinny więc nie trzeba ich zmieniać (chyba że macie pomysł jak je zoptymalizować)
#do ogarniecia na pewno jest design, i rzeczy typu stepcounter, jesli ktos z was wie jak to przepisac by dodac mozliwosc symulowania kilku mrówek to mozna tez to dodać, do poprawienia jest menu tak aby mozna bylo
#bylo wybierać między trybami symulacji, mozna tez dodac możliwosc dobrania prędkości i ilości kroków

from tkinter import *
import time
window = Tk()
window.title("Game of Life")


menu_frame = Frame(window)
menu_frame.grid(sticky="w")
size = 2500 #jest to rozmiar siatki, i lepiej tege nie zmieniac bo wszystko sie rozjedzie
foto = PhotoImage(width=0, height=0) #trik aby przyciski były kwadratowe
mode = "Ant" #tryb symulacji, na początku ustawiony na mrówkę
ant_placed = False #zmienna która sprawdza czy mrówka została już umieszczona na siatce
active = False #zmienna która sprawdza czy symulacja jest aktywna
sqrt_size=int(size**(1/2))
btn=[] 
btn_status = [0] * size  #tworzy początkowa liste statusu przycisków "komórek" (każda komórka na starcie jest martwa "0", żywa ma status "t"), w zależności od statusu zmienia sie kolor komórki 
orientation=3 #orientacja mrówki, można pomyslec nad opcją wyboru orientacji przed startem symulacji
ant_status= [0] * size #tworzy liste na której zapisane jest  na której będzie zapisane w której komórce znajduje sie mrówka
speed=500  #prędkość symulacji
square_size=7 #rozmiar kwadratu na siatce
def ant_simulation():   #to jest funkcja symulacji mrówki
    global ant_status, size, active, speed
    for i in range(size):
        if ant_status[i]=="m":
            ant_movement(i)
            break
    if active==False:
        return
    window.after(speed,ant_simulation)


def click_update(btn,i):   # ta funkcja jest od przycisków na siatce
    def in_func(btn,i):
        global btn_status, ant_status, ant_placed
        if start_stop.cget("text")=="Place Ant":
            ant_status[i]="m"
            start_stop.config(text="Start")
            start_stop.config(state="normal")
        if btn_status[i]==0 and ant_status[i]!="m":
            btn_status[i]=1
        elif btn_status[i]==1 and ant_status[i]!="m":
            btn_status[i]=0
        if btn_status[i]==1:
            btn.config(bg="black")
        if btn_status[i]==0:
            btn.config(bg="white")
        if ant_status[i]=="m":
            btn.config(bg="red")
    return(lambda: in_func(btn,i))



def which_neighbor(i,ant_neighbors): #przesuwa mrówke do właściwego sąsiada i obraca ją
    global orientation, btn_status, ant_status, btn
    if btn_status[i]==0:
        orientation=(orientation+1)%4#orientacja koreluje z miejscem "sąsiada" na liście wiec w zaleznosci od orientacji wybierany jest odpowiedni sąsiad
        ant_status[i]=0
        ant_status[i+ant_neighbors[orientation]]="m"
        btn[i+ant_neighbors[orientation]].config(bg="red")
        btn[i].config(bg="black")
        btn_status[i]=1
        
    elif btn_status[i]==1:
        orientation-=1
        if orientation<0:
            orientation=3
        ant_status[i]=0
        ant_status[i+ant_neighbors[orientation]]="m"
        btn[i+ant_neighbors[orientation]].config(bg="red")
        btn[i].config(bg="white")
        btn_status[i]=0
        
    
def ant_movement(i):
    global size,  sqrt_size
    s=size
    sqr=sqrt_size
    if i == s-1:  #poniższy kod sprawdza jakich sąsiadów posiada dana komórka
        ant_neighbors = [1-sqr, -s+sqr, -1, -sqr]
    elif i == s-sqr:
        ant_neighbors = [+1, -s+sqr, sqr-1, -sqr]
    elif i ==0:
        ant_neighbors = [+1, sqr, sqr-1, s-sqr]
    elif i==sqr-1:
        ant_neighbors = [1-sqr, sqr, -1, s-sqr]
    elif (i + 1) % sqr == 0:
        ant_neighbors = [1-sqr, sqr, -1, -sqr]
    elif i % sqr == 0 :
        ant_neighbors = [+1, sqr, sqr-1, -sqr]
    elif i < sqr :
        ant_neighbors = [+1, sqr, -1, s-sqr]
    elif i > s-sqr :
        ant_neighbors = [+1, -s+sqr, -1, -sqr]
    else:
        ant_neighbors = [+1, sqr, -1, -sqr]
    which_neighbor(i, ant_neighbors)

def count_neighbors(i, neighbors): # Liczy sąsiadów zadanej komórki 
    global btn_status
    k=0
    for n in range(8):
        w=0
        w=i+neighbors[n]
        if btn_status[w]==1:
            k+=1
    return k
def gl_simulation(): #symulacja "gry w życie"
    global btn_status, btn, size, sqrt_size, active, speed
    s= size
    sqr= sqrt_size
    btn_status_copy = [0] *s
    
    for i in range(s):
        k = 0
        if i == s-1: #poniższy kod sprawdza jakich sąsiadów posiada dana komórka
            neighbors = [-s+sqr, -s+1, 1-s+sqr, -1, -sqr-1, -sqr, -(2*sqr)+1, 1-sqr]
        elif i == s-sqr:
            neighbors = [-s+sqr, 1-s+2*sqr, -s-1+sqr, +1, -1, 1-sqr, -sqr, sqr-1]
        elif i ==0:
            neighbors = [1+s-sqr, s-sqr, s-1, +1, 2*sqr-1, sqr, sqr-1, sqr+1]
        elif i==sqr-1:
            neighbors = [s-sqr, s-2*sqr+1, s-sqr-1, +1, -1, 1-sqr, sqr, sqr-1]
        elif (i + 1) % sqr == 0:
            neighbors = [-(2*sqr)+1, 1-sqr, +1, sqr, sqr-1, -sqr-1, -1, -sqr]
        elif i % sqr == 0:
            neighbors = [2*sqr-1, sqr-1, -1, -sqr, 1-sqr, +1, sqr+1, sqr]
        elif i < sqr:
            neighbors = [+1, -1, sqr-1, sqr, sqr+1, 1+s-sqr, s-sqr-1, s-sqr]
        elif i > s-sqr:
            neighbors = [1-s+sqr, -s-1+sqr, -s+sqr, +1, -1, -sqr, -sqr-1, 1-sqr]
        else:
            neighbors = [+1, -1, sqr, -sqr, -sqr-1, sqr+1, 1-sqr, sqr-1]

        k = count_neighbors(i, neighbors)

        if btn_status[i] == 0 and k == 3:
            btn_status_copy[i] = 1
            btn[i].config(bg="black")
        elif btn_status[i] == 1:
            if k != 2 and k != 3:
                btn_status_copy[i] = 0
                btn[i].config(bg="white")
            else:
                btn_status_copy[i] = 1
    
    btn_status.clear()
    btn_status.extend(btn_status_copy)
    if active==False:
        return
    window.after(speed,gl_simulation)


  

def change_size_fun():
    global size, sqrt_size, btn, window, grid_window, btn_status, ant_status, ant_placed
    size = int(size_entry.get())**2
    sqrt_size=int(size**(1/2))
    btn.clear()
    btn_status.clear()
    btn_status = [0] * size
    ant_status.clear()
    ant_status = [0] * size
    grid_window.destroy()
    grid_window = Toplevel(window)
    if ant_placed==True:
        ant_placed=False
    square_size=400//sqrt_size
    for i in range(size): #tutaj tworzy sie siatka przycisków
        btn.append(Button(grid_window,image=foto,width=square_size,height=square_size))
        btn[i].grid(row=int(i//sqrt_size),column=int(i%sqrt_size),sticky="w")
        btn[i].config(bg="white", command=click_update(btn[i],i))
    
def start_stop_fun():
    global start_stop, mode, ant_placed, active, clear_grid, change_size_btn, mode_btn
    if start_stop.cget("text")=="Start":
        active=True
        start_stop.config(text="Stop")
        clear_grid.config(state="disabled")
        change_size_btn.config(state="disabled")
        mode_btn.config(state="disabled")
        if mode=="Ant" and ant_placed==False:
            start_stop.config(text="Place Ant")
            start_stop.config(state="disabled")
            ant_placed=True
        elif mode=="Ant" and ant_placed==True:
            ant_simulation()
        elif mode=="Life":
            gl_simulation()
    elif start_stop.cget("text")=="Stop":
        start_stop.config(text="Start")
        active=False
        clear_grid.config(state="normal")
        change_size_btn.config(state="normal")
        mode_btn.config(state="normal")

def clear_grid_fun():
    global btn_status, btn, ant_placed, ant_status
    for i in range(size):
        btn_status[i]=0
        if ant_status[i]=="m":
            ant_status[i]=0
        btn[i].config(bg="white")
    if ant_placed==True:
        ant_placed=False

def change_mode_fun():
    global mode_btn, mode
    if mode_btn.cget("text")=="Langstone Ant Mode":
        mode = "Life"
        mode_btn.config(text="Game of Life Mode")
    elif mode_btn.cget("text")=="Game of Life Mode":
        mode = "Ant"
        mode_btn.config(text="Langstone Ant Mode")

def change_speed_fun():
    global change_speed, speed
    if change_speed.cget("text")=="Speed: 1":
        speed=200
        change_speed.config(text="Speed: 2")
    elif change_speed.cget("text")=="Speed: 2":
        speed=10
        change_speed.config(text="Speed: 3")
    elif change_speed.cget("text")=="Speed: 3":
        speed=1
        change_speed.config(text="Speed: 4")
    elif change_speed.cget("text")=="Speed: 4":
        speed=500
        change_speed.config(text="Speed: 1")

clear_grid = Button(menu_frame,text="Clear grid", font=("Arial",20), width=18, height=3, command = clear_grid_fun)
clear_grid.grid(sticky="w")

change_size = Label(menu_frame, text="Change size (1-99)", font=("Arial",20))
change_size.grid(sticky="w")
change_size_btn = Button(menu_frame, text="Change", font=("Arial",20), width=18, height=3, command = change_size_fun)
change_size_btn.grid(sticky="w")
size_entry = Entry(menu_frame,  font=("Arial",20))
size_entry.insert(0, sqrt_size)
size_entry.grid(sticky="w")

start_stop = Button(menu_frame, text="Start", font=("Arial",20), width=18, height=3, command = start_stop_fun)
start_stop.grid(sticky="w")

mode_btn = Button(menu_frame, text="Langstone Ant Mode", font=("Arial",20), width=18, height=3, command = change_mode_fun)
mode_btn.grid(sticky="w")

change_speed = Button(menu_frame, text="Speed: 1", font=("Arial",20), width=18, height=3, command=change_speed_fun)
change_speed.grid(sticky="w")

grid_window = Toplevel(window)
for i in range(size): #tutaj tworzy sie siatka przycisków
    btn.append(Button(grid_window,image=foto,width=square_size,height=square_size))
    btn[i].grid(row=int(i//sqrt_size),column=int(i%sqrt_size),sticky="w")
    btn[i].config(bg="white", command=click_update(btn[i],i))


window.mainloop()