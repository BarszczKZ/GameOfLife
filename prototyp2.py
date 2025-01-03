from tkinter import *
import time
import sys
window = Tk()
window.geometry("710x910")
frame = Frame(window).grid(sticky="we")

files = []
btn=[]
status=[]
menu_status=0
steps=1000
orientation="n"

def simulation():
    global menu_status
    global status
    global btn
    global orientation
    global steps
    for i in range(steps):
        time.sleep(0)
        for i in range(len(files)):
            if status[i]=="m0":
                btn[i].config(bg="black")
                status[i]=1
                if orientation=="n":
                    orientation="e"
                    btn[i+1].config(bg="red")
                    if status[i+1]==0:
                        status[i+1]="m0"
                    elif status[i+1]==1:
                        status[i+1]="m1"

                elif orientation=="e":
                    orientation="s"
                    btn[i+50].config(bg="red")
                    if status[i+50]==0:
                        status[i+50]="m0"
                    elif status[i+50]==1:
                        status[i+50]="m1"

                elif orientation=="s":
                    orientation="w"
                    btn[i-1].config(bg="red")
                    if status[i-1]==0:
                        status[i-1]="m0"
                    elif status[i-1]==1:
                        status[i-1]="m1"

                elif orientation=="w":
                    orientation="n"
                    btn[i-50].config(bg="red")
                    if status[i-50]==0:
                        status[i-50]="m0"
                    elif status[i-50]==1:
                        status[i-50]="m1"
            elif status[i]=="m1":
                btn[i].config(bg="white")
                status[i]=0
                if orientation=="n":
                    orientation="w"
                    btn[i-1].config(bg="red")
                    if status[i-1]==0:
                        status[i-1]="m0"
                    elif status[i-1]==1:
                        status[i-1]="m1"

                elif orientation=="w":
                    orientation="s"
                    btn[i+50].config(bg="red")
                    if status[i+50]==0:
                        status[i+50]="m0"
                    elif status[i+50]==1:
                        status[i+50]="m1"

                elif orientation=="s":
                    orientation="e"
                    btn[i+1].config(bg="red")
                    if status[i+1]==0:
                        status[i+1]="m0"
                    elif status[i+1]==1:
                        status[i+1]="m1"

                elif orientation=="e":
                    orientation="n"
                    btn[i-50].config(bg="red")
                    if status[i-50]==0:
                        status[i-50]="m0"
                    elif status[i-50]==1:
                        status[i-50]="m1"
        window.update()       
    return

def click_update(btn,i):
    def in_func(btn,i):
        global status
        global menu_status
        if menu_status==1:
            if status[i]==1:
                status[i]="m1"
            elif status[i]==0:
                status[i]="m0"
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
        if status[i]=="m1" or status[i]=="m0":
            btn.config(bg="red")
    return(lambda: in_func(btn,i))
def menu_fun():
    global menu_status
    global btn
    global status
    if menu_status==0:
        menu_status=1
        print(menu_status)
    if menu_status==3:
        for i in range(len(files)):
            status[i]=0
            btn[i].config(state=NORMAL,bg="white")
        menu.config(text="Place Ant")
        menu_status=0
    if menu_status==2:
        for i in range(len(files)):
            btn[i].config(state=DISABLED)
        simulation()
        menu_status=3
        menu.config(text="Restart Simulation")

for i in range(2500): #to tylko do testów
    files.append("button"+str(1))
    
for i in range(len(files)):
    status.append(int(0))
    btn.append(Button(frame,font=("Arial",3),width=2,height=2))
    btn[i].grid(row=int(i//50),column=int(i%50),sticky="nesw")
    btn[i].config(bg="white", command=click_update(btn[i],i))
menu = Button(window,text="Place Ant", font=("Arial",20), width=18,height=3, command = menu_fun)
menu.place(x = 0 , y = 700)
    
window.mainloop()