import tkinter as tk
from tkinter import *
from tkinter import filedialog, colorchooser  # Importa colorchooser para la paleta de colores
from PIL import ImageGrab
from Tooltip import Tooltip
from tkinter import simpledialog

class Paint:  # Define la clase Paint
    
    def __init__(self):  # Define el método constructor de la clase Paint
    
        self.ventana = tk.Tk()  # Crea una ventana tkinter
        self.ventana.title("Paint")  # Establece el título de la ventana como "Paint"
        self.ventana.geometry("1100x660")  # Establece el tamaño de la ventana
        self.ventana.config(bg="AntiqueWhite1")  # Establece el color de fondo de la ventana
        self.ventana.resizable(0,0)  # Hace que la ventana no sea redimensionable
        self.modo_dibujo = False
        self.color = "black"  # Variable para almacenar el color seleccionado
        self.poligono_puntos = []  # Lista para almacenar los puntos del polígono
        self.elementos_dibujados = []  # Lista para almacenar los elementos dibujados
        self.undo_stack = []  # Pila para realizar el deshacer

        self.canvas = tk.Canvas(self.ventana, width=945, height=520, bg="white")  # Crea un lienzo en la ventana
        self.canvas.place(x=140, y=40)  # Coloca el lienzo en la ventana

        # Crea líneas en el lienzo para delimitar el área de dibujo

        canvas_colores = Canvas(self.ventana, bg='black', width=500,  height=40)
        canvas_colores.place(x=30, y=575)

        colores = [
            ('red', 10), ('green', 40), ('yellow', 70), ('magenta', 100), 
            ('blue', 130), ('orange', 160), ('salmon', 190), ('sky blue', 220),
            ('gold', 250), ('hot pink', 280), ('bisque', 310), ('brown4', 340),
            ('gray', 370), ('purple', 400), ('green2', 430), ('dodger blue', 460),
            ('black', 490)
        ]

        for color, x in colores:
            id = canvas_colores.create_rectangle((x, 10, x + 20, 30), fill=color)
            canvas_colores.tag_bind(id, '<Button-1>', lambda event, col=color: self.mostrar_color(col))

        # Botón para la paleta de colores
        self.btnPaleta = tk.Button(self.ventana, text="Paleta de Colores", command=self.abrir_paleta_colores, background="gold")  # Crea el botón para abrir la paleta de colores
        self.btnPaleta.place(x=900, y=580)  # Coloca el botón en la ventana
        Tooltip(self.btnPaleta, "Abrir paleta de colores")  # Añade un tooltip al botón de la paleta de colores

        # Carga las imágenes de los iconos de las herramientas de dibujo
        self.lapiz = tk.PhotoImage(file=r"Imagenes\pincel1.png")
        self.linea = tk.PhotoImage(file=r"Imagenes\linea1.png")
        self.rectangulo = tk.PhotoImage(file=r"Imagenes\rectangulo 12.png")
        self.poligono = tk.PhotoImage(file=r"Imagenes\poligono1.png")
        self.ovalo = tk.PhotoImage(file=r"Imagenes\Ovalo1.png")
        self.texto = tk.PhotoImage(file=r"Imagenes\c.png")
        self.Guardar = tk.PhotoImage(file=r"icons\application_get.png")
        self.Deshacer = tk.PhotoImage(file=r"icons\arrow_rotate_anticlockwise.png")
        self.lapiz1 = tk.PhotoImage(file=r"Imagenes\lapiz.png")
        self.tarrobasura = tk.PhotoImage(file=r"Imagenes/Sin título.png")

        # Crea los botones de las herramientas de dibujo y los coloca en la ventana
        self.btnLapiz = tk.Button(self.ventana, image=self.lapiz, border=0, background="AntiqueWhite1", command=self.activar_lapiz)
        self.btnLapiz.place(x=20, y=80, width=40, height=40)
        Tooltip(self.btnLapiz, "Lapiz")

        self.btnLinea = tk.Button(self.ventana, image=self.linea, border=0, background="AntiqueWhite1", command=self.activar_linea)  # Botón para activar la herramienta de línea
        self.btnLinea.place(x=80, y=80, width=40, height=40)
        Tooltip(self.btnLinea, "Linea")

        self.btnRectangulo = tk.Button(self.ventana, image=self.rectangulo, border=0, background="AntiqueWhite1", command=self.activar_rectangulo)  # Botón para activar la herramienta de rectángulo
        self.btnRectangulo.place(x=20, y=150, width=40, height=40)
        Tooltip(self.btnRectangulo, "Rectangulo")

        self.btnPoligono = tk.Button(self.ventana, image=self.poligono, border=0, background="AntiqueWhite1", command=self.activar_poligono)  # Agrega el comando para activar el polígono
        self.btnPoligono.place(x=80, y=150, width=40, height=40)
        Tooltip(self.btnPoligono, "Poligono")

        self.btnOvalo = tk.Button(self.ventana, image=self.ovalo, border=0, background="AntiqueWhite1", command=self.activar_ovalo)  # Botón para activar la herramienta de óvalo
        self.btnOvalo.place(x=20, y=220, width=40, height=40)
        Tooltip(self.btnOvalo, "Ovalo")


        self.btnTexto = tk.Button(self.ventana, image=self.texto, border=0, background="AntiqueWhite1", command=self.activar_texto)
        self.btnTexto.place(x=83, y=223)
        Tooltip(self.btnTexto, "Texto")

        self.btnDibujo = tk.Button(self.ventana, background="AntiqueWhite1", image=self.lapiz1, border=0, command=self.activar_lapiz)
        self.btnDibujo.place(x=55, y=300)
        Tooltip(self.btnDibujo, "Presione para Dibujar")

        # Crea el botón de guardar y lo coloca en la ventana
        self.save_button = tk.Button(self.ventana, image=self.Guardar, border=0, background="AntiqueWhite1", text="Guardar", command=self.guardar)
        self.save_button.place(x=15, y=4, width=35, height=35)

        # Crea el botón de deshacer y lo coloca en la ventana
        self.btnDevolver = tk.Button(self.ventana, image=self.Deshacer, border=0, background="AntiqueWhite1", command=self.deshacer)
        self.btnDevolver.place(x=45, y=4, width=35, height=35)
        Tooltip(self.btnDevolver, "Deshacer")

        self.btnEliminar = tk.Button(self.ventana, image=self.tarrobasura, border=0, background="AntiqueWhite1", command=self.limpiar)
        self.btnEliminar.place(x=15, y=510)
        Tooltip(self.btnEliminar, "Borrar toto el contenido del lienzo")

        self.espesor_pincel = Scale(self.ventana, orient=HORIZONTAL, from_=1, to=50, length=200, relief='groove', bg='yellow', width=17, sliderlength=20, highlightbackground='white', activebackground='red')
        self.espesor_pincel.set(1)
        self.espesor_pincel.place(x=600, y=575)  

        # Crea separadores en la ventana
        separadorsuperior = tk.Frame(self.ventana, width=5, bg="black")
        separadorsuperior.place(x=0, y=42, width=1100, height=2)

        separadorinferior = tk.Frame(self.ventana, width=5, bg="black")
        separadorinferior.place(x=0, y=560, width=1100, height=2)

        # Vincula los eventos de movimiento del ratón a las funciones de pintar y guardar
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<B2-Motion>", self.guardar)
        
        self.ventana.mainloop()  # Inicia el bucle principal de la ventana

    def mostrar_color(self, nuevo_color):
        self.color = nuevo_color  # Método para actualizar el color

    def abrir_paleta_colores(self):
        color_seleccionado = colorchooser.askcolor(title="Seleccionar color")  # Abre el diálogo de la paleta de colores
        if color_seleccionado[1] is not None:
            self.color = color_seleccionado[1]  # Actualiza el color seleccionado

    def limpiar(self):
        self.canvas.delete(ALL)

    def linea_xy(self, event):
        self.linea_x = event.x
        self.linea_y = event.y
    
    def activar_lapiz(self):
        self.desactivar_lapiz()  # Desactiva cualquier otra herramienta
        self.current_tool = "paint"  # Establece la herramienta actual como lápiz
        self.canvas.config(cursor="pencil")  # Cambia el cursor a un lápiz
        self.canvas.bind('<Button-1>', self.linea_xy)  # Vincula el evento de clic izquierdo a la función linea_xy
        self.canvas.bind('<B1-Motion>', self.paint)  # Vincula el evento de arrastre del ratón a la función paint

    def activar_linea(self):
        self.desactivar_lapiz()  # Desactiva cualquier otra herramienta
        self.current_tool = "line"  # Establece la herramienta actual como línea
        self.canvas.config(cursor="cross")  # Cambia el cursor a una cruz
        self.canvas.bind('<Button-1>', self.linea_xy)  # Vincula el evento de clic izquierdo a la función linea_xy
        self.canvas.bind('<ButtonRelease-1>', self.dibujar_linea)  # Vincula el evento de soltar clic izquierdo a la función dibujar_linea

    def activar_rectangulo(self):
        self.desactivar_lapiz()  # Desactiva cualquier otra herramienta
        self.current_tool = "rectangle"  # Establece la herramienta actual como rectángulo
        self.canvas.config(cursor="cross")  # Cambia el cursor a una cruz
        self.canvas.bind('<Button-1>', self.linea_xy)  # Vincula el evento de clic izquierdo a la función linea_xy
        self.canvas.bind('<ButtonRelease-1>', self.dibujar_rectangulo)  # Vincula el evento de soltar clic izquierdo a la función dibujar_rectangulo

    def activar_ovalo(self):
        self.desactivar_lapiz()  # Desactiva cualquier otra herramienta
        self.current_tool = "oval"  # Establece la herramienta actual como óvalo
        self.canvas.config(cursor="cross")  # Cambia el cursor a una cruz
        self.canvas.bind('<Button-1>', self.linea_xy)  # Vincula el evento de clic izquierdo a la función linea_xy
        self.canvas.bind('<ButtonRelease-1>', self.dibujar_ovalo)  # Vincula el evento de soltar clic izquierdo a la función dibujar_ovalo

    def activar_poligono(self):
        self.desactivar_lapiz()  # Desactiva cualquier otra herramienta
        self.current_tool = "polygon"  # Establece la herramienta actual como polígono
        self.canvas.config(cursor="cross")  # Cambia el cursor a una cruz
        self.canvas.bind('<Button-1>', self.agregar_punto_poligono)  # Vincula el evento de clic izquierdo a la función agregar_punto_poligono
        self.canvas.bind('<Button-3>', self.cerrar_poligono)  # Vincula el evento de clic derecho a la función cerrar_poligono

    def agregar_punto_poligono(self, event):
        self.poligono_puntos.append((event.x, event.y))  # Añade el punto actual a la lista de puntos del polígono
        if len(self.poligono_puntos) > 1:
            self.canvas.create_line(self.poligono_puntos[-2], self.poligono_puntos[-1], fill=self.color, width=self.espesor_pincel.get())  # Dibuja una línea entre los puntos

    def cerrar_poligono(self, event):
        if len(self.poligono_puntos) > 2:
            self.canvas.create_polygon(self.poligono_puntos, outline=self.color, fill='', width=self.espesor_pincel.get())  # Dibuja el polígono
            self.poligono_puntos = []  # Resetea la lista de puntos

    def activar_texto(self):
        self.desactivar_lapiz()  # Desactiva cualquier otra herramienta
        self.current_tool = "text"  # Establece la herramienta actual como texto
        self.canvas.config(cursor="xterm")  # Cambia el cursor a un cursor de texto
        self.canvas.bind("<Button-1>", self.colocar_texto)  # Vincula el evento de clic izquierdo a la función colocar_texto

    def colocar_texto(self, event):
        texto = simpledialog.askstring("Texto", "Introduzca el texto:")  # Solicita al usuario que introduzca el texto
        if texto:
            self.canvas.create_text(event.x, event.y, text=texto, fill=self.color, font=("Arial", 12, "bold"))  # Crea el texto en el lienzo

    def paint(self, event):
        if self.current_tool == "paint":
            x1, y1, x2, y2 = (event.x - self.espesor_pincel.get() / 2), (event.y - self.espesor_pincel.get() / 2), (event.x + self.espesor_pincel.get() / 2), (event.y + self.espesor_pincel.get() / 2)
            elemento = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)
            self.elementos_dibujados.append(elemento)  # Agrega el elemento dibujado a la lista
            self.undo_stack.append(elemento)

    def dibujar_linea(self, event):  # Define la función para dibujar una línea
        if self.current_tool == "line":
            self.canvas.create_line(self.linea_x, self.linea_y, event.x, event.y, fill=self.color, width=self.espesor_pincel.get())

    def dibujar_rectangulo(self, event):  # Define la función para dibujar un rectángulo
        if self.current_tool == "rectangle":
            self.canvas.create_rectangle(self.linea_x, self.linea_y, event.x, event.y, outline=self.color, width=self.espesor_pincel.get())

    def dibujar_ovalo(self, event):  # Define la función para dibujar un óvalo
        if self.current_tool == "oval":
            self.canvas.create_oval(self.linea_x, self.linea_y, event.x, event.y, outline=self.color, width=self.espesor_pincel.get())

    def guardar(self, event=None):  # Define la función de guardar
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])  # Abre el diálogo de guardar archivo
        if filename:  # Si se seleccionó un nombre de archivo
            x = self.canvas.winfo_rootx() + self.canvas.winfo_x()
            y = self.canvas.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            image = ImageGrab.grab(bbox=(x, y, x1, y1))  # Captura la imagen del lienzo
            image.save(filename)  # Guarda la imagen en el archivo seleccionado

    def deshacer(self):
        if self.undo_stack:  # Verifica si la pila de deshacer no está vacía
            elemento = self.undo_stack.pop()  # Elimina el último elemento de la pila
            self.canvas.delete(elemento)  # Elimina el elemento dibujado del lienzo
            self.elementos_dibujados.remove(elemento)

    def desactivar_lapiz(self):
        self.canvas.unbind('<B1-Motion>')  # Desvincula el evento de arrastre del ratón
        self.canvas.unbind('<Button-1>')  # Desvincula el evento de clic izquierdo
        self.canvas.unbind('<ButtonRelease-1>')  # Desvincula el evento de soltar clic izquierdo
        self.canvas.unbind('<Button-3>')  # Desvincula el evento de clic derecho

# Inicializa la aplicación
Paint()
