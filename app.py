
import customtkinter as ctk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import RegistroMedicao
import database

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Controle de Pressão e Glicose")
        self.geometry("1100x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Frame de Entrada de Dados ---
        self.frame_entrada = ctk.CTkFrame(self, width=250)
        self.frame_entrada.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

        self.label_titulo_entrada = ctk.CTkLabel(self.frame_entrada, text="Novo Registro", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titulo_entrada.pack(pady=20)

        self.entry_sistolica = ctk.CTkEntry(self.frame_entrada, placeholder_text="Pressão Sistólica (mmHg)")
        self.entry_sistolica.pack(pady=10, padx=20, fill="x")

        self.entry_diastolica = ctk.CTkEntry(self.frame_entrada, placeholder_text="Pressão Diastólica (mmHg)")
        self.entry_diastolica.pack(pady=10, padx=20, fill="x")

        self.entry_pulso = ctk.CTkEntry(self.frame_entrada, placeholder_text="Frequência de Pulso (bpm)")
        self.entry_pulso.pack(pady=10, padx=20, fill="x")

        self.entry_glicose = ctk.CTkEntry(self.frame_entrada, placeholder_text="Glicose (mg/dL)")
        self.entry_glicose.pack(pady=10, padx=20, fill="x")

        self.botao_adicionar = ctk.CTkButton(self.frame_entrada, text="Adicionar Registro", command=self.adicionar_registro)
        self.botao_adicionar.pack(pady=20, padx=20, fill="x")

        self.botao_deletar = ctk.CTkButton(self.frame_entrada, text="Deletar Selecionado", command=self.deletar_registro, fg_color="#D32F2F", hover_color="#B71C1C")
        self.botao_deletar.pack(pady=10, padx=20, fill="x")

        # --- Frame Principal (Tabela e Gráfico) ---
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nswe")
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        # --- Tabela de Registros ---
        self.criar_tabela_registros()

        # --- Gráfico ---
        self.figura_grafico = plt.Figure(figsize=(5, 2), dpi=100)
        self.ax_grafico = self.figura_grafico.add_subplot(111)
        self.canvas_grafico = FigureCanvasTkAgg(self.figura_grafico, master=self.frame_principal)
        self.canvas_grafico.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.figura_grafico.patch.set_facecolor('#2B2B2B') # Cor de fundo do gráfico
        self.ax_grafico.set_facecolor('#2B2B2B')
        self.ax_grafico.tick_params(axis='x', colors='white')
        self.ax_grafico.tick_params(axis='y', colors='white')
        self.ax_grafico.spines['bottom'].set_color('white')
        self.ax_grafico.spines['top'].set_color('white') 
        self.ax_grafico.spines['right'].set_color('white')
        self.ax_grafico.spines['left'].set_color('white')

        self.atualizar_dados()

    def criar_tabela_registros(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#2B2B2B", 
                        foreground="white", 
                        fieldbackground="#2B2B2B", 
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#2255A8')])
        style.configure("Treeview.Heading", 
                        background="#565B5E", 
                        foreground="white", 
                        font=("Roboto", 10, "bold"))

        self.tabela = ttk.Treeview(self.frame_principal, 
                                     columns=("ID", "Data/Hora", "Sistólica", "Diastólica", "Pulso", "Glicose", "Classificação"), 
                                     show='headings')
        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Data/Hora", text="Data/Hora")
        self.tabela.heading("Sistólica", text="Sistólica (mmHg)")
        self.tabela.heading("Diastólica", text="Diastólica (mmHg)")
        self.tabela.heading("Pulso", text="Pulso (bpm)")
        self.tabela.heading("Glicose", text="Glicose (mg/dL)")
        self.tabela.heading("Classificação", text="Classificação")

        self.tabela.column("ID", width=40, anchor="center")
        self.tabela.column("Data/Hora", width=150, anchor="center")
        self.tabela.column("Sistólica", width=120, anchor="center")
        self.tabela.column("Diastólica", width=120, anchor="center")
        self.tabela.column("Pulso", width=100, anchor="center")
        self.tabela.column("Glicose", width=120, anchor="center")
        self.tabela.column("Classificação", width=120, anchor="center")

        self.tabela.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")

        self.tabela.tag_configure('Normal', background='#4CAF50', foreground='white')
        self.tabela.tag_configure('Elevada', background='#FFC107', foreground='black')
        self.tabela.tag_configure('Hipertensão Estágio 1', background='#FF9800', foreground='black')
        self.tabela.tag_configure('Hipertensão Estágio 2', background='#F44336', foreground='white')
        self.tabela.tag_configure('Crise Hipertensiva', background='#B71C1C', foreground='white')
        self.tabela.tag_configure('indefinida', background='#666666', foreground='white')

    def adicionar_registro(self):
        try:
            sistolica = int(self.entry_sistolica.get())
            diastolica = int(self.entry_diastolica.get())
            pulso = int(self.entry_pulso.get())
            glicose_str = self.entry_glicose.get()
            glicose = int(glicose_str) if glicose_str else None

            novo_registro = RegistroMedicao(
                sistolica=sistolica,
                diastolica=diastolica,
                pulso=pulso,
                glicose=glicose
            )
            
            valido, mensagem = novo_registro.validar()
            if not valido:
                messagebox.showerror("Erro de Validação", mensagem)
                return

            database.adicionar_registro(
                novo_registro.sistolica,
                novo_registro.diastolica,
                novo_registro.pulso,
                novo_registro.glicose
            )
            messagebox.showinfo("Sucesso", "Registro adicionado com sucesso!")
            self.limpar_campos()
            self.atualizar_dados()
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    def deletar_registro(self):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Nenhum Registro", "Por favor, selecione um registro na tabela para deletar.")
            return

        if messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja deletar o registro selecionado?"):
            item_id = self.tabela.item(selecionado, 'values')[0]
            database.deletar_registro(item_id)
            self.atualizar_dados()
            messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")

    def limpar_campos(self):
        self.entry_sistolica.delete(0, 'end')
        self.entry_diastolica.delete(0, 'end')
        self.entry_pulso.delete(0, 'end')
        self.entry_glicose.delete(0, 'end')

    def atualizar_dados(self):
        # Limpa a tabela
        for i in self.tabela.get_children():
            self.tabela.delete(i)
        
        # Busca e insere os novos dados
        registros = database.buscar_registros()
        for reg_tuple in registros:
            registro = RegistroMedicao.from_tuple(reg_tuple)
            classificacao = registro.classificar_pressao()
            
            # Adiciona o nome da categoria aos valores
            valores_tabela = list(reg_tuple)
            valores_tabela.append(classificacao['descricao'])

            # Usa a descrição como tag
            self.tabela.insert("", "end", values=valores_tabela, tags=(classificacao['descricao'],))
        
        # Atualiza o gráfico
        self.atualizar_grafico(registros)

    def atualizar_grafico(self, registros):
        self.ax_grafico.clear()
        if not registros:
            self.ax_grafico.text(0.5, 0.5, "Sem dados para exibir", 
                                 horizontalalignment='center', 
                                 verticalalignment='center', 
                                 fontsize=12, color='gray')
            self.canvas_grafico.draw()
            return

        # Inverte a ordem para o gráfico (do mais antigo para o mais novo)
        registros.reverse()
        
        datas = [reg[1].split(' ')[0] for reg in registros] # Apenas a data
        sistolicas = [reg[2] for reg in registros]
        diastolicas = [reg[3] for reg in registros]
        glicoses = [reg[5] if reg[5] is not None else 0 for reg in registros]

        self.ax_grafico.plot(datas, sistolicas, marker='o', linestyle='-', label='Sistólica (mmHg)', color='#4CAF50')
        self.ax_grafico.plot(datas, diastolicas, marker='o', linestyle='-', label='Diastólica (mmHg)', color='#2196F3')
        
        # Eixo Y secundário para a glicose
        ax2 = self.ax_grafico.twinx()
        ax2.plot(datas, glicoses, marker='s', linestyle='--', label='Glicose (mg/dL)', color='#FFC107')
        ax2.set_ylabel('Glicose (mg/dL)', color='#FFC107')
        ax2.tick_params(axis='y', colors='#FFC107')
        ax2.spines['right'].set_color('#FFC107')

        self.ax_grafico.set_title("Histórico de Medições", color='white')
        self.ax_grafico.set_ylabel("Pressão Arterial (mmHg)", color='white')
        self.ax_grafico.tick_params(axis='x', labelrotation=45)
        self.figura_grafico.tight_layout()

        # Legendas
        lines, labels = self.ax_grafico.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')

        self.canvas_grafico.draw()

if __name__ == "__main__":
    database.criar_tabela() # Garante que a tabela exista
    app = App()
    app.mainloop()
