#symulacje działają tak jak powinny więc nie trzeba ich zmieniać (chyba że macie pomysł jak je zoptymalizować)
#do ogarniecia na pewno jest design, i rzeczy typu stepcounter, jesli ktos z was wie jak to przepisac by dodac mozliwosc symulowania kilku mrówek to mozna tez to dodać, do poprawienia jest menu tak aby mozna bylo
#bylo wybierać między trybami symulacji, mozna tez dodac możliwosc dobrania prędkości i ilości kroków

from tkinter import *
import time
import sys
window = Tk()
window.geometry("700x910")
frame = Frame(window).grid(sticky="we")

size = 2500 #jest to rozmiar siatki, i lepiej tege nie zmieniac bo wszystko sie rozjedzie
btn=[] 
status = [0] * size  #tworzy początkowa liste statusu (każda komórka na starcie jest martwa)
menu_status=0 
orientation="n" #orientacja mrówki, można pomyslec nad opcją wyboru orientacji przed startem symulacji
a_status= [0] * size #tworzy liste statusu na której będzie zapisane w której komórce znajduje sie mrówka
steps=1000  #ilosc kroków w symulacji życia, ale da sie tez ja zrobic dla nieskonczonej ilosci kroków
def simulation():   #to jest funkcja symulacji mrówki
    global menu_status, status, a_status
    while 1>0:
        time.sleep(0.1)
        window.update()
        for i in range(size):
            if a_status[i]=="m" and status[i]==0:
                move_right(i)
                break
            elif a_status[i]=="m" and status[i]==1:
                move_left(i)
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
    global menu_status, btn, status, a_status
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
        orientation="n"
    if menu_status==2:
        for i in range(size):
            btn[i].config(state=DISABLED)
        menu.config(text="Restart Simulation")
        menu_status=3
        simulation()

def move_left(i):  #element symulacji mrówki, oddzielony od głownej funkcji dla przejrzystosci. Odpowiedzialny za ruch w lewo
    global btn, status, orientation, a_status
    btn[i].config(bg="white")
    status[i]=0
    a_status[i]=0
    if orientation=="n":
        orientation="w"
        if i%50==0:
            i+=50
        btn[i-1].config(bg="red")
        a_status[i-1]="m"
    elif orientation=="w":
        orientation="s"
        if i>=2450:
            i-=2500
        btn[i+50].config(bg="red")
        a_status[i+50]="m"
    elif orientation=="s":
        orientation="e"
        if (i+1)%50==0:
            i-=50
        btn[i+1].config(bg="red")
        a_status[i+1]="m"
    elif orientation=="e":
        orientation="n"
        if i<=49:
            i+=2500
        btn[i-50].config(bg="red")
        a_status[i-50]="m"

def move_right(i):   #element symulacji mrówki, odpowiedzialny za ruch w prawo
    global btn, orientation, status, a_status
    btn[i].config(bg="black")
    status[i]=1
    a_status[i]=0
    if orientation=="n":
        orientation="e"
        if (i+1)%50==0:
            i-=50
        btn[i+1].config(bg="red")
        a_status[i+1]="m"
    elif orientation=="e":
        orientation="s"
        if i>=2450:
            i-=2500
        btn[i+50].config(bg="red")
        a_status[i+50]="m"
    elif orientation=="s":
        orientation="w"
        if i%50==0:
            i+=50
        btn[i-1].config(bg="red")
        a_status[i-1]="m"
    elif orientation=="w":
        orientation="n"
        if i<=49:
            i+=2500
        btn[i-50].config(bg="red")
        a_status[i-50]="m"
def color_change(i):    # wsm nie wiem czy gdzies tego użylem, jesli nie to mozna wyjebac
    global btn, status
    if status[i]==0:
        btn[i].config(bg="white")
    elif status[i]==1:
        btn[i].config(bg="white")
def gl_simulation():   #symulacja gry w życie, możliwe że mozna tu jeszcze sporo zoptymalizowac ale nie mialem pomyslu jak
    global menu_status, status, btn, size, steps
    for n in range(steps):
        status_copy=[]   #tworzy nowa zmieniana kopie statusu przycisków, która potem zamienia z oryginalem
        time.sleep(0.1)
        for i in range(size):
            status_copy.append(0)
            k=0
            if i==49:     #wierzę że da sie to skrócic ale nie wiedzialem jak
                if status[i+2450]==1:
                    k+=1
                if status[i+2401]==1:
                    k+=1
                if status[i+2449]==1:
                    k+=1
                if status[i+1]==1:
                    k+=1
                if status[i-49]==1:
                    k+=1
                if status[i+50]==1:
                    k+=1
                if status[i+49]==1:
                    k+=1
                if status[i-1]==1:
                    k+=1
            elif i==0:
                if status[i+2450]==1:
                    k+=1
                if status[i+2499]==1:
                    k+=1
                if status[i+2451]==1:
                    k+=1
                if status[i+1]==1:
                    k+=1
                if status[i+99]==1:
                    k+=1
                if status[i+50]==1:
                    k+=1
                if status[i+49]==1:
                    k+=1
                if status[i+51]==1:
                    k+=1
            
            elif i==2499:
                if status[i-2450]==1:
                    k+=1
                if status[i-2499]==1:
                    k+=1
                if status[i-2451]==1:
                    k+=1
                if status[i-1]==1:
                    k+=1
                if status[i-51]==1:
                    k+=1
                if status[i-50]==1:
                    k+=1
                if status[i-99]==1:
                    k+=1
                if status[i-49]==1:
                    k+=1
            elif i==2450:
                if status[i-2450]==1:
                    k+=1
                if status[i-2401]==1:
                    k+=1
                if status[i-2449]==1:
                    k+=1
                if status[i+1]==1:
                    k+=1
                if status[i-1]==1:
                    k+=1
                if status[i-49]==1:
                    k+=1
                if status[i-50]==1:
                    k+=1
                if status[i+49]==1:
                    k+=1
            elif (i+1)%50==0 and i!=49 and i!=2499:
                if status[i-99]==1:
                    k+=1
                if status[i-49]==1:
                    k+=1
                if status[i+1]==1:
                    k+=1
                if status[i+50]==1:
                    k+=1
                if status[i+49]==1:
                    k+=1
                if status[i-51]==1:
                    k+=1
                if status[i-1]==1:
                    k+=1
                if status[i-50]==1:
                    k+=1
            elif i%50==0 and i!=0 and i!=2450:
                if status[i+99]==1:
                    k+=1
                if status[i+49]==1:
                    k+=1
                if status[i-1]==1:
                    k+=1
                if status[i-50]==1:
                    k+=1
                if status[i-49]==1:
                    k+=1
                if status[i+1]==1:
                    k+=1
                if status[i+51]==1:
                    k+=1
                if status[i+50]==1:
                    k+=1
            elif i<50 and i!=0 and i!=49:
                if status[i+1]==1:
                    k+=1
                if status[i-1]==1:
                    k+=1
                if status[i+49]==1:
                    k+=1
                if status[i+50]==1:
                    k+=1
                if status[i+51]==1:
                    k+=1
                if status[i+2451]==1:
                    k+=1
                if status[i+2449]==1:
                    k+=1
                if status[i+2450]==1:
                    k+=1
            elif i>2450 and i!=2450 and i!=2499:
                if status[i-2451]==1:
                    k+=1
                if status[i-2449]==1:
                    k+=1
                if status[i-2450]==1:
                    k+=1
                if status[i+1]==1:
                    k+=1
                if status[i-1]==1:
                    k+=1
                if status[i-50]==1:
                    k+=1
                if status[i-51]==1:
                    k+=1
                if status[i-49]==1:
                    k+=1
            elif i<2450 and i>=50 and (i+1)%50!=0 and i%50!=0:
                if status[i+1]==1:
                    k+=1
                if status[i-1]==1:
                    k+=1
                if status[i+50]==1:
                    k+=1
                if status[i-50]==1:
                    k+=1
                if status[i-51]==1:
                    k+=1
                if status[i+51]==1:
                    k+=1
                if status[i-49]==1:
                    k+=1
                if status[i+49]==1:
                    k+=1
            
            if status[i]==0:
                if k==3:
                    status_copy[i]=1
                    btn[i].config(bg="black")
            if status[i]==1:
                if k!=2 and k!=3:
                    status_copy[i]=0
                    btn[i].config(bg="white")
                else:
                    status_copy[i]=1
        status.clear()
        status.extend(status_copy)
        window.update()
    

for i in range(size): #tutaj tworzy sie siatka przycisków
    btn.append(Button(frame,font=("Arial",3),width=2,height=2))
    btn[i].grid(row=int(i//50),column=int(i%50),sticky="nesw")
    btn[i].config(bg="white", command=click_update(btn[i],i))
menu = Button(window,text="Place Ant", font=("Arial",20), width=18,height=3, command = menu_fun) #tworzy przycisk menu
menu.place(x = 0 , y = 700)
test = Button(window, text="Start", font=("Arial",20),width=5, height=3, command = gl_simulation) #ten przycisk jest tymczasowy, uruchamia symulacje gry w życie
test.place(x=350,y=700)
window.mainloop()