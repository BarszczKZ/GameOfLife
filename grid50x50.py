from tkinter import *
window = Tk()
frame = Frame(window).grid()
files = []
btn=[]
status=[]
def btn_color(status):
    if status==0:
        return("black")
    if status==1:
        return("white")
def click_update(status,btn):
    status=abs(status-1)
    if status==0:
        btn.config(bg="black")
    if status==1:
        btn.config(bg="white")

for i in range(2500):
    files.append("button"+str(1))
for i in range(len(files)):
    status.append(int(0))
    btn.append(Button(frame,text="k", font=("Arial",3),width=2,height=2))
    btn[i].grid(row=int((i)//50),column=int((i-((i//50))*50)),sticky="we")
for i in range(len(files)):
     btn[i].config(bg=btn_color(status[i]), command=lambda: click_update(status[i],btn[i]))
window.mainloop()