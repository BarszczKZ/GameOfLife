import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

class LangtonsAntApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Langton's Ant Simulation")
        self.root.geometry("400x500")
        
        self.label1=ttk.Label(root,text="Szerokość planszy:")
        self.label1.pack(pady=5)
        self.widthAdd = ttk.Entry(root)
        self.widthAdd.pack(pady=5)

        self.label2=ttk.Label(root,text="Wysokość planszy:")
        self.label2.pack(pady=5)
        self.heightAdd = ttk.Entry(root)
        self.heightAdd.pack(pady=5)

        self.label3=ttk.Label(root,text="Liczba iteracji:")
        self.label3.pack(pady=5)
        self.stepsAdd = ttk.Entry(root)
        self.stepsAdd.pack(pady=5)

        self.label3=ttk.Label(root,text="Czy chcesz zaczac od wybranego miejsca na planszy?")
        self.label3.pack(pady=5)

        self.var1 = tk.IntVar()
        self.c1 = tk.Checkbutton(root, text="Chce zaczac z wybranych wspolrzednych", variable=self.var1, onvalue=1, offvalue=0, command=self.toggle_coordinates)
        self.c1.pack(pady=10)

        self.label4 = ttk.Label(root, text="Współrzędna x:")
        self.label5 = ttk.Label(root, text="Współrzędna y:")
        self.xAdd = ttk.Entry(root)
        self.yAdd = ttk.Entry(root)
        
        self.startButton = ttk.Button(root,text="Uruchom",command=self.run_simulation)
        self.startButton.pack(pady=20)
    def toggle_coordinates(self):
        if self.var1.get()==1:
            self.label4.pack(pady=5)
            self.xAdd.pack(pady=5)
            self.label5.pack(pady=5)
            self.yAdd.pack(pady=5)
        else:
            self.label4.pack_forget()
            self.xAdd.pack_forget()
            self.label5.pack_forget()
            self.yAdd.pack_forget()

    def run_simulation(self):
        try:
            width = int(self.widthAdd.get())
            height = int(self.heightAdd.get())
            steps = int(self.stepsAdd.get())
            if self.var1.get() == 1:
                x = int(self.xAdd.get())
                y = int(self.yAdd.get())
                if x<0 or x>=width or y<0 or y>=height:
                    raise ValueError("Współrzędne poza zakresem planszy.")
            else:
                x=width//2
                y=height//2

        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawne liczby całkowite.")
            return

        plansza=np.zeros((height, width))
        direction=0
        plt.figure(figsize=(8, 8))

        for i in range(steps):
            if plansza[y,x]==0:
                direction=(direction-1)%4
                plansza[y,x]=1
            else:
                direction=(direction+1)%4
                plansza[y,x]=0

            if direction==0:
                y-=1
            elif direction==1:
                x+=1
            elif direction==2:
                y+=1
            elif direction==3:
                x-=1

            if x<0:
                x=width-1
            elif x>=width:
                x=0

            if y<0:
                y=height-1
            elif y>=height:
                y=0

            if i%10==0:
                plt.clf()
                plt.imshow(plansza, cmap='binary')
                plt.title(f'Langton\'s Ant after {i} steps')
                plt.axis('off')
                plt.pause(0.01)

        plt.imshow(plansza, cmap='binary')
        plt.title(f'Langton\'s Ant after {steps} steps')
        plt.show()

if __name__ == "__main__":
    root=tk.Tk()
    app=LangtonsAntApp(root)
    root.mainloop()
