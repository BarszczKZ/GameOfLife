from tkinter import *
window = Tk()
frame = Frame(window).grid()

files = []
btn=[]
status=[]

def click_update(btn,i):
    def in_func(btn,i):
        global status
        if status[i]==0:
            status[i]=1
        elif status[i]==1:
            status[i]=0
        if status[i]==1:
            btn.config(bg="black")
        if status[i]==0:
            btn.config(bg="white")
    return(lambda: in_func(btn,i))
    
for i in range(2500): #to tylko do testów
    files.append("button"+str(1))
    
for i in range(len(files)):
    status.append(int(0))
    btn.append(Button(frame,font=("Arial",3),width=2,height=2))
    btn[i].grid(row=int(i//50),column=int(i%50),sticky="we")
    btn[i].config(bg="white", command=click_update(btn[i],i))
    
window.mainloop()