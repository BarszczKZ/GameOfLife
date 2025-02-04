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
sqrt_size=int(size**(1/2)) #pierwiastek z rozmiaru siatkiorientation=3 #orientacja mrówki, można pomyslec nad opcją wyboru orientacji przed startem symulacji
speed=2000  #prędkość symulacji
square_size=350//sqrt_size #rozmiar kwadratu na siatce
cell = [{"Button": None, "Life_Status": 0, "Ant_Status": [0,0,0,0]} for _ in range(size)] #lista która przechowuje statusy komórek, statusy mrówki i statusy komórek w symulacji "gry w życie"
orientation=[3,3,3,3]
ant_color = {0:"grey", 1:"red", 2:"green", 3:"blue"} #słownik który przypisuje kolor mrówce w zależności od orientacji
k=0 #orientacja mrówki, można pomyslec nad opcją wyboru orientacji przed startem symulacji
ant_count=0
copy = []
def ant_simulation():   #to jest funkcja symulacji mrówki
    global size, active, speed, cell, ant_count, copy
    def ant_movement(i, j, ant_neighbors): #przesuwa mrówke do właściwego sąsiada i obraca ją
        global orientation, cell, copy
        if cell[i]["Life_Status"]==0:
            orientation[j]=(orientation[j]+1)%4#orientacja koreluje z miejscem "sąsiada" na liście wiec w zaleznosci od orientacji wybierany jest odpowiedni sąsiad
            copy.append([i,j,ant_neighbors,1, "black", orientation[j]])
        elif cell[i]["Life_Status"]==1:
            orientation[j]-=1
            if orientation[j]<0:
                orientation[j]=3
            copy.append([i,j,ant_neighbors,0, "white", orientation[j]])

    def which_neighbor(i,j): #funkcja która sprawdza jakie sąsiedztwo ma dana komórka i wywołuje funkcję ant_movement
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
        ant_movement(i, j, ant_neighbors)
    
    for i in range(size):
        for j in range(4):
            if cell[i]["Ant_Status"][j]=="m":
                ant_count+=1
                which_neighbor(i, j)
        if ant_count==4:
            ant_count=0
            break
    for j in range(4):
        cell[copy[j][0]+copy[j][2][copy[j][5]]]["Ant_Status"][copy[j][1]]="m"
        cell[copy[j][0]+copy[j][2][copy[j][5]]]["Button"].config(bg=ant_color[copy[j][1]])
        cell[copy[j][0]]["Ant_Status"][copy[j][1]]=0
        cell[copy[j][0]]["Button"].config(bg=copy[j][4])
        cell[copy[j][0]]["Life_Status"]=copy[j][3]
    copy.clear()

    if active==False: #sprawdza czy symulacja jest aktywna
        return
    window.after(speed,ant_simulation) #rekurencyjne wywołanie funkcji symulacji mrówki



def click_update(btn, i):   # ta funkcja jest od przycisków na siatce
    #funkcja wewnętrzna która zmienia status komórki na żywą "1" lub martwą "0" w zależności od tego czy była żywa czy martwa
    global ant_placed, cell, k
    if start_stop.cget("text")=="Place Ant": #sprawdza czy napis na przycisku start/stop jest "Place Ant" i jeśli tak to umieszcza mrówkę w komórce na którą kliknięto
        cell[i]["Ant_Status"][k]="m"
        print(cell[i],i)
        if k==3:
            start_stop.config(text="Start")
            start_stop.config(state="normal")
        #start_stop.config(text="Start")
        #start_stop.config(state="normal")
    else:    
        cell[i]["Life_Status"] = 1 - cell[i]["Life_Status"]
    if cell[i]["Life_Status"]==1:
        btn.config(bg="black") #zmienia kolor komórki na czarny jeśli jest żywa
    if cell[i]["Life_Status"]==0:
        btn.config(bg="white") #zmienia kolor komórki na biały jeśli jest martwa
    if cell[i]["Ant_Status"][k]=="m" and mode=="Ant": #zmienia kolor komórki na czerwony jeśli jest w niej mrówka
        btn.config(bg=ant_color[k]) #zmienia kolor komórki na czerwony jeśli jest w niej mrówka
    k=(k+1)%4


def gl_simulation(): #symulacja "gry w życie"
    global size, sqrt_size, active, speed, cell
    s= size
    sqr= sqrt_size
    cell_status_copy = [0] *s
    def count_neighbors(i, neighbors): # Liczy sąsiadów zadanej komórki 
        global btn_status,cell
        k=0
        for n in range(8):
            w=0
            w=i+neighbors[n]
            if cell[w]["Life_Status"]==1:
                k+=1
        return k
    for i in range(s): 
        k = 0
        if i == s-1: #poniższy kod sprawdza jakich sąsiadów posiada dana komórka
            neighbors = [-s+sqr, -s+1, -1-s+sqr, -1, -sqr-1, -sqr, -(2*sqr)+1, 1-sqr] 
        elif i == s-sqr:
            neighbors = [-s+sqr, -1-s+2*sqr, -s+1+sqr, +1, -1, 1-sqr, -sqr, sqr-1]
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

        if cell[i]["Life_Status"] == 0 and k == 3: #zmienia status komórki na żywą "1" jeśli była martwa "0" i ma 3 żywych sąsiadów
            cell_status_copy[i] = 1
            cell[i]["Button"].config(bg="black")
        elif cell[i]["Life_Status"] == 1: #zmienia status komórki na martwą "0" jeśli była żywa "1" i ma mniej niż 2 lub więcej niż 3 żywych sąsiadów
            if k != 2 and k != 3:
                cell_status_copy[i] = 0
                cell[i]["Button"].config(bg="white")
            else: #pozostawia komórkę żywą "1" jeśli ma 2 lub 3 żywych sąsiadów
                cell_status_copy[i] = 1
    
    for i in range(s): #przepisuje statusy komórek z kopii
        cell[i]["Life_Status"] = cell_status_copy[i]
    if active==False: #sprawdza czy symulacja jest aktywna
        return
    window.after(speed,gl_simulation) #rekurencyjne wywołanie funkcji symulacji "gry w życie"

def change_size_fun():
    global size, sqrt_size, window, grid_window, ant_placed, change_size_btn, square_size, cell
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
    cell = [{"Button": None, "Life_Status": 0, "Ant_Status": 0} for _ in range(size)]
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
        cell[i]["Button"]=Button(grid_window,image=foto,width=square_size,height=square_size)
        cell[i]["Button"].grid(row=int(i//sqrt_size),column=int(i%sqrt_size),sticky="w")
        cell[i]["Button"].config(bg="white", command= lambda btn=cell[i]["Button"], idx=i: click_update(btn,idx))
    
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
    global ant_placed, cell
    for i in range(size):
        cell[i]["Life_Status"]=0
        for j in range(4):
            if cell[i]["Ant_Status"][j]=="m":
                cell[i]["Ant_Status"][j]=0
        cell[i]["Button"].config(bg="white")
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
    cell[i]["Button"]=Button(grid_window,image=foto,width=square_size,height=square_size)
    cell[i]["Button"].grid(row=int(i//sqrt_size),column=int(i%sqrt_size),sticky="w")
    cell[i]["Button"].config(bg="white", command= lambda btn=cell[i]["Button"], idx=i: click_update(btn,idx))

window.mainloop()