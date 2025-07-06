# Configurações da aplicação
import os

# Configurações do banco de dados
DATABASE_NAME = 'controle_pressao.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)

# Configurações da interface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
THEME = "dark"
COLOR_THEME = "blue"

# Cores personalizadas
COLORS = {
    'primary': '#2196F3',
    'secondary': '#4CAF50',
    'danger': '#D32F2F',
    'warning': '#FFC107',
    'background': '#2B2B2B',
    'surface': '#565B5E',
    'text': 'white'
}

# Validações
VALIDATION_RANGES = {
    'sistolica': {'min': 70, 'max': 250},
    'diastolica': {'min': 40, 'max': 150},
    'pulso': {'min': 30, 'max': 200},
    'glicose': {'min': 50, 'max': 500}
}

# Classificações de pressão arterial (AHA Guidelines)
PRESSURE_CLASSIFICATIONS = {
    'normal': {'sistolica': (0, 120), 'diastolica': (0, 80), 'color': '#4CAF50'},
    'elevada': {'sistolica': (120, 129), 'diastolica': (0, 80), 'color': '#FFC107'},
    'hipertensao_1': {'sistolica': (130, 139), 'diastolica': (80, 89), 'color': '#FF9800'},
    'hipertensao_2': {'sistolica': (140, 180), 'diastolica': (90, 120), 'color': '#F44336'},
    'crise': {'sistolica': (180, 999), 'diastolica': (120, 999), 'color': '#B71C1C'}
}
