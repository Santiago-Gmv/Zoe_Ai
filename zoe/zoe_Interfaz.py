'''
¡Hola! Este es el código principal de Zoe, tu asistente virtual con IA.
Importamos un montón de cosas chulas para que Zoe pueda hacer de todo.
'''
import sys
import pyttsx3
import datetime
import webbrowser
import wikipedia
import google.generativeai as genai
import os
import speech_recognition as sr
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, QLineEdit, QApplication
from PyQt5.QtCore import QTimer

'''
Aquí empieza la clase principal de Zoe. Es como el cerebro de nuestra asistente.
'''
class ZoeInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        
        '''
        Configuramos la ventana principal. Le damos un título chulo y un icono para que se vea guay.
        '''
        self.setWindowTitle("Zoe_ChatAi")
        self.setWindowIcon(QtGui.QIcon('img/icono.png'))
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #468986;")
        
        '''
        Configuramos Gemini, el cerebro de IA de Zoe. Es como darle superpoderes.
        '''
        genai.configure(api_key='AIzaSyD4d-LtLFXMhEGubrFORjGPUDnoc_QllJQ')
        self.model = genai.GenerativeModel('gemini-pro')
        
        '''
        Creamos la interfaz de usuario. Es como el cuerpo de Zoe, donde puedes interactuar con ella.
        '''
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        '''
        Añadimos una caja de texto donde Zoe mostrará sus respuestas. Es como su boca digital.
        '''
        self.text_box = QTextEdit()
        self.text_box.setStyleSheet("background-color: #2C3E50; color: white; font-size: 25px; border-radius: 10px; font-family: 'Comic Sans MS';")
        self.text_box.setReadOnly(True)
        self.layout.addWidget(self.text_box)

        '''
        Creamos los controles para interactuar con Zoe: una entrada de texto, un botón de enviar y un botón de micrófono.
        '''
        self.input_layout = QHBoxLayout()

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Por favor, ingresa tu nombre...")
        self.entry.setStyleSheet("background-color: #BBABBB; color: white; font-size: 25px; border-radius: 10px;")
        self.entry.returnPressed.connect(self.handle_name_entry)
        self.input_layout.addWidget(self.entry)

        self.send_button = QPushButton("Enviar")
        self.send_button.setStyleSheet("background-color: #1ABC9C ; color: white; font-size: 30px; border-radius: 10px;")
        self.send_button.clicked.connect(self.handle_name_entry)
        self.input_layout.addWidget(self.send_button)

        self.mic_button = QPushButton("🎤")
        self.mic_button.setStyleSheet("background-color: #1ABC9C ; color: white; font-size: 30px; border-radius: 10px;")
        self.mic_button.clicked.connect(self.toggle_microphone)
        self.input_layout.addWidget(self.mic_button)

        self.layout.addLayout(self.input_layout)

        '''
        Inicializamos algunas cosas importantes: el nombre del usuario, el motor de voz y el reconocimiento de voz.
        '''
        self.user_name = ""
        self.engine = self.init_engine()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False

        '''
        Zoe saluda al usuario. Es como decir "¡Hola, estoy lista para ayudarte!"
        '''
        self.display_text("Bienvenido! Por favor, ingresa tu nombre para empezar.", user=False)

    '''
    Configuramos el motor de voz de Zoe. Es como darle una voz humana.
    '''
    def init_engine(self):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        sp_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_LAURA_11.0"
        engine.setProperty('voice', sp_voice_id)
        engine.setProperty('rate', 130)
        return engine

    '''
    Esta función hace que Zoe hable. Es como darle vida a sus palabras.
    '''
    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    '''
    Muestra el texto en la interfaz. Es como escribir en la pantalla lo que Zoe dice.
    '''
    def display_text(self, text, user=False):
        self.text_box.append(f"{text}\n")
        self.text_box.ensureCursorVisible()

    '''
    Zoe saluda al usuario por su nombre. Es como dar una bienvenida personalizada.
    '''
    def greet_user(self, name):
        greeting = f"Hola {name}, ¿cómo estás hoy?"
        self.speak(greeting)

    '''
    Maneja la entrada del nombre del usuario. Es como presentarse a Zoe.
    '''
    def handle_name_entry(self):
        if not self.user_name:
            self.user_name = self.entry.text().strip()
            if self.user_name:
                self.greet_user(self.user_name)
                self.display_text(f"Hola {self.user_name}, ¿cómo puedo ayudarte hoy?", user=False)
                self.entry.clear()
                self.entry.setPlaceholderText("Escribe un comando...")
                self.entry.returnPressed.connect(self.send_command)
                self.send_button.clicked.connect(self.send_command)
            else:
                self.display_text("Por favor, ingresa tu nombre.", user=False)
        else:
            self.send_command()

    '''
    Envía un comando a Zoe. Es como pedirle que haga algo.
    '''
    def send_command(self):
        user_input = self.entry.text().strip()
        if user_input:
            self.display_text(f"{self.user_name}: {user_input}", user=True)
            self.entry.clear()
            response = self.process_command(user_input.lower())
            if response:
                self.display_text(f"Zoe: {response}", user=False)

    '''
    Zoe usa su IA para responder preguntas. Es como su proceso de pensamiento.
    '''
    def responder_pregunta(self, query):
        response = self.model.generate_content(query)
        return response.text

    '''
    Procesa los comandos del usuario. Es como el cerebro de Zoe decidiendo qué hacer.
    '''
    def process_command(self, query):
        '''
        Aquí hay un montón de 'elif' que manejan diferentes comandos.
        Es como si Zoe tuviera una lista de cosas que sabe hacer y elige la adecuada.
        '''
        if 'wikipedia' in query.lower():
            wikipedia.set_lang("es")
            self.speak('Buscando en Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                self.speak(results)
                return results
            except wikipedia.exceptions.DisambiguationError as e:
                self.speak("Hay múltiples opciones. Por favor, sé más específico.")
                return str(e)
            except wikipedia.exceptions.PageError as e:
                self.speak("No se encontró la página solicitada.")
                return str(e)
        elif 'libro' in query.lower():
            self.speak('Zoe esta Pensando...')
            query = query.replace("Zoe", "")
            results = self.responder_pregunta(query)
            self.speak(results)
            return results
        elif 'calculadora' in query.lower():
            os.startfile("C:\\Windows\\System32\\calc.exe")
            self.speak("Hecho, ¿algo más?")
        elif 'abre google' in query.lower():
            webbrowser.open("https://google.com")
            self.speak("Lo he realizado... ¿Puedo hacer algo más?")
        elif 'abre mercado libre' in query.lower():
            webbrowser.open("https://mercadolibre.com.ar")
            self.speak("Lo he realizado... ¿Puedo hacer algo más?")
        elif 'la hora' in query.lower():
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            self.speak(f"La hora es {current_time}")
            return f"La hora es {current_time}"
        elif 'fecha' in query.lower():
            current_date = datetime.datetime.now().strftime("%d/%m/%Y")
            self.speak(f"La fecha es {current_date}")
            return f"La fecha es {current_date}"
        elif 'saludar' in query.lower():
            self.speak("¡Hola! ¿En qué puedo ayudarte?")
            return "¡Hola! ¿En qué puedo ayudarte?"
        elif 'nada mas 'or 'nada más' in query.lower():
            self.speak("Hasta luego, ¡que tengas un buen día!")
            self.close()
        elif 'google' in query.lower():
            self.speak("Buscando en Google...")
            query = query.replace("google", "")
            webbrowser.open("https://google.com/search?q=" + query)
            return "He encontrado lo que buscabas"
        elif 'youtube' in query.lower():
            self.speak("Buscando en YouTube...")
            query = query.replace("youtube", "")
            webbrowser.open("https://youtube.com/search?q=" + query)
            return "He encontrado lo que buscabas"
        elif 'clima' in query.lower():
            self.speak("Buscando clima...")
            query = query.replace("clima", "")
            webbrowser.open("https://www.google.com/search?q=" + query + "clima")
            return "He encontrado lo que buscabas"
        elif 'spotify' in query.lower():
            self.speak("Buscando en Spotify...")
            query = query.replace("play list spotify", "")
            webbrowser.open("https://open.spotify.com/search/" + query)
            return "He encontrado lo que buscabas"
        elif 'Hola' in query.lower():
            self.speak(f"Hola, soy Zoe, tu asistente de inteligencia artificial. "
                       "Estoy aquí para ayudarte con cualquier cosa que necesites. "
                       "Puedo asistirte en tareas diarias, responder preguntas, "
                       "proporcionar información actualizada y mucho más. "
                       "Mi objetivo es hacer tu vida más fácil y ayudarte a alcanzar tus metas.")
            return "He encontrado lo que buscabas"
        else:
            self.speak("Lo siento, no he podido comprender eso. ¿Podrías repetirlo?")
            return "No he podido comprender eso. ¿Podrías repetirlo?"

    '''
    Activa o desactiva el micrófono. Es como darle oídos a Zoe.
    '''
    def toggle_microphone(self):
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()

    '''
    Inicia la escucha del micrófono. Es como decirle a Zoe "¡Pon atención!"
    '''
    def start_listening(self):
        self.is_listening = True
        self.mic_button.setStyleSheet("background-color: #ff9d9d; color: white; font-size: 30px; border-radius: 10px;")
        self.speak("Escuchando...")
        QTimer.singleShot(100, self.listen_for_speech)

    '''
    Detiene la escucha del micrófono. Es como decirle a Zoe "Ya puedes relajarte"
    '''
    def stop_listening(self):
        self.is_listening = False
        self.mic_button.setStyleSheet("background-color: #9de5ff; color: white; font-size: 30px; border-radius: 10px;")

    '''
    Escucha y procesa el discurso del usuario. Es como los oídos y el cerebro de Zoe trabajando juntos.
    '''
    def listen_for_speech(self):
        if not self.is_listening:
            return

        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

            text = self.recognizer.recognize_google(audio, language='es-ES')
            self.display_text(f"Tú: {text}", user=True)
            response = self.process_command(text.lower())
            if response:
                self.display_text(f"Zoe: {response}", user=False)
        except sr.WaitTimeoutError:
            self.speak("No se detectó ningún audio. Por favor, intenta de nuevo.")
        except sr.UnknownValueError:
            self.speak("No pude entender lo que dijiste. Por favor, intenta de nuevo.")
        except sr.RequestError as e:
            self.speak(f"Error en el servicio de reconocimiento de voz; {e}")
        finally:
            self.stop_listening()

'''
Este es el punto de entrada del programa. Es como encender a Zoe y ponerla en marcha.
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZoeInterface()
    window.show()
    sys.exit(app.exec_())