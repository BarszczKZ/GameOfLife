from tkinter import *
window = Tk()
frame = Frame(window).grid()
files = []
btn=[]
for i in range(2500):
    files.append("button"+str(1))
for i in range(len(files)):
    btn.append(Button(frame,text="k", font=("Arial",3),width=2,height=2).grid(row=int((i)//50),column=int((i-((i//50))*50)),sticky="w"))


window.mainloop()