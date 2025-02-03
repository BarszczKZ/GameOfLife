from tkinter import *


class Simulation:
    def __init__(self):
        self.window = Tk()
        self.window.title("Project Menu")
        self.menu_frame = Frame(self.window)
        self.menu_frame.grid(sticky="w")
        self.size = 100  # jest to rozmiar siatki, na początku ustawiony na 50x50
        self.foto = PhotoImage(width=0, height=0)  # trik aby przyciski były kwadratowe
        self.mode = "Ant"  # tryb symulacji, na początku ustawiony na mrówkę
        self.ant_placed = False  # zmienna która sprawdza czy mrówka została już umieszczona na siatce
        self.active = False  # zmienna która sprawdza czy symulacja jest aktywna
        self.sqrt_size = int(self.size ** (1 / 2))  # pierwiastek z rozmiaru siatki
        self.orientation = 3  # orientacja mrówki, można pomyslec nad opcją wyboru orientacji przed startem symulacji
        self.speed = 500  # prędkość symulacji
        self.square_size = 350 // self.sqrt_size  # rozmiar kwadratu na siatce
        self.cell = [{"Button": None, "Life_Status": 0, "Ant_Status": 0} for _ in range(
            self.size)]  # lista która przechowuje statusy komórek, statusy mrówki i statusy komórek w symulacji "gry w życie"
        self.orientation = 3  # orientacja mrówki, można pomyslec nad opcją wyboru orientacji przed startem symulacji

        def ant_simulation_inner():
            self.ant_simulation()

        # poniżej przycisk do czyszczenia siatki
        self.clear_grid = Button(self.menu_frame, text="Clear grid", font=("Arial", 20), width=18, height=3,
                                 command=self.clear_grid_fun)
        self.clear_grid.grid(sticky="w")

        # poniżej widgety do zmmiany rozmiaru siatki
        self.change_size = Label(self.menu_frame, text="Change size (2-99)", font=("Arial", 20))
        self.change_size.grid(sticky="w")
        self.change_size_btn = Button(self.menu_frame, text="Change", font=("Arial", 20), width=18, height=3,
                                      command=self.change_size_fun)
        self.change_size_btn.grid(sticky="w")
        self.size_entry = Entry(self.menu_frame, font=("Arial", 20))
        self.size_entry.insert(0, self.sqrt_size)
        self.size_entry.grid(sticky="w")

        # poniżej przyciski do rozpoczęcia symulacji i zatrzyania
        self.start_stop = Button(self.menu_frame, text="Start", font=("Arial", 20), width=18, height=3,
                                 command=self.start_stop_fun)
        self.start_stop.grid(sticky="w")

        # poniżej przyciski do zmiany trybu symulacji
        self.mode_btn = Button(self.menu_frame, text="Langstone Ant Mode", font=("Arial", 20), width=18, height=3,
                               command=self.change_mode_fun)
        self.mode_btn.grid(sticky="w")

        # poniżej przycisk do zmiany prędkości symulacji
        self.change_speed = Button(self.menu_frame, text="Speed: 1", font=("Arial", 20), width=18, height=3,
                                   command=self.change_speed_fun)
        self.change_speed.grid(sticky="w")

        # poniżej tworzenie siatki przycisków na której będzie odbywać się symulacja
        self.grid_window = Toplevel(self.window)
        self.grid_window.title("Langstone Ant")
        for i in range(self.size):  # tutaj tworzy sie siatka przycisków
            self.cell[i]["Button"] = Button(self.grid_window, image=self.foto, width=self.square_size,
                                            height=self.square_size)
            self.cell[i]["Button"].grid(row=int(i // self.sqrt_size), column=int(i % self.sqrt_size), sticky="w")
            self.cell[i]["Button"].config(bg="white",
                                          command=lambda btn=self.cell[i]["Button"], idx=i: self.click_update(btn, idx))

        self.window.mainloop()

    def ant_simulation(self):  # to jest funkcja symulacji mrówki
        def ant_movement(i, ant_neighbors):  # przesuwa mrówke do właściwego sąsiada i obraca ją
            if self.cell[i]["Life_Status"] == 0:
                self.orientation = (
                                               self.orientation + 1) % 4  # orientacja koreluje z miejscem "sąsiada" na liście wiec w zaleznosci od orientacji wybierany jest odpowiedni sąsiad
                self.cell[i]["Ant_Status"] = 0
                self.cell[i + ant_neighbors[self.orientation]]["Ant_Status"] = "m"
                self.cell[i + ant_neighbors[self.orientation]]["Button"].config(bg="red")
                self.cell[i]["Button"].config(bg="black")
                self.cell[i]["Life_Status"] = 1
            elif self.cell[i]["Life_Status"] == 1:
                self.orientation -= 1
                if self.orientation < 0:
                    self.orientation = 3
                self.cell[i]["Ant_Status"] = 0
                self.cell[i + ant_neighbors[self.orientation]]["Ant_Status"] = "m"
                self.cell[i + ant_neighbors[self.orientation]]["Button"].config(bg="red")
                self.cell[i]["Button"].config(bg="white")
                self.cell[i]["Life_Status"] = 0

        def which_neighbor(
                i):  # funkcja która sprawdza jakie sąsiedztwo ma dana komórka i wywołuje funkcję ant_movement
            s = self.size
            sqr = self.sqrt_size
            if i == s - 1:  # poniższy kod sprawdza jakich sąsiadów posiada dana komórka
                ant_neighbors = [1 - sqr, -s + sqr, -1, -sqr]
            elif i == s - sqr:
                ant_neighbors = [+1, -s + sqr, sqr - 1, -sqr]
            elif i == 0:
                ant_neighbors = [+1, sqr, sqr - 1, s - sqr]
            elif i == sqr - 1:
                ant_neighbors = [1 - sqr, sqr, -1, s - sqr]
            elif (i + 1) % sqr == 0:
                ant_neighbors = [1 - sqr, sqr, -1, -sqr]
            elif i % sqr == 0:
                ant_neighbors = [+1, sqr, sqr - 1, -sqr]
            elif i < sqr:
                ant_neighbors = [+1, sqr, -1, s - sqr]
            elif i > s - sqr:
                ant_neighbors = [+1, -s + sqr, -1, -sqr]
            else:
                ant_neighbors = [+1, sqr, -1, -sqr]
            ant_movement(i, ant_neighbors)

        for i in range(self.size):
            if self.cell[i]["Ant_Status"] == "m":
                which_neighbor(i)
                break
        if self.active == False:  # sprawdza czy symulacja jest aktywna
            return
        self.window.after(self.speed, self.ant_simulation)  # rekurencyjne wywołanie funkcji symulacji mrówki

    def click_update(self, btn, i):  # ta funkcja jest od przycisków na siatce
        # funkcja wewnętrzna która zmienia status komórki na żywą "1" lub martwą "0" w zależności od tego czy była żywa czy martwa
        if self.start_stop.cget(
                "text") == "Place Ant":  # sprawdza czy napis na przycisku start/stop jest "Place Ant" i jeśli tak to umieszcza mrówkę w komórce na którą kliknięto
            self.cell[i]["Ant_Status"] = "m"
            print(self.cell[i], i)
            self.start_stop.config(text="Start")
            self.start_stop.config(state="normal")
        else:
            self.cell[i]["Life_Status"] = 1 - self.cell[i]["Life_Status"]
        if self.cell[i]["Life_Status"] == 1:
            btn.config(bg="black")  # zmienia kolor komórki na czarny jeśli jest żywa
        if self.cell[i]["Life_Status"] == 0:
            btn.config(bg="white")  # zmienia kolor komórki na biały jeśli jest martwa
        if self.cell[i][
            "Ant_Status"] == "m" and self.mode == "Ant":  # zmienia kolor komórki na czerwony jeśli jest w niej mrówka
            btn.config(bg="red")  # zmienia kolor komórki na czerwony jeśli jest w niej mrówka

    def gl_simulation(self):  # symulacja "gry w życie"
        s = self.size
        sqr = self.sqrt_size
        cell_status_copy = [0] * s

        def count_neighbors(i, neighbors):  # Liczy sąsiadów zadanej komórki
            k = 0
            for n in range(8):
                w = i + neighbors[n]
                if self.cell[w]["Life_Status"] == 1:
                    k += 1
            return k

        for i in range(s):
            k = 0
            if i == s - 1:  # poniższy kod sprawdza jakich sąsiadów posiada dana komórka
                neighbors = [-s + sqr, -s + 1, -1 - s + sqr, -1, -sqr - 1, -sqr, -(2 * sqr) + 1, 1 - sqr]
            elif i == s - sqr:
                neighbors = [-s + sqr, -1 - s + 2 * sqr, -s + 1 + sqr, +1, -1, 1 - sqr, -sqr, sqr - 1]
            elif i == 0:
                neighbors = [1 + s - sqr, s - sqr, s - 1, +1, 2 * sqr - 1, sqr, sqr - 1, sqr + 1]
            elif i == sqr - 1:
                neighbors = [s - sqr, s - 2 * sqr + 1, s - sqr - 1, +1, -1, 1 - sqr, sqr, sqr - 1]
            elif (i + 1) % sqr == 0:
                neighbors = [-(2 * sqr) + 1, 1 - sqr, +1, sqr, sqr - 1, -sqr - 1, -1, -sqr]
            elif i % sqr == 0:
                neighbors = [2 * sqr - 1, sqr - 1, -1, -sqr, 1 - sqr, +1, sqr + 1, sqr]
            elif i < sqr:
                neighbors = [+1, -1, sqr - 1, sqr, sqr + 1, 1 + s - sqr, s - sqr - 1, s - sqr]
            elif i > s - sqr:
                neighbors = [1 - s + sqr, -s - 1 + sqr, -s + sqr, +1, -1, -sqr, -sqr - 1, 1 - sqr]
            else:
                neighbors = [+1, -1, sqr, -sqr, -sqr - 1, sqr + 1, 1 - sqr, sqr - 1]

            k = count_neighbors(i, neighbors)

            if self.cell[i][
                "Life_Status"] == 0 and k == 3:  # zmienia status komórki na żywą "1" jeśli była martwa "0" i ma 3 żywych sąsiadów
                cell_status_copy[i] = 1
                self.cell[i]["Button"].config(bg="black")
            elif self.cell[i][
                "Life_Status"] == 1:  # zmienia status komórki na martwą "0" jeśli była żywa "1" i ma mniej niż 2 lub więcej niż 3 żywych sąsiadów
                if k != 2 and k != 3:
                    cell_status_copy[i] = 0
                    self.cell[i]["Button"].config(bg="white")
                else:  # pozostawia komórkę żywą "1" jeśli ma 2 lub 3 żywych sąsiadów
                    cell_status_copy[i] = 1

        for i in range(s):  # przepisuje statusy komórek z kopii
            self.cell[i]["Life_Status"] = cell_status_copy[i]
        if self.active == False:  # sprawdza czy symulacja jest aktywna
            return
        self.window.after(self.speed, self.gl_simulation)  # rekurencyjne wywołanie funkcji symulacji "gry w życie"

    def change_size_fun(self):
        global END
        if self.size_entry.get().isdigit() == False:  # sprawdza czy rozmiar siatki jest liczbą
            self.size_entry.delete(0, END)  # jeśli nie to usuwa napis z pola entry
            self.size_entry.insert(0, "Insert number!")
            return
        if int(self.size_entry.get()) == self.sqrt_size:  # sprawdza czy rozmiar siatki jest taki sam jak poprzedni
            return
        if int(self.size_entry.get()) < 2 or int(
                self.size_entry.get()) > 99:  # sprawdza czy rozmiar siatki mieści się w zakresie 2-99
            self.size_entry.delete(0, END)  # jeśli nie to usuwa napis z pola entry
            self.size_entry.insert(0, "Wrong size!")  # jeśli nie to wstawia napis "2-99" do pola entry
            return
        self.size = int(self.size_entry.get()) ** 2  # zmienia rozmiar siatki na podany przez użytkownika
        self.sqrt_size = int(self.size ** (1 / 2))
        self.cell = [{"Button": None, "Life_Status": 0, "Ant_Status": 0} for _ in range(self.size)]
        self.grid_window.destroy()  # niszczy poprzednią siatkę przycisków
        self.grid_window = Toplevel(self.window)
        if self.mode == "Life":
            self.grid_window.title("Game of Life")
        elif self.mode == "Ant":
            self.grid_window.title("Langstone Ant")
        if self.ant_placed == True:
            self.ant_placed = False
        self.square_size = 350 // self.sqrt_size
        for i in range(self.size):  # tutaj tworzy sie siatka przycisków
            self.cell[i]["Button"] = Button(self.grid_window, image=self.foto, width=self.square_size,
                                            height=self.square_size)
            self.cell[i]["Button"].grid(row=int(i // self.sqrt_size), column=int(i % self.sqrt_size), sticky="w")
            self.cell[i]["Button"].config(bg="white",
                                          command=lambda btn=self.cell[i]["Button"], idx=i: self.click_update(btn, idx))

    def start_stop_fun(self):
        global END
        if self.start_stop.cget("text") == "Start":
            self.active = True
            self.start_stop.config(text="Stop")
            self.clear_grid.config(
                state="disabled")  # blokuje przyciski aby nie można było zmienić rozmiaru siatki, czy wyczyścić siatki podczas symulacji
            self.change_size_btn.config(state="disabled")
            self.mode_btn.config(state="disabled")
            if self.mode == "Ant" and self.ant_placed == False:  # sprawdza czy mrówka została umieszczona na siatce
                self.start_stop.config(
                    text="Place Ant")  # zmienia napis na przycisku aby zasygnalizować żeby umieścić mrówkę na siatce
                self.start_stop.config(
                    state="disabled")  # blokuje przycisk startu aby nie można było zmienić trybu symulacji przed umieszczeniem mrówki
                self.ant_placed = True  # zmienia zmienną która sprawdza czy mrówka została umieszczona na siatce
            elif self.mode == "Ant" and self.ant_placed == True:
                self.ant_simulation()
            elif self.mode == "Life":
                self.gl_simulation()
        elif self.start_stop.cget("text") == "Stop":
            self.start_stop.config(text="Start")
            self.active = False  # zatrzyuje działające symulacje
            self.clear_grid.config(state="normal")  # odblokowuje przyciski
            self.change_size_btn.config(state="normal")
            self.mode_btn.config(state="normal")

    def clear_grid_fun(self):
        global END
        for i in range(self.size):
            self.cell[i]["Life_Status"] = 0
            if self.cell[i]["Ant_Status"] == "m":
                self.cell[i]["Ant_Status"] = 0
            self.cell[i]["Button"].config(bg="white")
        if self.ant_placed == True:
            self.ant_placed = False

    def change_mode_fun(self):
        if self.mode_btn.cget("text") == "Langstone Ant Mode":
            self.mode = "Life"
            self.mode_btn.config(text="Game of Life Mode")
            self.grid_window.title("Game of Life")

        elif self.mode_btn.cget("text") == "Game of Life Mode":
            self.mode = "Ant"
            self.mode_btn.config(text="Langstone Ant Mode")
            self.grid_window.title("Langstone Ant")

    def change_speed_fun(self):
        if self.change_speed.cget("text") == "Speed: 1":
            self.speed = 200
            self.change_speed.config(text="Speed: 2")
        elif self.change_speed.cget("text") == "Speed: 2":
            self.speed = 10
            self.change_speed.config(text="Speed: 3")
        elif self.change_speed.cget("text") == "Speed: 3":
            self.speed = 1
            self.change_speed.config(text="Speed: 4")
        elif self.change_speed.cget("text") == "Speed: 4":
            self.speed = 500
            self.change_speed.config(text="Speed: 1")


if __name__ == "__main__":
    Simulation()
