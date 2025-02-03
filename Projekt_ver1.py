from tkinter import *

window = Tk()
window.title("Project Menu")
menu_frame = Frame(window)
menu_frame.grid(sticky="w")
size = 2500 #jest to rozmiar siatki, na początku ustawiony na 50x50
foto = PhotoImage(width=0, height=0) #trik aby przyciski były kwadratowe
mode = "Ant" #tryb symulacji, na początku ustawiony na mrówkę
ant_placed = False #zmienna która sprawdza czy mrówka została już umieszczona na siatce
active = False #zmienna która sprawdza czy symulacja jest aktywna
sqrt_size=int(size**(1/2)) #pierwiastek z rozmiaru siatki
btn=[] # deklaracja lisy przycisków na siatce
btn_status = [0] * size  #tworzy początkowa liste statusu przycisków "komórek" (każda komórka na starcie jest martwa "0", żywa ma status "1"), w zależności od statusu zmienia sie kolor komórki 
orientation=3 #orientacja mrówki, można pomyslec nad opcją wyboru orientacji przed startem symulacji
ant_status= [0] * size #tworzy liste na której zapisane jest  na której będzie zapisane w której komórce znajduje sie mrówka
speed=500  #prędkość symulacji
square_size=350//sqrt_size #rozmiar kwadratu na siatce

def ant_simulation():   #to jest funkcja symulacji mrówki
    global ant_status, size, active, speed
    def ant_movement(i,ant_neighbors): #przesuwa mrówke do właściwego sąsiada i obraca ją
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
    def which_neighbor(i): #funkcja która sprawdza jakie sąsiedztwo ma dana komórka i wywołuje funkcję ant_movement
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
        ant_movement(i, ant_neighbors)
    
    for i in range(size):
        if ant_status[i]=="m":
            which_neighbor(i)
            break
    if active==False: #sprawdza czy symulacja jest aktywna
        return
    window.after(speed,ant_simulation) #rekurencyjne wywołanie funkcji symulacji mrówki

def click_update(btn,i):   # ta funkcja jest od przycisków na siatce
    def in_func(btn,i): #funkcja wewnętrzna która zmienia status komórki na żywą "1" lub martwą "0" w zależności od tego czy była żywa czy martwa
        global btn_status, ant_status, ant_placed
        if start_stop.cget("text")=="Place Ant": #sprawdza czy napis na przycisku start/stop jest "Place Ant" i jeśli tak to umieszcza mrówkę w komórce na którą kliknięto
            ant_status[i]="m"
            start_stop.config(text="Start")
            start_stop.config(state="normal")
        if btn_status[i]==0: #zmienia status komórki na żywą "1" jeśli była martwa "0" i na odwrót
            btn_status[i]=1
        elif btn_status[i]==1:
            btn_status[i]=0
        if btn_status[i]==1:
            btn.config(bg="black") #zmienia kolor komórki na czarny jeśli jest żywa
        if btn_status[i]==0:
            btn.config(bg="white") #zmienia kolor komórki na biały jeśli jest martwa
        if ant_status[i]=="m" and mode=="Ant": #zmienia kolor komórki na czerwony jeśli jest w niej mrówka
            btn.config(bg="red") #zmienia kolor komórki na czerwony jeśli jest w niej mrówka
    return(lambda: in_func(btn,i)) 

def gl_simulation(): #symulacja "gry w życie"
    global btn_status, btn, size, sqrt_size, active, speed
    s= size
    sqr= sqrt_size
    btn_status_copy = [0] *s
    def count_neighbors(i, neighbors): # Liczy sąsiadów zadanej komórki 
        global btn_status
        k=0
        for n in range(8):
            w=0
            w=i+neighbors[n]
            if btn_status[w]==1:
                k+=1
        return k
    for i in range(s): 
        k = 0
        if i == s-1: #poniższy kod sprawdza jakich sąsiadów posiada dana komórka
            neighbors = [-s+sqr, -s+1, 1-s+sqr, -1, -sqr-1, -sqr, -(2*sqr)+1, 1-sqr] 
        elif i == s-sqr:
            neighbors = [-s+sqr, 1-s+2*sqr, -s+1+sqr, +1, -1, 1-sqr, -sqr, sqr-1]
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

        if btn_status[i] == 0 and k == 3: #zmienia status komórki na żywą "1" jeśli była martwa "0" i ma 3 żywych sąsiadów
            btn_status_copy[i] = 1
            btn[i].config(bg="black")
        elif btn_status[i] == 1: #zmienia status komórki na martwą "0" jeśli była żywa "1" i ma mniej niż 2 lub więcej niż 3 żywych sąsiadów
            if k != 2 and k != 3:
                btn_status_copy[i] = 0
                btn[i].config(bg="white")
            else: #pozostawia komórkę żywą "1" jeśli ma 2 lub 3 żywych sąsiadów
                btn_status_copy[i] = 1
    
    btn_status.clear()
    btn_status.extend(btn_status_copy)
    if active==False: #sprawdza czy symulacja jest aktywna
        return
    window.after(speed,gl_simulation) #rekurencyjne wywołanie funkcji symulacji "gry w życie"

def change_size_fun():
    global size, sqrt_size, btn, window, grid_window, btn_status, ant_status, ant_placed, change_size_btn, square_size
    if int(size_entry.get())== sqrt_size: #sprawdza czy rozmiar siatki jest taki sam jak poprzedni
        return
    if size_entry.get().isdigit()==False: #sprawdza czy rozmiar siatki jest liczbą
        size_entry.delete(0, END) #jeśli nie to usuwa napis z pola entry
        size_entry.insert(0, "Insert number!") 
    if int(size_entry.get())<2 or int(size_entry.get())>99: #sprawdza czy rozmiar siatki mieści się w zakresie 2-99
        size_entry.delete(0, END) #jeśli nie to usuwa napis z pola entry 
        size_entry.insert(0, "Wrong size!") #jeśli nie to wstawia napis "2-99" do pola entry
        return
    size = int(size_entry.get())**2 #zmienia rozmiar siatki na podany przez użytkownika
    sqrt_size=int(size**(1/2))
    btn.clear() #niszczy poprzednią listę przycisków
    btn_status.clear() #niszczy poprzednią listę statusów przycisków
    btn_status = [0] * size #tworzy nową listę statusów przycisków
    ant_status.clear() #niszczy poprzednią listę statusów mrówki
    ant_status = [0] * size #tworzy nową listę statusów mrówki
    grid_window.destroy() #niszczy poprzednią siatkę przycisków
    grid_window = Toplevel(window)
    if mode=="Life":
        grid_window.title("Game of Life")
    elif mode=="Ant":
        grid_window.title("Langstone Ant")
    if ant_placed==True:
        ant_placed=False
    square_size=350//sqrt_size 
    for i in range(size): #tutaj tworzy sie siatka przycisków
        btn.append(Button(grid_window,image=foto,width=square_size,height=square_size))
        btn[i].grid(row=int(i//sqrt_size),column=int(i%sqrt_size),sticky="w")
        btn[i].config(bg="white", command=click_update(btn[i],i))
    
def start_stop_fun():
    global start_stop, mode, ant_placed, active, clear_grid, change_size_btn, mode_btn 
    if start_stop.cget("text")=="Start":
        active=True
        start_stop.config(text="Stop") 
        clear_grid.config(state="disabled") #blokuje przyciski aby nie można było zmienić rozmiaru siatki, czy wyczyścić siatki podczas symulacji
        change_size_btn.config(state="disabled")
        mode_btn.config(state="disabled")
        if mode=="Ant" and ant_placed==False: #sprawdza czy mrówka została umieszczona na siatce
            start_stop.config(text="Place Ant") #zmienia napis na przycisku aby zasygnalizować żeby umieścić mrówkę na siatce
            start_stop.config(state="disabled") #blokuje przycisk startu aby nie można było zmienić trybu symulacji przed umieszczeniem mrówki
            ant_placed=True #zmienia zmienną która sprawdza czy mrówka została umieszczona na siatce
        elif mode=="Ant" and ant_placed==True:
            ant_simulation()
        elif mode=="Life":
            gl_simulation()
    elif start_stop.cget("text")=="Stop":
        start_stop.config(text="Start")
        active=False #zatrzyuje działające symulacje
        clear_grid.config(state="normal") #odblokowuje przyciski
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
        grid_window.title("Game of Life")   

    elif mode_btn.cget("text")=="Game of Life Mode":
        mode = "Ant"
        mode_btn.config(text="Langstone Ant Mode")
        grid_window.title("Langstone Ant")

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

#poniżej przycisk do czyszczenia siatki
clear_grid = Button(menu_frame,text="Clear grid", font=("Arial",20), width=18, height=3, command = clear_grid_fun)
clear_grid.grid(sticky="w")

#poniżej widgety do zmmiany rozmiaru siatki
change_size = Label(menu_frame, text="Change size (2-99)", font=("Arial",20))
change_size.grid(sticky="w")
change_size_btn = Button(menu_frame, text="Change", font=("Arial",20), width=18, height=3, command = change_size_fun)
change_size_btn.grid(sticky="w")
size_entry = Entry(menu_frame,  font=("Arial",20))
size_entry.insert(0, sqrt_size)
size_entry.grid(sticky="w")

#poniżej przyciski do rozpoczęcia symulacji i zatrzyania
start_stop = Button(menu_frame, text="Start", font=("Arial",20), width=18, height=3, command = start_stop_fun)
start_stop.grid(sticky="w")

#poniżej przyciski do zmiany trybu symulacji
mode_btn = Button(menu_frame, text="Langstone Ant Mode", font=("Arial",20), width=18, height=3, command = change_mode_fun)
mode_btn.grid(sticky="w")

#poniżej przycisk do zmiany prędkości symulacji
change_speed = Button(menu_frame, text="Speed: 1", font=("Arial",20), width=18, height=3, command=change_speed_fun)
change_speed.grid(sticky="w")

#poniżej tworzenie siatki przycisków na której będzie odbywać się symulacja 
grid_window = Toplevel(window)
grid_window.title("Langstone Ant")
for i in range(size): #tutaj tworzy sie siatka przycisków
    btn.append(Button(grid_window,image=foto,width=square_size,height=square_size))
    btn[i].grid(row=int(i//sqrt_size),column=int(i%sqrt_size),sticky="w")
    btn[i].config(bg="white", command=click_update(btn[i],i))

window.mainloop()