import tkinter as tk
from tkinter import messagebox, font
import subprocess
import os
import sys

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        # Configuración de la ventana
        self.root.title("Sistema de Redes de Petri")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        # Estilos de fuente
        title_font = font.Font(family="Arial", size=16, weight="bold")
        subtitle_font = font.Font(family="Arial", size=12)
        button_font = font.Font(family="Arial", size=12)
        
        # Frame para el contenido
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(main_frame, text="SISTEMA DE SIMULACIÓN DE REDES DE PETRI", 
                 font=title_font, bg="#f0f0f0", fg="#2c3e50").pack(pady=(0, 10))
        
        # Subtítulo
        tk.Label(main_frame, text="Universidad de San Carlos de Guatemala\nFacultad de Ingeniería\nDepartamento de Matemática\nMatemática para Computación 2", 
                 font=subtitle_font, bg="#f0f0f0", fg="#34495e", justify=tk.CENTER).pack(pady=(0, 20))
        
        # Frame para los botones
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Botones
        button_width = 30
        button_height = 2
        
        semaforo_btn = tk.Button(button_frame, text="1. Iniciar Simulación de Semáforos", 
                              command=self.ejecutar_semaforos, font=button_font,
                              width=button_width, height=button_height,
                              bg="#3498db", fg="white", relief=tk.FLAT,
                              activebackground="#2980b9", activeforeground="white")
        semaforo_btn.pack(pady=10)
        
        cadenas_btn = tk.Button(button_frame, text="2. Iniciar Evaluación de Cadenas", 
                             command=self.ejecutar_cadenas, font=button_font,
                             width=button_width, height=button_height,
                             bg="#2ecc71", fg="white", relief=tk.FLAT,
                             activebackground="#27ae60", activeforeground="white")
        cadenas_btn.pack(pady=10)
        
        salir_btn = tk.Button(button_frame, text="3. Salir", 
                           command=self.salir, font=button_font,
                           width=button_width, height=button_height,
                           bg="#e74c3c", fg="white", relief=tk.FLAT,
                           activebackground="#c0392b", activeforeground="white")
        salir_btn.pack(pady=10)

    def ejecutar_semaforos(self):
        """Ejecuta la aplicación de semáforos"""
        # Ocultar la ventana principal mientras se ejecuta el programa
        self.root.withdraw()
        
        # Mostrar mensaje
        messagebox.showinfo("Iniciando Simulación", 
                           "Iniciando la simulación de semáforos.\n\n"
                           "El servidor web se ejecutará en segundo plano.\n"
                           "Visite http://127.0.0.1:5000/ en su navegador para ver la simulación.\n\n"
                           "Para finalizar, cierre la aplicación.")
        
        try:
            # Ejecutar el script
            process = subprocess.Popen(["python", "app.py"], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
                        
            # No esperamos a que termine, porque Flask bloquea el hilo
            messagebox.showinfo("Información", 
                               "Servidor web iniciado en segundo plano.\n"
                               "Cuando termines, cierra la aplicación para volver al menú.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        
        # Mostrar nuevamente la ventana principal
        self.root.deiconify()
        
    def ejecutar_cadenas(self):
        """Ejecuta la aplicación de evaluación de cadenas"""
        # Ocultar la ventana principal mientras se ejecuta el programa
        self.root.withdraw()
        
        # Mostrar mensaje
        messagebox.showinfo("Iniciando Evaluación", 
                           "Iniciando la evaluación de cadenas.\n\n"
                           "Al finalizar, volverás al menú principal.")
        
        try:
            # Ejecutar el script y esperar a que termine
            process = subprocess.run(["python", "Cadenas.py"], 
                                   check=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True)
            
            # Mostrar el resultado
            messagebox.showinfo("Completado", 
                               "La evaluación de cadenas ha finalizado.\n\n"
                               "Volviendo al menú principal.")
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", 
                                f"La aplicación terminó con un error:\n{e.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        
        # Mostrar nuevamente la ventana principal
        self.root.deiconify()
    
    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Estás seguro que deseas salir?"):
            self.root.destroy()
            sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()