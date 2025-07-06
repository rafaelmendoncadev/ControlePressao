from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import config

@dataclass
class RegistroMedicao:
    """Modelo para representar um registro de medição."""
    id: Optional[int] = None
    data_hora: Optional[datetime] = None
    sistolica: int = 0
    diastolica: int = 0
    pulso: int = 0
    glicose: Optional[int] = None
    
    def __post_init__(self):
        if self.data_hora is None:
            self.data_hora = datetime.now()
    
    def validar(self) -> tuple[bool, str]:
        """Valida os dados do registro."""
        ranges = config.VALIDATION_RANGES
        
        # Validar sistólica
        if not (ranges['sistolica']['min'] <= self.sistolica <= ranges['sistolica']['max']):
            return False, f"Pressão sistólica deve estar entre {ranges['sistolica']['min']} e {ranges['sistolica']['max']} mmHg"
        
        # Validar diastólica
        if not (ranges['diastolica']['min'] <= self.diastolica <= ranges['diastolica']['max']):
            return False, f"Pressão diastólica deve estar entre {ranges['diastolica']['min']} e {ranges['diastolica']['max']} mmHg"
        
        # Validar pulso
        if not (ranges['pulso']['min'] <= self.pulso <= ranges['pulso']['max']):
            return False, f"Pulso deve estar entre {ranges['pulso']['min']} e {ranges['pulso']['max']} bpm"
        
        # Validar glicose (opcional)
        if self.glicose is not None and not (ranges['glicose']['min'] <= self.glicose <= ranges['glicose']['max']):
            return False, f"Glicose deve estar entre {ranges['glicose']['min']} e {ranges['glicose']['max']} mg/dL"
        
        # Validar lógica médica
        if self.sistolica <= self.diastolica:
            return False, "Pressão sistólica deve ser maior que a diastólica"
        
        return True, "Válido"
    
    def classificar_pressao(self) -> dict:
        """Classifica a pressão arterial segundo diretrizes médicas."""
        for categoria, valores in config.PRESSURE_CLASSIFICATIONS.items():
            if (valores['sistolica'][0] <= self.sistolica <= valores['sistolica'][1] and
                valores['diastolica'][0] <= self.diastolica <= valores['diastolica'][1]):
                return {
                    'categoria': categoria,
                    'cor': valores['color'],
                    'descricao': self._get_descricao_categoria(categoria)
                }
        return {'categoria': 'indefinida', 'cor': '#666666', 'descricao': 'Classificação indefinida'}
    
    def _get_descricao_categoria(self, categoria: str) -> str:
        """Retorna descrição legível da categoria."""
        descricoes = {
            'normal': 'Normal',
            'elevada': 'Pressão Elevada',
            'hipertensao_1': 'Hipertensão Estágio 1',
            'hipertensao_2': 'Hipertensão Estágio 2',
            'crise': 'Crise Hipertensiva'
        }
        return descricoes.get(categoria, 'Indefinida')
    
    def to_dict(self) -> dict:
        """Converte o registro para dicionário."""
        return {
            'id': self.id,
            'data_hora': self.data_hora.strftime('%Y-%m-%d %H:%M:%S') if self.data_hora else None,
            'sistolica': self.sistolica,
            'diastolica': self.diastolica,
            'pulso': self.pulso,
            'glicose': self.glicose
        }
    
    @classmethod
    def from_tuple(cls, data: tuple) -> 'RegistroMedicao':
        """Cria um registro a partir de uma tupla do banco de dados."""
        return cls(
            id=data[0],
            data_hora=datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S'),
            sistolica=data[2],
            diastolica=data[3],
            pulso=data[4],
            glicose=data[5]
        )
