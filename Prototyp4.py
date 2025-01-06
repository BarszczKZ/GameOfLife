from tkinter import *
import time
import sys
window = Tk()
window.geometry("700x910")
frame = Frame(window).grid(sticky="we")

size = 2500
btn=[]
status = [0] * size
menu_status=0
x=[]
y=[]
orientation="n"
a_status= [0] * size

def simulation():
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

def click_update(btn,i):
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

def menu_fun():
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

def move_left(i):
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

def move_right(i):
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

for i in range(size):
    btn.append(Button(frame,font=("Arial",3),width=2,height=2))
    btn[i].grid(row=int(i//50),column=int(i%50),sticky="nesw")
    btn[i].config(bg="white", command=click_update(btn[i],i))
menu = Button(window,text="Place Ant", font=("Arial",20), width=18,height=3, command = menu_fun)
menu.place(x = 0 , y = 700)
    
window.mainloop()
