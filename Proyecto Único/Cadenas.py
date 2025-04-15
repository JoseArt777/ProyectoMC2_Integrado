import graphviz
import time
import os
import random
import shutil
from datetime import datetime

class PetriNet:
    def __init__(self, title="Red de Petri para Evaluar Cadenas"):
        # Definimos los estados (plazas) de la red
        self.places = {
            'inicio': 1,  #  1 token al inicio
            'letra': 0,
            'error': 0,
            'A': 0,
            'P': 0,
            'R': 0,
            'O': 0,
            'B': 0,
            'A2': 0,
            'D': 0,
            'O2': 0,
            'fin': 0
        }
        
        # Colores para las plazas por categoría
        self.place_colors = {
            'inicio': '#8DD3C7',  # Verde menta
            'letra': '#FFFFB3',   # Amarillo
            'error': '#FB8072',   # Rojo 
            'fin': '#80B1D3',     # Azul 
            'default': '#D9D9D9'  # Gris  para estados normales
        }
        
        # Se definen las transiciones y sus conexiones
        self.transitions = {
            'T_1': {'input': ['inicio'], 'output': ['letra']},
            'T_2': {'input': ['letra'], 'output': ['error', 'A']},
            'T_3': {'input': ['A'], 'output': ['P']},
            'T_8': {'input': ['A'], 'output': ['error']},
            'T_4': {'input': ['P'], 'output': ['R']},
            'T_9': {'input': ['P'], 'output': ['error']},
            'T_5': {'input': ['R'], 'output': ['O']},
            'T_10': {'input': ['R'], 'output': ['error']},
            'T_6': {'input': ['O'], 'output': ['B']},
            'T_11': {'input': ['O'], 'output': ['error']},
            'T_7': {'input': ['B'], 'output': ['A2']},
            'T_12': {'input': ['B'], 'output': ['error']},
            'T_13': {'input': ['A2'], 'output': ['D']},
            'T_14': {'input': ['A2'], 'output': ['error']},
            'T_15': {'input': ['D'], 'output': ['O2']},
            'T_16': {'input': ['D'], 'output': ['error']},
            'T_17': {'input': ['O2'], 'output': ['fin']},
            'T_18': {'input': ['O2'], 'output': ['error']}
        }
        
        self.title = title
        self.dot = graphviz.Digraph(comment=title, format='png')
        self.history = []
        self.current_step = 0
        
        # Añadir información de tiempo para los logs
        self.start_time = datetime.now()
    
    def get_place_color(self, place, tokens, highlight=False):
        """Determina el color de una plaza basado en su tipo y estado"""
        if highlight:
            return '#4CAF50'  # Verde 
        
        if tokens <= 0:
            return '#F5F5F5'  # Gris 
        
        if place in self.place_colors:
            return self.place_colors[place]
        
        if place in ['A', 'P', 'R', 'O', 'B', 'A2', 'D', 'O2']:
            letter_colors = {
                'A': '#007BFF',  # Azul
                'P': '#0096FF', 
                'R': '#00ACFF',
                'O': '#00C2FF',
                'B': '#00D8FF',
                'A2': '#00EEFF',
                'D': '#00FFC8',
                'O2': '#00FF95'  # Verde 
            }
            return letter_colors[place]
        
        return self.place_colors['default']
    
    def draw_net(self, highlight_char=None, char_processed=None, highlight_place=None):
        """Dibuja la red de Petri y guarda la imagen con estilo mejorado"""
        dot = graphviz.Digraph(comment=self.title, format='png')
        
        # Estilo general gráfica
        dot.attr(rankdir='LR', size='8,5', dpi='300')
        dot.attr('graph', fontname='Arial', fontsize='16', label=self.title, labelloc='t')
        dot.attr('node', fontname='Arial', fontsize='12')
        dot.attr('edge', fontname='Arial', fontsize='10')
        
        # Dibujar plazas (estados)
        for place, tokens in self.places.items():
            label = place
            if tokens > 0:
                label = f"{place}\n({tokens})"
            
            # Da formato de acuerdo al tipo de plaza
            color = self.get_place_color(place, tokens, place == highlight_place)
            penwidth = '1.5' if tokens > 0 else '0.8'
            dot.node(place, label, shape='circle', style='filled,rounded', 
                     fillcolor=color, color='#505050', penwidth=penwidth)
        
        # Dibujar transiciones 
        for trans_name, trans in self.transitions.items():
            # Comprueba si la transición está habilitada
            enabled = self.is_enabled(trans_name)
            color = '#4CAF50' if enabled else '#D9D9D9'  # Verde si está habilitada, gris si no
            dot.node(trans_name, trans_name, shape='box', style='filled,rounded', 
                     fillcolor=color, color='#505050', penwidth='1.2')
            
            # Conectar entradas a la transición con flechas
            for input_place in trans['input']:
                dot.edge(input_place, trans_name, color='#505050', penwidth='1.0', arrowsize='0.8')
            
            # Conectar transición a salidas
            for output_place in trans['output']:
                dot.edge(trans_name, output_place, color='#505050', penwidth='1.0', arrowsize='0.8')
        
        # Añadir información sobre el carácter procesado
        if char_processed:
            title = f"Procesando: '{char_processed}'"
            if highlight_char:
                title += f" - Evaluando: '{highlight_char}'"
            
            # Añadimos al gráfico
            dot.attr(label=title)
            dot.attr(fontsize='18', fontcolor='#303030')
            
            # Añade el paso actual
            step_label = f"Paso {self.current_step}"
            dot.attr('graph', label=f"{title}\n{step_label}")
        
        return dot
    
    def is_enabled(self, transition):
        """Comprueba si una transición está habilitada"""
        for input_place in self.transitions[transition]['input']:
            if self.places[input_place] <= 0:
                return False
        return True
    
    def fire_transition(self, transition):
        """Dispara una transición habilitada"""
        if not self.is_enabled(transition):
            return False
        
        #  tokens de entrada
        for input_place in self.transitions[transition]['input']:
            self.places[input_place] -= 1
        
        #  tokens de salida
        for output_place in self.transitions[transition]['output']:
            self.places[output_place] += 1
        
        return True
    
    def evaluate_character(self, char, full_string, current_index):
        """Evalúa un carácter y actualiza la red"""
        self.current_step += 1
        
        dot_before = self.draw_net(char, full_string, None)
        self.history.append(dot_before)
        
        result = "skipped"  #  se omitirá el carácter (dígito)
        
        if self.places['inicio'] > 0:
            self.fire_transition('T_1')
        
        # Si es un dígito, simplemente lo ignoramos sin cambiar el estado
        if char.isdigit():
            result = "skipped_digit"
            # No consumimos el token de 'letra' para dígitos
            if self.places['letra'] > 0:
                # Mantenemos el token en la plaza 'letra' para el siguiente carácter
                pass
        else:
            # Procesamos letras
            lowercase_char = char.lower()
            if lowercase_char == 'a' and self.places['letra'] > 0:
                self.fire_transition('T_2')
                result = "accepted_a"
            elif lowercase_char == 'p' and self.places['A'] > 0:
                self.fire_transition('T_3')
                result = "accepted_p"
            elif lowercase_char == 'r' and self.places['P'] > 0:
                self.fire_transition('T_4')
                result = "accepted_r"
            elif lowercase_char == 'o' and self.places['R'] > 0:
                self.fire_transition('T_5')
                result = "accepted_o"
            elif lowercase_char == 'b' and self.places['O'] > 0:
                self.fire_transition('T_6')
                result = "accepted_b"
            elif lowercase_char == 'a' and self.places['B'] > 0:
                self.fire_transition('T_7')
                result = "accepted_a2"
            elif lowercase_char == 'd' and self.places['A2'] > 0:
                self.fire_transition('T_13')
                result = "accepted_d"
            elif lowercase_char == 'o' and self.places['D'] > 0:
                self.fire_transition('T_15')
                result = "accepted_o2"
            elif lowercase_char == 'o' and self.places['O2'] > 0:
                self.fire_transition('T_17')
                result = "finished"
            else:
                # Para caracteres no esperados
                if self.places['letra'] > 0:
                    self.places['error'] += 1
                    self.places['letra'] -= 1
                elif self.places['A'] > 0:
                    self.fire_transition('T_8')
                elif self.places['P'] > 0:
                    self.fire_transition('T_9')
                elif self.places['R'] > 0:
                    self.fire_transition('T_10')
                elif self.places['O'] > 0:
                    self.fire_transition('T_11')
                elif self.places['B'] > 0:
                    self.fire_transition('T_12')
                elif self.places['A2'] > 0:
                    self.fire_transition('T_14')
                elif self.places['D'] > 0:
                    self.fire_transition('T_16')
                elif self.places['O2'] > 0:
                    self.fire_transition('T_18')
                result = "error"
        
        # Determina qué lugar destacar
        highlight_place = None
        if result.startswith("accepted"):
            if result == "accepted_a":
                highlight_place = "A"
            elif result == "accepted_p":
                highlight_place = "P"
            elif result == "accepted_r":
                highlight_place = "R"
            elif result == "accepted_o":
                highlight_place = "O"
            elif result == "accepted_b":
                highlight_place = "B"
            elif result == "accepted_a2":
                highlight_place = "A2"
            elif result == "accepted_d":
                highlight_place = "D"
            elif result == "accepted_o2":
                highlight_place = "O2"
        elif result == "error":
            highlight_place = "error"
        elif result == "finished":
            highlight_place = "fin"
        
        # Registrar el resultado después de procesar
        dot_after = self.draw_net(None, full_string, highlight_place)
        self.history.append(dot_after)
        
        return result
        
    def process_string(self, input_string):
        """Procesa una cadena completa a traves de la red de Petri"""
        print(f"\n{'='*50}")
        print(f" INICIANDO PROCESAMIENTO DE CADENA: '{input_string}'")
        print(f"{'='*50}")
        
        results = []
        
        # Reiniciar la red
        for place in self.places:
            self.places[place] = 0
        self.places['inicio'] = 1
        
        # Reiniciar contador de pasos
        self.current_step = 0
        
        self.history = [self.draw_net()]
        
        filtered_string = ""
        
        for i, char in enumerate(input_string):
            print(f"\nPaso {i+1}: Procesando carácter '{char}'")
            result = self.evaluate_character(char, input_string, i)
            results.append(result)
            
            status = ""
            if result == "skipped_digit":
                status = f"Digito ignorado"
            elif result.startswith("accepted"):
                letter = result.split("_")[1].upper()
                status = f"Letra '{letter}' aceptada"
                filtered_string += char.lower()
            elif result == "error":
                status = f"Error: caracter no valido"
            
            print(f"  => {status}")
        
        print("\nRESULTADO DEL PROCESAMIENTO:")
        print(f"Cadena filtrada: '{filtered_string}'")
        
        # Comprueba si la palabra "aprobado" se extrajo correctamente
        if filtered_string == "aprobado":
            print("\n[EXITO] ¡VALIDACIÓN EXITOSA! Se obtuvo la palabra 'aprobado'.")
            success = True
        else:
            print("\n[ERROR] La cadena no produce la palabra 'aprobado'.")
            success = False
        
        # tiempo de procesamiento
        elapsed = datetime.now() - self.start_time
        print(f"\nTiempo de procesamiento: {elapsed.total_seconds():.2f} segundos")
        print(f"{'='*50}\n")
        
        return success, filtered_string
        
    def generate_animation(self, output_dir="petri_animation", prefix=""):
        """Genera una secuencia de imagenes para la animación con mejor estilo"""
        
        # En lugar de usar timestamp, usamos directorios fijos para sobreescribir
        if prefix:
            dir_name = f"{output_dir}_{prefix}"
        else:
            dir_name = output_dir
            
        # Si el directorio ya existe, lo eliminamos para recrearlo
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            
        # Crear directorio
        os.makedirs(dir_name)
        
        print(f"\n GENERANDO ANIMACIÓN...")
        print(f"Directorio de salida: {dir_name}")
        
        for i, dot in enumerate(self.history):
            if i > 0: 
                step = (i // 2) + (0 if i % 2 == 0 else 0.5)
                frame_desc = f"Paso {step:.1f}"
                if step.is_integer():
                    frame_desc = f"Paso {int(step)}"
                
                # Añadir información de paso al gráfico
                dot.attr('graph', label=f"{dot.graph_attr.get('label', '')}\n{frame_desc}")
            
            # Generar el archivo con mejor nombre
            filename = f"{dir_name}/frame_{i:03d}"
            dot.render(filename, cleanup=True)
            print(f"  Generada imagen {i+1}/{len(self.history)}")
        
        print(f"\n Animación generada exitosamente con {len(self.history)} cuadros.")
        print(f"Ruta: {dir_name}")
        
        #  HTML  para visualizar la secuencia
        self._generate_html_viewer(dir_name)
        
        return len(self.history)
    
    def _generate_html_viewer(self, output_dir):
        """Genera un HTML básico para visualizar la secuencia de imágenes"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Visualizador de Red de Petri - {self.title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                }}
                .controls {{
                    display: flex;
                    justify-content: center;
                    margin: 20px 0;
                    gap: 10px;
                }}
                button {{
                    padding: 8px 15px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                }}
                button:hover {{
                    background-color: #2980b9;
                }}
                .frame-container {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .frame-info {{
                    margin: 15px 0;
                    font-size: 16px;
                    color: #7f8c8d;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 15px;
                    border-top: 1px solid #eee;
                    color: #7f8c8d;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Visualizador de Red de Petri</h1>
                <h2 style="text-align: center;">{self.title}</h2>
                
                <div class="controls">
                    <button id="btnPrev">Anterior</button>
                    <button id="btnPlay">Reproducir</button>
                    <button id="btnNext">Siguiente</button>
                    <span style="margin: 0 10px;">|</span>
                    <button id="btnSlower">Mas lento</button>
                    <button id="btnFaster">Mas rapido</button>
                </div>
                
                <div class="frame-info">
                    Frame: <span id="frameNum">1</span> / {len(self.history)}
                </div>
                
                <div class="frame-container">
                    <img id="frameImage" src="frame_000.png" alt="Frame" style="max-width: 100%;">
                </div>
                
                <div class="footer">
                    Generado el {datetime.now().strftime("%d/%m/%Y a las %H:%M:%S")}
                    <br>
                    Universidad de San Carlos de Guatemala - Facultad de Ingenieria
                </div>
            </div>
            
            <script>
                let currentFrame = 0;
                const totalFrames = {len(self.history)};
                let isPlaying = false;
                let playInterval;
                let playSpeed = 1000; // ms
                
                const frameImage = document.getElementById('frameImage');
                const frameNum = document.getElementById('frameNum');
                const btnPlay = document.getElementById('btnPlay');
                
                function updateFrame() {{
                    frameImage.src = `frame_${{currentFrame.toString().padStart(3, '0')}}.png`;
                    frameNum.textContent = currentFrame + 1;
                }}
                
                function nextFrame() {{
                    currentFrame = (currentFrame + 1) % totalFrames;
                    updateFrame();
                }}
                
                function prevFrame() {{
                    currentFrame = (currentFrame - 1 + totalFrames) % totalFrames;
                    updateFrame();
                }}
                
                function togglePlay() {{
                    isPlaying = !isPlaying;
                    btnPlay.textContent = isPlaying ? 'Pausar' : 'Reproducir';
                    
                    if (isPlaying) {{
                        playInterval = setInterval(nextFrame, playSpeed);
                    }} else {{
                        clearInterval(playInterval);
                    }}
                }}
                
                function adjustSpeed(faster) {{
                    if (faster) {{
                        playSpeed = Math.max(200, playSpeed - 200);
                    }} else {{
                        playSpeed = Math.min(2000, playSpeed + 200);
                    }}
                    
                    if (isPlaying) {{
                        clearInterval(playInterval);
                        playInterval = setInterval(nextFrame, playSpeed);
                    }}
                    
                    console.log(`Velocidad de reproduccion: ${{playSpeed}}ms`);
                }}
                
                document.getElementById('btnPrev').addEventListener('click', () => {{
                    if (isPlaying) togglePlay();
                    prevFrame();
                }});
                
                document.getElementById('btnNext').addEventListener('click', () => {{
                    if (isPlaying) togglePlay();
                    nextFrame();
                }});
                
                document.getElementById('btnPlay').addEventListener('click', togglePlay);
                document.getElementById('btnSlower').addEventListener('click', () => adjustSpeed(false));
                document.getElementById('btnFaster').addEventListener('click', () => adjustSpeed(true));
                
                // Inicializar
                updateFrame();
            </script>
        </body>
        </html>
        """
        
        with open(f"{output_dir}/viewer.html", "w") as file:
            file.write(html_content)
        
        print(f"Visor HTML generado: {output_dir}/viewer.html")

#  crea una cabecera estilizada
def print_header(text):
    border = "=" * 60
    print(f"\n{border}")
    print(f"{text.center(60)}")
    print(f"{border}\n")

def main():
    print_header("SIMULADOR DE REDES DE PETRI")
    print("Universidad de San Carlos de Guatemala")
    print("Facultad de Ingenieria")
    print("Departamento de Matematica")
    print("Matematica para Computacion 2")
    print("\nEvaluación de Cadenas de Caracteres")
    
    petri = PetriNet(title="Evaluacion de la Cadena 'aprobado'")
    
    # Ejemplo según el enunciado "A1P2R3O4B5A6D7O8"
    test_string = "A1P2R3O4B5A6D7O8"
    
    success, filtered = petri.process_string(test_string)
    
    # Generamos animación
    num_frames = petri.generate_animation(prefix="cadena_correcta")
    
    print("\nProbando con una cadena incorrecta:")
    petri = PetriNet(title="Evaluacion de una Cadena Incorrecta")
    petri.process_string("X1A2P3R4O5B6A7D8O9")
    petri.generate_animation(prefix="cadena_incorrecta")
    
    print_header("FIN DEL PROCESAMIENTO")
    # Esperar input del usuario antes de terminar
    input("\nPresione Enter para finalizar...")

if __name__ == "__main__":
    main()