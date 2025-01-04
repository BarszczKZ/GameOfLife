import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

def main():
    try:
        width = int(input("Podaj szerokość planszy: "))
        height = int(input("Podaj wysokość planszy: "))
        steps = int(input("Podaj liczbę iteracji: "))
    except ValueError:
        print("Wprowadź poprawne liczby całkowite.")
        return

    plansza = np.zeros((height, width))  
    x, y = width // 2, height // 2 #tu ustawiam poczatkowe polozenie czyli srodek potem sie bedzie zmieniac wraz ruchami cnie
    direction=0

    plt.figure(figsize=(8, 8))

    for i in range(steps):
        if plansza[y, x] == 0:
            direction = (direction - 1) % 4
            plansza[y, x] = 1
        else:
            direction = (direction + 1) % 4
            plansza[y, x] = 0

        if direction == 0:
            y-=1
        elif direction == 1:
            x+=1
        elif direction == 2:
            y+=1
        elif direction == 3:
            x-=1
        
        if x<0: #jezeli wyjdziemy za plansze mrowka sie pojawi na drugiej stronie
            x=width-1
        elif x>=width:
            x=0
    
        if y<0:
            y=height-1
        elif y>=height:
            y=0

        # Tutaj wyswietlanie mozecie sobie dostosowac co ile ruchow mrowek ma sie wyswietlic albo jak szybko
        if i % 10 == 0:
            plt.clf()
            plt.imshow(plansza, cmap='binary')
            plt.title(f'Langton\'s Ant after {i} steps')
            plt.axis('off')
            plt.pause(0.001)

    plt.imshow(plansza, cmap='binary')
    plt.title(f'Langton\'s Ant after {steps} steps')
    plt.show()

if __name__ == "__main__":
    main()