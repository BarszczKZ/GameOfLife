#Na bazie prototypu7 kacpra i Gui JankaM. Zmiany w Gui, dodatkowa opcja wyboru rozmiaru gridu.
#Zostaje przy time.sleep bo after nie zapętla mi ruchu komórek w grze w życie nie wiem czemu ale nie jestem w stanie
#tego zmienić, mogłem jedynie uzależnić od ilości kliknięć w przycisk "Start" w symulaji Kacpra, ale innego efektu nie
#byłem w stanie otrzymać, zmieniłem "Start" na "Uruchom symulacje" i button działa dopiero po wybraniu symulacji, co powinno
#zapobiec problemowi który był w prototyp7, że nasza mrówka i gra w życie mogły na siebie "Nachodzić" i jednocześnie
#działać + zmiana nazewnictwa zmiennych na polskie odpowiedniki, imo lepsza czytelność.
#Nie mogę niestety uruchomić Gui przed renderem gridu, jako taki wczesny interface bo nie działa mi potem symulacja
#(Nie odpala się), więc musimy czekać na render. Dodatkowo można utworzyć kilka mrówek naraz.

from tkinter import *
import time

window = Tk()
window.title("Gra w Życie & Mrówka Langtona")
window.geometry("700x910")

# Zmienne
ramka = None  # Główna ramka dla gridu
rozmiar_gridu = 50  # Domyślny rozmiar gridu
przyciski = []
stan_komorek = []
stan_mrowki = []
typ_symulacji = None  # Typ symulacji: "mrówka" lub "gra_w_zycie"
kierunek = 3  # Kierunek mrówki (0=Góra, 1=Prawo, 2=Dół, 3=Lewo)
predkosc = 1  # Prędkość w milisekundach (dla gry w życie)


# Funkcja tworząca grid
def utworz_siatke():
    global ramka, przyciski, stan_komorek, stan_mrowki
    if ramka:  # Jeśli ramka istnieje, usuwamy
        ramka.destroy()

    ramka = Frame(window)
    ramka.pack()

    przyciski = []
    stan_komorek = [0] * (rozmiar_gridu ** 2)
    stan_mrowki = [0] * (rozmiar_gridu ** 2)

    for i in range(rozmiar_gridu ** 2):
        przyciski.append(Button(ramka, font=("Arial", 3), width=2, height=2))
        przyciski[i].grid(row=i // rozmiar_gridu, column=i % rozmiar_gridu)
        przyciski[i].config(bg="white", command=kliknij_aktualizuj(przyciski[i], i))


# Funkcja aktualizująca kliknięcia na gridzie
def kliknij_aktualizuj(przycisk, i):
    def funkcja_w_przyciski(przycisk, i):
        global stan_komorek, stan_mrowki, typ_symulacji
        if typ_symulacji == "mrowka":  # Ustawienie mrówki
            stan_mrowki[i] = "m"
            przycisk.config(bg="red")
        else:  # Ustawienie stanu komórki dla gry w życie
            stan_komorek[i] = 1 if stan_komorek[i] == 0 else 0
            przycisk.config(bg="black" if stan_komorek[i] == 1 else "white")
    return lambda: funkcja_w_przyciski(przycisk, i)


# Funkcja symulacji mrówki
def symulacja_mrowki():
    global stan_mrowki
    while True:
        time.sleep(predkosc / 1000)  #Płynna i szybka symulacja
        window.update()
        for i in range(len(stan_mrowki)):
            if stan_mrowki[i] == "m":
                ruch_mrowki(i)
                break


# Funkcja symulacji gry w życie
def symulacja_gra_w_zycie():
    global stan_komorek
    przesuniecia_sasiadow = [-rozmiar_gridu - 1, -rozmiar_gridu, -rozmiar_gridu + 1,
                             -1, 1, rozmiar_gridu - 1, rozmiar_gridu, rozmiar_gridu + 1]

    while True:
        stan_komorek_kopia = stan_komorek.copy()  # Kopiowanie stanu gridu
        for i in range(rozmiar_gridu ** 2):
            wiersz, kolumna = divmod(i, rozmiar_gridu)

            # Sąsiedzi w granicach gridu
            sasiedzi = [
                (wiersz + dwiersz) * rozmiar_gridu + (kolumna + dkolumna)
                for dwiersz, dkolumna in [(-1, -1), (-1, 0), (-1, 1),
                                          (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                if 0 <= wiersz + dwiersz < rozmiar_gridu and 0 <= kolumna + dkolumna < rozmiar_gridu
            ]

            # Liczenie żywych sąsiadów
            zywi_sasiedzi = sum(stan_komorek[s] for s in sasiedzi)

            # Zasady gry w życie
            if stan_komorek[i] == 0 and zywi_sasiedzi == 3:
                stan_komorek_kopia[i] = 1
            elif stan_komorek[i] == 1 and zywi_sasiedzi not in (2, 3):
                stan_komorek_kopia[i] = 0

        # Aktualizacja stanu przycisków
        for i in range(rozmiar_gridu ** 2):
            if stan_komorek[i] != stan_komorek_kopia[i]:
                stan_komorek[i] = stan_komorek_kopia[i]
                przyciski[i].config(bg="black" if stan_komorek[i] == 1 else "white")

        window.update()
        time.sleep(predkosc / 1000)  # Żeby symulacja była płynna/szybka tak samo jak w mrówce


# Funkcja do wyboru symulacji
def uruchom_symulacje():
    if typ_symulacji == "mrowka":
        symulacja_mrowki()
    elif typ_symulacji == "gra_w_zycie":
        symulacja_gra_w_zycie()


# Funkcja ruchu mrówki
def ruch_mrowki(i):
    global kierunek, stan_komorek, stan_mrowki, przyciski
    sasiedzi_mrowki = pobierz_sasiadow_mrowki(i)
    if stan_komorek[i] == 0:
        kierunek = (kierunek + 1) % 4
        stan_mrowki[i] = 0
        stan_mrowki[i + sasiedzi_mrowki[kierunek]] = "m"
        przyciski[i + sasiedzi_mrowki[kierunek]].config(bg="red")
        przyciski[i].config(bg="black")
        stan_komorek[i] = 1
    elif stan_komorek[i] == 1:
        kierunek -= 1
        if kierunek < 0:
            kierunek = 3
        stan_mrowki[i] = 0
        stan_mrowki[i + sasiedzi_mrowki[kierunek]] = "m"
        przyciski[i + sasiedzi_mrowki[kierunek]].config(bg="red")
        przyciski[i].config(bg="white")
        stan_komorek[i] = 0


# Funkcja do uzyskiwania sąsiadów mrówki
def pobierz_sasiadow_mrowki(i):
    if i == (rozmiar_gridu ** 2) - 1:
        return [-rozmiar_gridu, -rozmiar_gridu * (rozmiar_gridu - 1), -1, -rozmiar_gridu]
    elif i == rozmiar_gridu * (rozmiar_gridu - 1):
        return [+1, -rozmiar_gridu * (rozmiar_gridu - 1), +rozmiar_gridu - 1, -rozmiar_gridu]
    elif i == 0:
        return [+1, +rozmiar_gridu, +rozmiar_gridu - 1, +rozmiar_gridu * (rozmiar_gridu - 1)]
    elif i == rozmiar_gridu - 1:
        return [-rozmiar_gridu, +rozmiar_gridu, -1, +rozmiar_gridu * (rozmiar_gridu - 1)]
    elif (i + 1) % rozmiar_gridu == 0:
        return [-rozmiar_gridu, +rozmiar_gridu, -1, -rozmiar_gridu]
    elif i % rozmiar_gridu == 0:
        return [+1, +rozmiar_gridu, +rozmiar_gridu - 1, -rozmiar_gridu]
    elif i < rozmiar_gridu:
        return [+1, +rozmiar_gridu, -1, +rozmiar_gridu * (rozmiar_gridu - 1)]
    elif i >= rozmiar_gridu * (rozmiar_gridu - 1):
        return [+1, -rozmiar_gridu * (rozmiar_gridu - 1), -1, -rozmiar_gridu]
    else:
        return [+1, +rozmiar_gridu, -1, -rozmiar_gridu]


# Funkcja konfiguracji symulacji
def konfiguruj_symulacje(typ):
    global rozmiar_gridu, typ_symulacji
    typ_symulacji = typ
    rozmiar_gridu = int(pole_rozmiar.get())
    utworz_siatke()


# Gui
Label(window, text="Rozmiar siatki (10-99):").pack()
pole_rozmiar = Entry(window, width=10)
pole_rozmiar.insert(0, "50")
pole_rozmiar.pack()

Button(window, text="Mrówka Langtona", command=lambda: konfiguruj_symulacje("mrowka")).pack()
Button(window, text="Gra w Życie", command=lambda: konfiguruj_symulacje("gra_w_zycie")).pack()

przycisk_start = Button(window, text="Uruchom Symulację", command=uruchom_symulacje)
przycisk_start.pack()

# Uruchomienie naszej symulacji
utworz_siatke()
window.mainloop()
