"""
Модуль для управления анкетой пользователя
©️ 2025
"""

from typing import Dict, List
import json
from datetime import datetime


class Questionnaire:
    """Управление анкетой пользователя"""
    
    def __init__(self):
        self.required_fields = [
            'age', 'gender', 'height_cm', 'weight_kg',
            'systolic_bp', 'has_diabetes', 'smoking'
        ]
        
        self.questions = [
            {
                'id': 'age',
                'text': 'Ваш возраст (лет)',
                'type': 'number',
                'min': 15,
                'max': 100,
                'required': True
            },
            {
                'id': 'gender',
                'text': 'Ваш пол',
                'type': 'select',
                'options': ['мужской', 'женский'],
                'required': True
            },
            {
                'id': 'on_blood_pressure_meds',
                'text': 'Принимаете ли вы лекарства от давления?',
                'type': 'radio',
                'options': ['да', 'нет'],
                'required': True
            },
            {
                'id': 'has_atrial_fibrillation',
                'text': 'Есть ли мерцательная аритмия?',
                'type': 'radio',
                'options': ['да', 'нет'],
                'required': True
            },
            {
                'id': 'previous_stroke_tia',
                'text': 'Был ли инсульт/ТИА ранее?',
                'type': 'radio',
                'options': ['да', 'нет'],
                'required': True
            }
        ]
    
    def validate_responses(self, responses: Dict) -> List[str]:
        """Валидация ответов"""
        errors = []
        
        # Проверка возраста
        age = responses.get('age')
        if age and age < 15:
            errors.append("Минимальный возраст для оценки - 15 лет")
        
        # Проверка обязательных полей
        for field in self.required_fields:
            if field not in responses or responses[field] is None:
                errors.append(f"Обязательное поле '{field}' не заполнено")
        
        return errors
    
    def save_responses(self, responses: Dict, filename: str = None):
        """Сохранение ответов в файл"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"анкета_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'responses': responses,
            'app_version': '1.0',
            'year': 2025
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename
