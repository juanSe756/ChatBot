import tkinter as tk
from tkinter import scrolledtext
from nltk.chat.util import Chat, reflections
import json

class ChatGUI:
    def __init__(self, bot):
        self.window = tk.Tk()
        self.window.title("ChatBot😁")

        # Configurar la geometría para centrar la ventana
        window_width = 400
        window_height = 300
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Contenedor principal
        main_frame = tk.Frame(self.window, bg="#005C53")
        main_frame.pack(expand=True, fill="both")

        # Área de mensajes
        self.message_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=40, height=10)
        self.message_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)  # Aumenté el valor de columnspan

        # Entrada de texto
        self.input_entry = tk.Entry(main_frame, width=30)
        self.input_entry.grid(column=0, row=1, padx=10, pady=10)

        # Botón de enviar
        send_button = tk.Button(main_frame, text="Enviar🔼", command=self.send_message, font=("Helvetica", 10, "bold"), bg="#9FC131", fg="white")
        send_button.grid(column=1, row=1, padx=(0, 10), pady=10)  # Ajusté el padx para acercar el botón al campo de entrada

        # Configurar la tecla Enter
        self.window.bind('<Return>', self.send_message)

        # Hacer que la ventana no sea redimensionable
        self.window.resizable(width=False, height=False)

        # Instanciar el bot
        self.bot = bot

    def send_message(self, event=None):
        message_user = self.input_entry.get()
        if message_user:
            self.message_area.insert(tk.END, "Tú: " + message_user + "\n", ("blue_bold",))
            response = self.bot.respond(message_user)
            if(response == None):
                self.message_area.insert(tk.END, "Bot: " + "Ups eso ultimo no lo entendi :(" + "\n", ("black_bold",))
            elif(response.startswith('*')):
                self.message_area.insert(tk.END, "Bot: " + response[1:] + "\n", ("black_bold",))
            else:
                self.message_area.insert(tk.END, "Bot: " + "Segun mi info, es "+response + "\n", ("black_bold",))
            self.input_entry.delete(0, tk.END)

    def run(self):
        self.message_area.tag_configure("blue_bold", foreground="#00B4D8", font=("Helvetica", 10, "bold"))
        self.message_area.tag_configure("black_bold", foreground="black", font=("Helvetica", 10, "bold"))
        self.message_area.insert(tk.END, "Bot: " + "¿De qué hablaremos hoy? :)" + "\n", ("black_bold",))
        self.window.mainloop()

class Bot:
    def __init__(self):
        self.pairs = self.load_corpus('corpus/movies.json')+self.load_corpus('corpus/games.json')+self.load_corpus('corpus/greetings.json')
        self.chat = Chat(self.pairs, reflections)

    def load_corpus(self, file_path):
        with open(file_path, 'r') as corpus_file:
            data = json.load(corpus_file)

        pairs = []
        for entry in data['data']:
            question = entry['question'].lower()
            answers = [answer.lower() for answer in entry['value']]
            pairs.append((question, answers))
        return pairs

    def respond(self, message):
        return self.chat.respond(message.lower())

if __name__ == "__main__":
    chat_bot = Bot()
    chat_gui = ChatGUI(chat_bot)
    chat_gui.run()
