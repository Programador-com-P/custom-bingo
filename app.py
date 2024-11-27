import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Navegação entre Telas")
        self.geometry("400x300")
        
        # Variável de controle para cancelamento
        self.task_cancelled = False
        
        # Dicionário de frames
        self.frames = {}
        
        # Adicionar telas
        for F in (StartPage, PageOne, LoadingPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Tela Inicial", font=("Arial", 16))
        label.pack(pady=20)
        
        next_button = tk.Button(self, text="Ir para Tela 1", 
                                command=lambda: controller.show_frame("PageOne"))
        next_button.pack()
        
        loading_button = tk.Button(self, text="Tela com Loading", 
                                   command=lambda: self.run_with_loading())
        loading_button.pack()
    
    def run_with_loading(self):
        # Resetar o cancelamento da tarefa
        self.controller.task_cancelled = False
        self.controller.frames["LoadingPage"].reset_feedback()
        self.controller.show_frame("LoadingPage")
        thread = Thread(target=self.long_running_task)
        thread.start()
    
    def long_running_task(self):
        # Simula uma execução demorada com feedback
        for i in range(10):  # Dividir o tempo total em partes
            if self.controller.task_cancelled:
                break
            time.sleep(0.5)  # Pequenos intervalos
            # Atualizar o feedback na tela de loading
            progress = (i + 1) * 10
            self.controller.frames["LoadingPage"].update_feedback(progress)
        # Retorna à tela inicial se a execução não foi cancelada
        if not self.controller.task_cancelled:
            self.controller.show_frame("StartPage")

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Tela 1", font=("Arial", 16))
        label.pack(pady=20)
        
        back_button = tk.Button(self, text="Voltar para Tela Inicial", 
                                command=lambda: controller.show_frame("StartPage"))
        back_button.pack()

class LoadingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Carregando...", font=("Arial", 16))
        label.pack(pady=10)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(self, mode="determinate", maximum=100)
        self.progress.pack(pady=10, fill=tk.X, padx=20)
        
        # Label de feedback dinâmico
        self.feedback_label = tk.Label(self, text="Iniciando...", font=("Arial", 12))
        self.feedback_label.pack(pady=10)
        
        # Botão de cancelar
        cancel_button = tk.Button(self, text="Cancelar e Voltar", 
                                  command=self.cancel_task)
        cancel_button.pack()
    
    def reset_feedback(self):
        """Reseta os elementos de feedback para o início."""
        self.progress["value"] = 0
        self.feedback_label.config(text="Iniciando...")
    
    def update_feedback(self, progress):
        """Atualiza o feedback do progresso."""
        self.progress["value"] = progress
        self.feedback_label.config(text=f"Progresso: {progress}% concluído.")
    
    def cancel_task(self):
        """Cancela a tarefa e volta à página inicial."""
        self.controller.task_cancelled = True
        self.controller.show_frame("StartPage")

if __name__ == "__main__":
    app = App()
    app.mainloop()
