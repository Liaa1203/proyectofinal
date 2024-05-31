import tkinter as tk
from tkinter import simpledialog, messagebox
from os import path
from random import shuffle

class Jugador:
    def __init__(self):
        self.nombre = ""
        self.credito = 0
        self.mano = []

class Baraja:
    palos = ["♠", "♡", "♢", "♣"]
    letras = ["A", "J", "Q", "K"]

    def __init__(self):
        self.cartas = []
        self.crearBaraja()
        self.barajear()
        

    def crearBaraja(self):
        for p in self.palos:
            for i in range(2, 11):
                self.cartas.append(f"{i}{p}")
            for i in self.letras:
                self.cartas.append(f"{i}{p}")

    def barajear(self):
        shuffle(self.cartas)

    def pedirCarta(self):
        if self.cartas:
            return self.cartas.pop()
        else:
            return None

class MenuPrincipal:
    def __init__(self, window):
        self.window = window 
        self.jugador = Jugador()
        self.window.configure(bg='#2b081b') 
        self.baraja = Baraja()

        # self.background_image = tk.PhotoImage(file="C:\Users\natal\OneDrive\Escritorio\cosodepoo\casino.jpeg")
        
       
        # self.background_label = tk.Label(self.window, image=self.background_image)
        # self.background_label.place(relwidth=1, relheight=1)
        

        self.frame = tk.Frame(self.window)
        self.frame.pack(expand=True)

        self.label = tk.Label(self.frame, text="♠  ♥ BLACKJACK NIGHT ♦  ♣", font=("Helvetica", 30), bg='#2b081b', fg='white', borderwidth=0)
        self.label.pack(pady=20)
        
        self.boton_nueva_partida = tk.Button(self.frame, text="Nueva Partida", command=self.mostrarFormularioNuevaPartida,
                                             font=("Helvetica", 14), width=20, height=2, bg="#7e4029", fg="white")
        self.boton_nueva_partida.pack(pady=10)
        
        self.boton_continuar_partida = tk.Button(self.frame, text="Continuar Partida", command=self.continuarPartida,
                                                 font=("Helvetica", 14), width=20, height=2, bg="#7e4029", fg="white")
        self.boton_continuar_partida.pack(pady=10)

        self.boton_cargar_partida = tk.Button(self.frame, text="Cargar Partida", command=self.cargarPartida,
                                              font=("Helvetica", 14), width=20, height=2, bg="#7e4029", fg="white")
        self.boton_cargar_partida.pack(pady=10)


    def nuevaPartida(self):
        self.jugador.nombre = simpledialog.askstring("Input", "Ingrese su nombre:")
        fichas = simpledialog.askinteger("Input", "Ingrese su número de fichas:", minvalue=1, maxvalue=100000)
        if fichas is not None:
            self.jugador.credito = fichas
            self.guardarPartida()
            self.mostrarMenuNivel()
            
    def mostrarFormularioNuevaPartida(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.frame = tk.Frame(self.window)
        self.frame.pack(expand=True)

        self.label_nombre = tk.Label(self.frame, text="Nombre:", font=("Helvetica", 14))
        self.label_nombre.pack(pady=5)

        self.entry_nombre = tk.Entry(self.frame, font=("Helvetica", 14))
        self.entry_nombre.pack(pady=5)

        self.label_fichas = tk.Label(self.frame, text="Fichas:", font=("Helvetica", 14))
        self.label_fichas.pack(pady=5)

        self.entry_fichas = tk.Entry(self.frame, font=("Helvetica", 14))
        self.entry_fichas.pack(pady=5)

        self.boton_guardar = tk.Button(self.frame, text="Guardar", command=self.guardarJugador,
                                       font=("Helvetica", 14), width=20, height=2, bg="#7e4029", fg="white")
        self.boton_guardar.pack(pady=10)

    def guardarJugador(self):
        self.jugador.nombre = self.entry_nombre.get()
        fichas = self.entry_fichas.get()
        if fichas.isdigit():
            self.jugador.credito = int(fichas)
            self.guardarPartida()
            self.mostrarMenuPrincipal()
        else:
            messagebox.showerror("Error", "El número de fichas debe ser un número entero.")

    def mostrarMenuPrincipal(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        MenuPrincipal(self.window)


    def continuarPartida(self):
        self.guardarPartida()  # Guardar la partida antes de continuar
        self.mostrarMenuNivel()

    def cargarPartida(self):
        ruta = "partida.txt"
        if path.exists(ruta):
            with open(ruta, "r") as file:
                lines = file.readlines()
                if lines:
                    datos = [line.strip() for line in lines]
                    if len(datos) == 2:
                        nombre, credito = datos
                        self.jugador.nombre = nombre
                        self.jugador.credito = int(credito)
                        messagebox.showinfo("Cargar Partida", "Cuenta iniciada con éxito")
                        self.mostrarMenuNivel()
                    else:
                        messagebox.showerror("Error", "El archivo de partida está corrupto.")
                else:
                    messagebox.showerror("Error", "El archivo de partida está vacío.")
        else:
            messagebox.showerror("Error", "No se encontró el archivo de partida.")

    def guardarPartida(self):
        ruta = "partida.txt"
        with open(ruta, "w") as file:
            datos = [f"{self.jugador.nombre}", f"{int(self.jugador.credito)}"]
            file.write("\n".join(datos))

    def mostrarMenuNivel(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        SeleccionarNivel(self.window, self.jugador, self.baraja)

class SeleccionarNivel:
    def __init__(self, window, jugador, baraja):
        self.window = window
        self.jugador = jugador
        self.baraja = baraja
        self.window.title("Niveles")

        self.fichas = {
            "Fácil": [10, 20, 50, 70, 200],
            "Medio": [200, 230, 260, 350, 550],
            "Difícil": [550, 750, 1000, 1250, 1500]
        }

        self.frame = tk.Frame(self.window)
        self.frame.pack(expand=True)

        self.label = tk.Label(self.frame, text="Selecciona un nivel", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.boton_nivel_facil = tk.Button(self.frame, text="Fácil", command=lambda: self.iniciarJuego("Fácil"), font=("Helvetica", 14),
                                           width=20, height=2, bg="#7e4029", fg="white")
        self.boton_nivel_facil.pack(pady=10, anchor='center')

        self.boton_nivel_medio = tk.Button(self.frame, text="Medio", command=lambda: self.iniciarJuego("Medio"), font=("Helvetica", 14),
                                           width=20, height=2, bg="#7e4029", fg="white")
        self.boton_nivel_medio.pack(pady=10, anchor='center')

        self.boton_nivel_dificil = tk.Button(self.frame, text="Difícil", command=lambda: self.iniciarJuego("Difícil"), font=("Helvetica", 14),
                                             width=20, height=2, bg="#7e4029", fg="white")
        self.boton_nivel_dificil.pack(pady=10, anchor='center')

    def iniciarJuego(self, nivel):
        JuegoBlackjack(self.window, self.jugador, self.baraja, nivel, self.fichas[nivel])


class JuegoBlackjack:
    def __init__(self, window, jugador, baraja, nivel, fichas):
        self.window = window
        self.jugador = jugador
        self.baraja = baraja
        self.nivel = nivel
        self.jugador.mano = []
        self.dealer_mano = []
        self.apuesta = 0
        self.fichas = fichas

        self.iniciarJuego()

    
    def iniciarJuego(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.label_nombre = tk.Label(self.window, text=f"Jugador: {self.jugador.nombre}", font=("Helvetica", 14))
        self.label_nombre.pack(pady=5)

        self.label_credito = tk.Label(self.window, text=f"Crédito: {self.jugador.credito}", font=("Helvetica", 14))
        self.label_credito.pack(pady=5)

        self.label_apuesta = tk.Label(self.window, text="Seleccione su apuesta:", font=("Helvetica", 14))
        self.label_apuesta.pack(pady=5)

        for ficha in self.fichas:  # Usar los valores de las fichas para el nivel seleccionado
            boton = tk.Button(self.window, text=str(ficha), command=lambda ficha=ficha: self.apostar(ficha), font=("Helvetica", 14), width=7, height=3)
            boton.pack(pady=5)
            

    def apostar(self, ficha):
        if ficha <= self.jugador.credito:
            self.apuesta = ficha
            self.jugador.credito -= ficha
            self.repartirCartas()
        else:
            respuesta = messagebox.askquestion("Sin céditos", "Te has quedado sin créditos. ¿Quieres añadir más?")
            if respuesta == "yes":
                self.añadirCreditos()
            else:
                self.nivelInfierno()

    def añadirCreditos(self):
        creditos = simpledialog.askinteger("Input", "Ingrese la cantidad de créditos que desea añadir:", minvalue=1, maxvalue=100000)
        if creditos is not None:
            self.jugador.credito += creditos
            self.guardarPartida()
            self.iniciarJuego()

    def nivelInfierno(self):
        self.finalizarJuego("Has entrado al nivel Infierno. Buena suerte.")
        NivelInfierno(self.window, self.jugador, self.baraja)


    def repartirCartas(self):
        self.jugador.mano.append(self.baraja.pedirCarta())
        self.jugador.mano.append(self.baraja.pedirCarta())
        self.dealer_mano.append(self.baraja.pedirCarta())
        self.dealer_mano.append(self.baraja.pedirCarta())
        self.actualizarInterfaz()

    def actualizarInterfaz(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.label_nombre = tk.Label(self.window, text=f"Jugador: {self.jugador.nombre}", font=("Helvetica", 14))
        self.label_nombre.pack(pady=5)

        self.label_credito = tk.Label(self.window, text=f"Crédito: {self.jugador.credito}", font=("Helvetica", 14))
        self.label_credito.pack(pady=5)

        self.label_apuesta = tk.Label(self.window, text=f"Apuesta: {self.apuesta}", font=("Helvetica", 14))
        self.label_apuesta.pack(pady=5)

        self.label_mano_jugador = tk.Label(self.window, text=f"Mano del Jugador: {', '.join(self.jugador.mano)}", font=("Helvetica", 14))
        self.label_mano_jugador.pack(pady=5)

        self.label_mano_dealer = tk.Label(self.window, text=f"Mano del Dealer: {self.dealer_mano[0]}, ?", font=("Helvetica", 14))
        self.label_mano_dealer.pack(pady=5)

        self.boton_pedir = tk.Button(self.window, text="Pedir Carta", command=self.pedirCarta, font=("Helvetica", 14), width=15, height=2)
        self.boton_pedir.pack(pady=5)

        self.boton_plantarse = tk.Button(self.window, text="Plantarse", command=self.plantarse, font=("Helvetica", 14), width=15, height=2)
        self.boton_plantarse.pack(pady=5)

        self.chequearEstado()

    def pedirCarta(self):
        self.jugador.mano.append(self.baraja.pedirCarta())
        self.chequearEstado()
        self.actualizarInterfaz()

    def plantarse(self):
        while self.calcularPuntos(self.dealer_mano) < 17:
            self.dealer_mano.append(self.baraja.pedirCarta())
        self.determinarGanador()

    def chequearEstado(self):
        puntos_jugador = self.calcularPuntos(self.jugador.mano)
        if puntos_jugador == 21:
            self.jugador.credito += self.apuesta * 2
            self.finalizarJuego("Jugador gana con 21 puntos")
        elif puntos_jugador > 21:
            self.finalizarJuego("Jugador se pasa, Dealer gana")

    def calcularPuntos(self, mano):
        valores = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        puntos = sum(valores[carta[:-1]] for carta in mano)
        ases = sum(1 for carta in mano if carta[:-1] == 'A')
        while puntos > 21 and ases:
            puntos -= 10
            ases -= 1
        return puntos

    def determinarGanador(self):
        puntos_jugador = self.calcularPuntos(self.jugador.mano)
        puntos_dealer = self.calcularPuntos(self.dealer_mano)

        if puntos_dealer > 21 or puntos_jugador > puntos_dealer:
            self.jugador.credito += self.apuesta * 2
            self.finalizarJuego("Jugador gana")
        elif puntos_jugador == puntos_dealer:
            self.jugador.credito += self.apuesta
            self.finalizarJuego("Empate")
        else:
            self.finalizarJuego("Dealer gana")

    def finalizarJuego(self, mensaje):
        messagebox.showinfo("Resultado", mensaje)
        self.guardarPartida()
        self.regresarMenuNivel()

    def guardarPartida(self):
        ruta = "partida.txt"
        with open(ruta, "w") as file:
            datos = [f"{self.jugador.nombre}", f"{int(self.jugador.credito)}"]
            file.write("\n".join(datos))

    def regresarMenuNivel(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        SeleccionarNivel(self.window, self.jugador, self.baraja)

class NivelInfierno(JuegoBlackjack):
    def __init__(self, window, jugador, baraja):
        super().__init__(window, jugador, baraja, "Infierno", [100])  # Se dan 100 fichas en el nivel Infierno

    def iniciarJuego(self):
        super().iniciarJuego()
        self.jugador.credito = 100  # Se dan 100 fichas en el nivel Infierno

    def determinarGanador(self):
        messagebox.showinfo("Nivel Infierno", "La casa siempre gana :)")
        self.borrarCuenta()
        self.regresarMenuPrincipal()

    def borrarCuenta(self):
        ruta = "partida.txt"
        with open(ruta, "w") as file:
            datos = ["", "0"]
            file.write("\n".join(datos))

    def regresarMenuPrincipal(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        MenuPrincipal(self.window)




window = tk.Tk()
window.geometry("1400x800")
menu = MenuPrincipal(window)
window.mainloop()
