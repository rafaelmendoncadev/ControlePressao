# 🏥 Sistema de Controle de Pressão Arterial e Glicose

Um sistema desktop moderno para monitoramento e controle de pressão arterial e níveis de glicose, desenvolvido em Python com interface gráfica intuitiva.

## 🎯 Funcionalidades

- ✅ **Cadastro de Medições**: Registro de pressão arterial (sistólica/diastólica), pulso e glicose
- ✅ **Validação de Dados**: Verificação automática de valores dentro de faixas médicas seguras
- ✅ **Classificação Médica**: Categorização automática da pressão arterial segundo diretrizes AHA
- ✅ **Histórico Visual**: Tabela com todos os registros e opção de exclusão
- ✅ **Gráficos Interativos**: Visualização temporal das medições com duplo eixo Y
- ✅ **Banco de Dados**: Armazenamento persistente em SQLite
- ✅ **Interface Moderna**: Design responsivo com tema escuro

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **CustomTkinter** - Interface gráfica moderna
- **Matplotlib** - Gráficos e visualizações
- **SQLite** - Banco de dados local
- **Tkinter** - Componentes base da interface

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/rafaelmendoncadev/ControlePressao.git
   cd ControlePressao
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python app.py
   ```

## 📊 Como Usar

### Adicionando Registros
1. Preencha os campos na lateral esquerda:
   - **Pressão Sistólica**: Valor "de cima" da pressão (ex: 120)
   - **Pressão Diastólica**: Valor "de baixo" da pressão (ex: 80)
   - **Pulso**: Frequência cardíaca em batimentos por minuto
   - **Glicose**: Nível de glicose em mg/dL (opcional)

2. Clique em "Adicionar Registro"

### Visualizando Dados
- **Tabela**: Visualize todos os registros ordenados por data
- **Gráfico**: Acompanhe a evolução temporal das medições
- **Classificação**: Cores indicam a classificação da pressão arterial

### Excluindo Registros
1. Selecione um registro na tabela
2. Clique em "Deletar Selecionado"
3. Confirme a exclusão

## 🎨 Classificação da Pressão Arterial

O sistema classifica automaticamente a pressão arterial segundo as diretrizes da American Heart Association:

| Categoria | Sistólica (mmHg) | Diastólica (mmHg) | Cor |
|-----------|------------------|-------------------|-----|
| Normal | < 120 | < 80 | 🟢 Verde |
| Elevada | 120-129 | < 80 | 🟡 Amarelo |
| Hipertensão Estágio 1 | 130-139 | 80-89 | 🟠 Laranja |
| Hipertensão Estágio 2 | 140-179 | 90-119 | 🔴 Vermelho |
| Crise Hipertensiva | ≥ 180 | ≥ 120 | 🔴 Vermelho Escuro |

## 🗂️ Estrutura do Projeto

```
ControlePressao/
├── app.py              # Interface principal
├── database.py         # Gerenciamento do banco de dados
├── models.py           # Modelos de dados
├── config.py           # Configurações da aplicação
├── requirements.txt    # Dependências
├── README.md          # Documentação
└── .gitignore         # Arquivos ignorados pelo Git
```

## 🔧 Configuração

As configurações podem ser ajustadas no arquivo `config.py`:

- **Dimensões da janela**
- **Cores e temas**
- **Faixas de validação**
- **Classificações médicas**
- **Localização do banco de dados**

## 📱 Capturas de Tela

### Interface Principal
![Interface Principal](docs/screenshot_main.png)

### Gráfico de Histórico
![Gráfico](docs/screenshot_graph.png)

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Roadmap

- [ ] **Exportação de dados** (PDF, Excel)
- [ ] **Relatórios estatísticos** avançados
- [ ] **Alertas e notificações**
- [ ] **Backup automático**
- [ ] **Importação de dados** externos
- [ ] **Múltiplos usuários**
- [ ] **Sincronização na nuvem**
- [ ] **Aplicativo mobile**

## 🐛 Reportando Bugs

Encontrou um bug? Abra uma [issue](https://github.com/rafaelmendoncadev/ControlePressao/issues) com:

- Descrição detalhada do problema
- Passos para reproduzir
- Sistema operacional e versão do Python
- Screenshots (se aplicável)

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Rafael Mendonça**
- GitHub: [@rafaelmendoncadev](https://github.com/rafaelmendoncadev)
- Email: rafaelmendoncadev@users.noreply.github.com

## ⚠️ Aviso Médico

Este software é apenas para fins de monitoramento pessoal e não substitui o acompanhamento médico profissional. Sempre consulte um médico para interpretação dos dados e orientações de tratamento.

---

<p align="center">
  Desenvolvido com ❤️ por Rafael Mendonça
</p>
