import tkinter as tk
from tkinter import messagebox, font, ttk
import subprocess
import os
import sys
import time
from PIL import Image, ImageTk  # Necesitarás instalar pillow: pip install pillow

class ModernMenuApp:
    def __init__(self, root):
        self.root = root
        # Obtener la ruta del directorio actual donde se encuentra el script
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Personalización de tema
        self.primary_color = "#2c3e50"  # Azul oscuro
        self.secondary_color = "#3498db"  # Azul claro
        self.accent_color = "#e74c3c"  # Rojo
        self.bg_color = "#ecf0f1"  # Gris muy claro
        self.text_color = "#2c3e50"  # Azul oscuro
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configuración de la ventana
        self.root.title("Sistema de Redes de Petri")
        self.root.geometry("800x600")
        self.root.configure(bg=self.bg_color)
        self.root.minsize(700, 500)  # Tamaño mínimo
        
        # Para que se redimensione apropiadamente
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Estilos para ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Usar un tema base más moderno
        
        # Configurar estilos personalizados
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Header.TLabel', 
                            background=self.primary_color, 
                            foreground='white', 
                            font=('Arial', 16, 'bold'),
                            padding=15)
        self.style.configure('Title.TLabel', 
                           background=self.bg_color, 
                           foreground=self.primary_color, 
                           font=('Arial', 22, 'bold'),
                           padding=10)
        self.style.configure('Subtitle.TLabel', 
                           background=self.bg_color, 
                           foreground=self.text_color, 
                           font=('Arial', 12),
                           padding=5)
        self.style.configure('Status.TLabel', 
                           background=self.bg_color, 
                           foreground="#7f8c8d", 
                           font=('Arial', 10, 'italic'),
                           padding=5)
        
        # Estilo para botones
        self.style.configure('Menu.TButton', 
                           font=('Arial', 12),
                           padding=10)
        self.style.map('Menu.TButton',
                     background=[('active', self.secondary_color), ('!active', self.primary_color)],
                     foreground=[('active', 'white'), ('!active', 'white')])
        
        self.style.configure('Exit.TButton', 
                           font=('Arial', 12),
                           padding=10)
        self.style.map('Exit.TButton',
                     background=[('active', '#c0392b'), ('!active', self.accent_color)],
                     foreground=[('active', 'white'), ('!active', 'white')])
        
        # Frame principal con margen
        main_frame = ttk.Frame(self.root, style='TFrame', padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Añadir logo (puedes reemplazar con tu propio logo)
        try:
            # Intentar cargar un logo (crea un archivo logo.png en la misma carpeta)
            logo_path = os.path.join(self.script_dir, "logo.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((80, 80), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(logo_img)
                logo_label = ttk.Label(header_frame, image=self.logo_img, background=self.bg_color)
                logo_label.grid(row=0, column=0, pady=10)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
        
        # Título principal
        title_label = ttk.Label(header_frame, text="SISTEMA DE SIMULACIÓN DE REDES DE PETRI", style='Title.TLabel')
        title_label.grid(row=1, column=0, pady=5)
        
        # Subtítulo
        subtitle_text = "Universidad de San Carlos de Guatemala\nFacultad de Ingeniería\nDepartamento de Matemática\nMatemática para Computación 2"
        subtitle_label = ttk.Label(header_frame, text=subtitle_text, style='Subtitle.TLabel', justify=tk.CENTER)
        subtitle_label.grid(row=2, column=0, pady=5)
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=1, column=0, sticky="ew", pady=10)
        
        # Frame de contenido
        content_frame = ttk.Frame(main_frame, style='TFrame')
        content_frame.grid(row=2, column=0, sticky="nsew", pady=20)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para los botones
        button_frame = ttk.Frame(content_frame, style='TFrame')
        button_frame.grid(row=0, column=0)
        
        # Configuración de botones con iconos
        button_width = 30
        
        # Botón de semáforos con frame para efecto de elevación
        semaforo_frame = ttk.Frame(button_frame, style='TFrame')
        semaforo_frame.pack(pady=10, padx=5)
        
        semaforo_btn = ttk.Button(semaforo_frame, 
                                text="1. Iniciar Simulación de Semáforos", 
                                command=self.ejecutar_semaforos, 
                                style='Menu.TButton',
                                width=button_width)
        semaforo_btn.pack(pady=2, padx=2)
        
        # Botón de cadenas
        cadenas_frame = ttk.Frame(button_frame, style='TFrame')
        cadenas_frame.pack(pady=10, padx=5)
        
        cadenas_btn = ttk.Button(cadenas_frame, 
                               text="2. Iniciar Evaluación de Cadenas", 
                               command=self.ejecutar_cadenas, 
                               style='Menu.TButton',
                               width=button_width)
        cadenas_btn.pack(pady=2, padx=2)
        
        # Botón de salir
        salir_frame = ttk.Frame(button_frame, style='TFrame')
        salir_frame.pack(pady=10, padx=5)
        
        salir_btn = ttk.Button(salir_frame, 
                             text="3. Salir", 
                             command=self.salir, 
                             style='Exit.TButton',
                             width=button_width)
        salir_btn.pack(pady=2, padx=2)
        
        # Footer con barra de estado
        footer_frame = ttk.Frame(main_frame, style='TFrame')
        footer_frame.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Separador antes del footer
        footer_separator = ttk.Separator(footer_frame, orient='horizontal')
        footer_separator.grid(row=0, column=0, sticky="ew", pady=10)
        
        # Mensaje de estado
        self.status_label = ttk.Label(footer_frame, text="Listo para ejecutar", style='Status.TLabel')
        self.status_label.grid(row=1, column=0, sticky="w", pady=(5, 5))
        
        # Versión
        version_label = ttk.Label(footer_frame, text="v1.0.0", style='Status.TLabel')
        version_label.grid(row=1, column=0, sticky="e", pady=(5, 5))

    def mostrar_mensaje_cargando(self, mensaje="Cargando..."):
        """Muestra una ventana de carga durante las operaciones"""
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Procesando")
        
        # Centrar en la pantalla
        window_width = 300
        window_height = 100
        screen_width = self.loading_window.winfo_screenwidth()
        screen_height = self.loading_window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.loading_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.loading_window.resizable(False, False)
        self.loading_window.configure(bg=self.bg_color)
        self.loading_window.transient(self.root)
        self.loading_window.grab_set()
        
        # Eliminar decoraciones de ventana
        self.loading_window.overrideredirect(True)
        
        # Crear un frame con borde para efecto de elevación
        border_frame = tk.Frame(self.loading_window, bg=self.primary_color, bd=2)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        inner_frame = tk.Frame(border_frame, bg=self.bg_color)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje
        msg_label = tk.Label(inner_frame, text=mensaje, font=('Arial', 12), bg=self.bg_color, fg=self.text_color)
        msg_label.pack(pady=(20, 10))
        
        # Barra de progreso
        progress = ttk.Progressbar(inner_frame, mode='indeterminate', length=200)
        progress.pack(pady=(0, 10))
        progress.start(10)
        
        self.loading_window.update()
        
    def cerrar_mensaje_cargando(self):
        """Cierra la ventana de carga"""
        if hasattr(self, 'loading_window') and self.loading_window.winfo_exists():
            self.loading_window.destroy()

    def ejecutar_semaforos(self):
        """Ejecuta la aplicación de semáforos"""
        # Ocultar la ventana principal mientras se ejecuta el programa
        self.root.withdraw()
        
        # Ruta del script de semáforos
        semaforos_path = os.path.join(self.script_dir, "Petri_Network_MC2-main", "app.py")
        self.status_label.config(text=f"Ruta de semáforos: {semaforos_path}")
        
        # Comprobar si el archivo existe
        if not os.path.exists(semaforos_path):
            messagebox.showerror("Error", 
                                f"No se encontró el archivo:\n{semaforos_path}\n\nVerifique la ubicación del archivo.")
            self.root.deiconify()
            return
        
        # Mostrar mensaje moderno
        messagebox.showinfo("Iniciando Simulación", 
                           "Iniciando la simulación de semáforos.\n\n"
                           "El servidor web se ejecutará en segundo plano.\n"
                           "Visite http://127.0.0.1:5000/ en su navegador para ver la simulación.\n\n"
                           "Para finalizar, cierre la ventana del servidor o presione Ctrl+C en la consola.")
        
        try:
            # Mostrar ventana de carga
            self.mostrar_mensaje_cargando("Iniciando el servidor...")
            self.root.update()
            
            # Ejecutar el script con la ruta correcta
            # Nos cambiamos al directorio donde está app.py antes de ejecutarlo
            app_dir = os.path.dirname(semaforos_path)
            original_dir = os.getcwd()
            os.chdir(app_dir)
            
            # Usamos Popen para ejecutar en segundo plano
            process = subprocess.Popen(["python", semaforos_path], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     shell=False,
                                     creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            # Volver al directorio original
            os.chdir(original_dir)
            
            # Esperar un poco para asegurarnos de que el servidor arrancó
            time.sleep(2)
            
            # Cerramos ventana de carga
            self.cerrar_mensaje_cargando()
                        
            # No esperamos a que termine, porque Flask bloquea el hilo
            messagebox.showinfo("Información", 
                               "Servidor web iniciado en segundo plano.\n"
                               "Cuando termines, cierra la aplicación para volver al menú.")
            
        except Exception as e:
            self.cerrar_mensaje_cargando()
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        
        # Mostrar nuevamente la ventana principal
        self.root.deiconify()
        
    def ejecutar_cadenas(self):
        """Ejecuta la aplicación de evaluación de cadenas"""
        # Ocultar la ventana principal mientras se ejecuta el programa
        self.root.withdraw()
        
        # Ruta del script de cadenas
        cadenas_path = os.path.join(self.script_dir, "Cadenas_modificado.py")
        
        # Si no existe el archivo modificado, intentamos con el original
        if not os.path.exists(cadenas_path):
            cadenas_path = os.path.join(self.script_dir, "Cadenas.py")
            
        self.status_label.config(text=f"Ruta de cadenas: {cadenas_path}")
        
        # Comprobar si el archivo existe
        if not os.path.exists(cadenas_path):
            messagebox.showerror("Error", 
                                f"No se encontró el archivo:\n{cadenas_path}\n\nVerifique la ubicación del archivo.")
            self.root.deiconify()
            return
        
        # Mostrar mensaje
        messagebox.showinfo("Iniciando Evaluación", 
                           "Iniciando la evaluación de cadenas.\n\n"
                           "Al finalizar, volverás al menú principal.")
        
        try:
            # Mostrar ventana de carga
            self.mostrar_mensaje_cargando("Iniciando el programa de cadenas...")
            self.root.update()
            
            # Ejecutar el script en un proceso separado para evitar problemas de codificación
            if os.name == 'nt':  # Windows
                process = subprocess.Popen(["python", cadenas_path], 
                                         creationflags=subprocess.CREATE_NEW_CONSOLE,
                                         cwd=self.script_dir)
                
                # Cerramos ventana de carga
                self.cerrar_mensaje_cargando()
                
                # Esperamos a que el usuario cierre la ventana de la consola
                messagebox.showinfo("En progreso", 
                                   "El programa está ejecutándose en una ventana separada.\n"
                                   "Cuando termines, cierra esa ventana y haz clic en Aceptar para volver al menú.")
                
                # Intentamos terminar el proceso por si sigue activo
                try:
                    process.terminate()
                except:
                    pass
            else:  # Linux/Mac
                # En sistemas Unix, ejecutamos y esperamos a que termine
                process = subprocess.run(["python", cadenas_path], 
                                       cwd=self.script_dir,
                                       check=False)  # No lanzar excepción si hay error
                
                # Cerramos ventana de carga
                self.cerrar_mensaje_cargando()
                
                # Mostrar el resultado
                messagebox.showinfo("Completado", 
                                   "La evaluación de cadenas ha finalizado.\n\n"
                                   "Volviendo al menú principal.")
            
        except Exception as e:
            self.cerrar_mensaje_cargando()
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        
        # Mostrar nuevamente la ventana principal
        self.root.deiconify()
    
    def salir(self):
        """Cierra la aplicación con un diálogo moderno"""
        result = messagebox.askyesno("Salir", "¿Estás seguro que deseas salir?")
        if result:
            # Animación de cierre
            self.mostrar_mensaje_cargando("Cerrando aplicación...")
            self.root.update()
            time.sleep(0.5)  # Breve pausa para mostrar la animación
            self.root.destroy()
            sys.exit(0)

def center_window(window):
    """Centra la ventana en la pantalla"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

class SplashScreen:
    """Pantalla de inicio para dar un aspecto más profesional"""
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Eliminar decoraciones de ventana
        
        # Colores
        self.bg_color = "#2c3e50"  # Azul oscuro
        self.text_color = "white"
        
        # Tamaño y posición
        width = 500
        height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configuración
        self.root.configure(bg=self.bg_color)
        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(self.frame, 
                              text="SISTEMA DE REDES DE PETRI", 
                              font=("Arial", 22, "bold"), 
                              bg=self.bg_color, 
                              fg=self.text_color)
        title_label.pack(pady=(40, 10))
        
        # Subtítulo
        subtitle_label = tk.Label(self.frame, 
                               text="Universidad de San Carlos de Guatemala", 
                               font=("Arial", 12), 
                               bg=self.bg_color, 
                               fg=self.text_color)
        subtitle_label.pack(pady=5)
        
        # Logo (opcional)
        try:
            # Puedes agregar tu propio logo
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((100, 100), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(self.frame, image=self.logo_img, bg=self.bg_color)
                logo_label.pack(pady=10)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
        
        # Barra de progreso
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=(20, 10), padx=50)
        
        # Mensaje de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Cargando...")
        self.status_label = tk.Label(self.frame, 
                                   textvariable=self.status_var, 
                                   font=("Arial", 10), 
                                   bg=self.bg_color, 
                                   fg=self.text_color)
        self.status_label.pack(pady=10)
        
        # Versión
        version_label = tk.Label(self.frame, 
                               text="v1.0.0", 
                               font=("Arial", 8), 
                               bg=self.bg_color, 
                               fg="#95a5a6")
        version_label.pack(side=tk.BOTTOM, pady=10)
        
        # Iniciar animación de carga
        self.update_progress()
        
    def update_progress(self):
        """Actualiza la barra de progreso y mensajes de estado"""
        status_messages = [
            "Cargando módulos...",
            "Inicializando sistema...",
            "Configurando entorno...",
            "Preparando interfaz...",
            "Casi listo..."
        ]
        
        # Simulación de carga progresiva
        for i in range(101):
            self.progress["value"] = i
            if i % 20 == 0 and i < 100:
                self.status_var.set(status_messages[i // 20])
            elif i == 100:
                self.status_var.set("¡Listo!")
            self.root.update()
            time.sleep(0.02)
        
        # Esperar un momento con el 100% antes de continuar
        time.sleep(0.5)
        self.root.destroy()

if __name__ == "__main__":
    # Mostrar pantalla de splash
    splash_root = tk.Tk()
    splash = SplashScreen(splash_root)
    splash_root.mainloop()
    
    # Iniciar la ventana principal
    root = tk.Tk()
    app = ModernMenuApp(root)
    center_window(root)
    root.mainloop()