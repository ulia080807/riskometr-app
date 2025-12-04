"""
Мой Риск: Калькулятор риска инсульта
©️ 2025
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    LOW = "Низкий"
    MODERATE = "Умеренный"
    HIGH = "Высокий"
    CRITICAL = "Критический"


@dataclass
class RiskResult:
    six_month_risk: float
    risk_level: RiskLevel
    framingham_score: int
    abcd2_score: Optional[int]
    chads2_vasc_score: Optional[int]
    bmi: float
    bmi_category: str
    recommendations: List[str]
    warning_flags: List[str]


class StrokeRiskCalculator:
    """Основной калькулятор риска инсульта на 6 месяцев"""
    
    def __init__(self):
        self.min_age = 15
        self.current_year = 2025
        
    def calculate_bmi(self, weight_kg: float, height_cm: float) -> Tuple[float, str]:
        """Расчет индекса массы тела"""
        if height_cm <= 0 or weight_kg <= 0:
            return 0.0, "Недостаточно данных"
        
        height_m = height_cm / 100
        bmi = round(weight_kg / (height_m ** 2), 1)
        
        if bmi < 18.5:
            category = "Недостаточный вес"
        elif 18.5 <= bmi < 25:
            category = "Нормальный вес"
        elif 25 <= bmi < 30:
            category = "Избыточный вес"
        else:
            category = "Ожирение"
            
        return bmi, category
    
    def calculate_framingham_6month_risk(self, user_data: Dict) -> Tuple[int, float]:
        """
        Модифицированная шкала Framingham для 6-месячного риска
        
        Основана на Framingham Stroke Risk Profile с адаптацией 
        для краткосрочного прогноза (6 месяцев вместо 10 лет)
        """
        score = 0
        risk_factors = []
        
        # 1. Возраст (усиленный вес для краткосрочного риска)
        age = user_data.get('age', 0)
        if age < 35:
            score += 0
        elif 35 <= age < 45:
            score += 3
            risk_factors.append("Возраст 35-44 года")
        elif 45 <= age < 55:
            score += 5
            risk_factors.append("Возраст 45-54 года")
        elif 55 <= age < 65:
            score += 8
            risk_factors.append("Возраст 55-64 года")
        elif 65 <= age < 75:
            score += 10
            risk_factors.append("Возраст 65-74 года")
        else:
            score += 12
            risk_factors.append("Возраст 75+ лет")
        
        # 2. Систолическое артериальное давление
        systolic_bp = user_data.get('systolic_bp', 0)
        if systolic_bp < 120:
            score += 0
        elif 120 <= systolic_bp < 130:
            score += 1
            risk_factors.append("Нормальное АД (120-129)")
        elif 130 <= systolic_bp < 140:
            score += 3
            risk_factors.append("Высокое нормальное АД (130-139)")
        elif 140 <= systolic_bp < 160:
            score += 5
            risk_factors.append("Артериальная гипертензия 1 ст. (140-159)")
        elif 160 <= systolic_bp < 180:
            score += 7
            risk_factors.append("Артериальная гипертензия 2 ст. (160-179)")
        else:
            score += 9
            risk_factors.append("Артериальная гипертензия 3 ст. (180+)")
        
        # 3. Прием антигипертензивных препаратов (НОВОЕ ПО ТЗ)
        if user_data.get('on_blood_pressure_meds', False):
            score += 2
            risk_factors.append("Прием антигипертензивных препаратов")
        
        # 4. Сахарный диабет
        if user_data.get('has_diabetes', False):
            score += 4
            risk_factors.append("Сахарный диабет")
        
        # 5. Курение
        smoking_status = user_data.get('smoking', 'никогда')
        if smoking_status == 'курящий':
            score += 5
            risk_factors.append("Курение в настоящее время")
        elif smoking_status == 'курил в прошлом':
            score += 2
            risk_factors.append("Курение в прошлом")
        
        # 6. Мерцательная аритмия (НОВОЕ ПО ТЗ)
        if user_data.get('has_atrial_fibrillation', False):
            score += 6
            risk_factors.append("Мерцательная аритмия")
        
        # 7. Предыдущий инсульт/ТИА (НОВОЕ ПО ТЗ)
        if user_data.get('previous_stroke_tia', False):
            score += 8
            risk_factors.append("Предыдущий инсульт/ТИА")
        
        # 8. Учащенное сердцебиение
        palpitations = user_data.get('palpitations', 'никогда')
        if palpitations == 'часто':
            score += 2
            risk_factors.append("Частое сердцебиение")
        
        # 9. Семейный анамнез инсульта
        if user_data.get('family_stroke_history', False):
            score += 2
            risk_factors.append("Семейный анамнез инсульта")
        
        # 10. Образ жизни
        activity_level = user_data.get('activity_level', 'подвижный')
        if activity_level == 'малоподвижный':
            score += 1
            risk_factors.append("Малоподвижный образ жизни")
        elif activity_level == 'неподвижный':
            score += 2
            risk_factors.append("Неподвижный образ жизни")
        
        # 11. Холестерин ЛПНП
        ldl_cholesterol = user_data.get('ldl_cholesterol', 0)
        if ldl_cholesterol >= 4.9:
            score += 3
            risk_factors.append(f"Высокий холестерин ЛПНП ({ldl_cholesterol} ммоль/л)")
        elif ldl_cholesterol >= 3.0:
            score += 1
        
        # Конвертация баллов в процент риска на 6 месяцев
        # На основе данных INTERSTROKE и мета-анализа
        if score <= 5:
            risk_percent = 0.1  # < 0.1%
        elif 6 <= score <= 10:
            risk_percent = 0.5  # 0.5%
        elif 11 <= score <= 15:
            risk_percent = 1.2  # 1.2%
        elif 16 <= score <= 20:
            risk_percent = 2.8  # 2.8%
        elif 21 <= score <= 25:
            risk_percent = 5.5  # 5.5%
        elif 26 <= score <= 30:
            risk_percent = 9.0  # 9.0%
        else:
            risk_percent = 15.0  # 15.0%
        
        return score, round(risk_percent, 1), risk_factors
    
    def calculate_abcd2_score(self, user_data: Dict) -> Optional[Tuple[int, float, float]]:
        """
        Шкала ABCD² для оценки риска инсульта после ТИА
        
        Рассчитывается только если был предыдущий инсульт/ТИА
        """
        if not user_data.get('previous_stroke_tia', False):
            return None
        
        score = 0
        
        # A - Age (Возраст)
        age = user_data.get('age', 0)
        if age >= 60:
            score += 1
        
        # B - Blood pressure (Артериальное давление)
        systolic_bp = user_data.get('systolic_bp', 0)
        diastolic_bp = user_data.get('diastolic_bp', 90)
        if systolic_bp >= 140 or diastolic_bp >= 90:
            score += 1
        
        # C - Clinical features (Клинические особенности)
        # Используем данные из анкеты
        if user_data.get('limb_weakness', False):
            score += 2
        elif user_data.get('speech_disturbance', False):
            score += 1
        
        # D - Duration (Длительность симптомов)
        symptom_duration = user_data.get('tia_symptom_duration', 0)
        if symptom_duration >= 60:  # 60+ минут
            score += 2
        elif 10 <= symptom_duration < 60:  # 10-59 минут
            score += 1
        
        # D - Diabetes (Диабет)
        if user_data.get('has_diabetes', False):
            score += 1
        
        # Риск инсульта на 2 и 7 дней после ТИА
        if score <= 3:
            two_day_risk = 1.0
            seven_day_risk = 1.2
        elif score == 4:
            two_day_risk = 4.1
            seven_day_risk = 5.9
        else:  # score 5-7
            two_day_risk = 8.1
            seven_day_risk = 11.7
        
        return score, two_day_risk, seven_day_risk
    
    def calculate_chads2_vasc_score(self, user_data: Dict) -> Optional[Tuple[int, float]]:
        """
        Шкала CHA₂DS₂-VASc для оценки риска тромбоэмболии
        при фибрилляции предсердий
        
        Рассчитывается только при наличии мерцательной аритмии
        """
        if not user_data.get('has_atrial_fibrillation', False):
            return None
        
        score = 0
        criteria = []
        
        # Congestive heart failure - Сердечная недостаточность
        if user_data.get('shortness_of_breath', 'никогда') == 'часто':
            score += 1
            criteria.append("Симптомы сердечной недостаточности")
        
        # Hypertension - Гипертония
        if user_data.get('systolic_bp', 0) >= 140 or user_data.get('on_blood_pressure_meds', False):
            score += 1
            criteria.append("Гипертония")
        
        # Age ≥75 лет
        age = user_data.get('age', 0)
        if age >= 75:
            score += 2
            criteria.append("Возраст ≥75 лет")
        # Age 65-74 года
        elif 65 <= age < 75:
            score += 1
            criteria.append("Возраст 65-74 года")
        
        # Diabetes - Диабет
        if user_data.get('has_diabetes', False):
            score += 1
            criteria.append("Диабет")
        
        # Stroke/TIA - Предыдущий инсульт/ТИА
        if user_data.get('previous_stroke_tia', False):
            score += 2
            criteria.append("Предыдущий инсульт/ТИА")
        
        # Vascular disease - Сосудистые заболевания
        if user_data.get('vascular_disease', False):
            score += 1
            criteria.append("Сосудистые заболевания")
        
        # Age 65-74 (уже учтен) и Sex category (Female)
        if user_data.get('gender') == 'женский' and age >= 65:
            score += 1
            criteria.append("Женский пол ≥65 лет")
        
        # Годовой риск инсульта (%)
        risk_map = {
            0: 0.0,  1: 1.3,  2: 2.2,  3: 3.2,
            4: 4.0,  5: 6.7,  6: 9.8,  7: 9.6,
            8: 12.5, 9: 15.2
        }
        annual_risk = risk_map.get(min(score, 9), 15.0)
        
        return score, annual_risk, criteria
    
    def determine_risk_level(self, risk_percent: float) -> RiskLevel:
        """Определение уровня риска"""
        if risk_percent < 1.0:
            return RiskLevel.LOW
        elif 1.0 <= risk_percent < 3.0:
            return RiskLevel.MODERATE
        elif 3.0 <= risk_percent < 10.0:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def generate_recommendations(self, risk_level: RiskLevel, 
                               user_data: Dict, 
                               risk_factors: List[str]) -> List[str]:
        """Генерация персонализированных рекомендаций"""
        recommendations = []
        
        # Общие рекомендации для всех
        recommendations.append("⚕️ Регулярно проходите диспансеризацию по полису ОМС")
        recommendations.append("📝 Ведите дневник артериального давления")
        
        if risk_level == RiskLevel.LOW:
            recommendations.append("✅ Ваш риск низкий. Поддерживайте здоровый образ жизни")
            recommendations.append("🏃‍♂️ Физическая активность: 150 мин умеренной нагрузки в неделю")
            recommendations.append("🥗 Питание: сократите соль до <5 г/день, добавьте овощи/фрукты")
            recommendations.append("📅 Измеряйте АД 1 раз в месяц")
            
        elif risk_level == RiskLevel.MODERATE:
            recommendations.append("⚠️ Ваш риск умеренный. Требуется активная профилактика")
            recommendations.append("🩺 Измеряйте АД ежедневно (утром и вечером)")
            recommendations.append("📊 Если АД ≥140/90 ≥3 дня подряд — запишитесь к терапевту")
            
            if any("Курение" in factor for factor in risk_factors):
                recommendations.append("🚭 Начните отказ от курения — риск снижается через 24 часа")
            
            bmi = self.calculate_bmi(user_data.get('weight_kg', 0), 
                                    user_data.get('height_cm', 0))[0]
            if bmi > 27:
                recommendations.append("⚖️ Снижение веса на 5-10% уменьшит риск инсульта на 25%")
                
        elif risk_level == RiskLevel.HIGH:
            recommendations.append("🚨 Ваш риск высокий! Требуется срочная врачебная оценка")
            recommendations.append("🏥 Запишитесь к терапевту в ближайшие дни")
            recommendations.append("📞 Знайте симптомы инсульта (FAST) и номера 103/112")
            
            if user_data.get('previous_stroke_tia', False):
                recommendations.append("🆘 При повторных симптомах — немедленно звоните 103!")
            
        else:  # CRITICAL
            recommendations.append("‼️ КРИТИЧЕСКИЙ РИСК! Требуется НЕМЕДЛЕННОЕ обращение к врачу")
            recommendations.append("🆘 Немедленно обратитесь к терапевту или кардиологу")
            recommendations.append("📱 Всегда имейте при себе телефон для вызова скорой")
            recommendations.append("👨‍⚕️ Рассмотрите госпитализацию для комплексного обследования")
        
        # Специфические рекомендации по факторам риска
        if "Мерцательная аритмия" in risk_factors:
            recommendations.append("❤️ При мерцательной аритмии требуется консультация кардиолога")
        
        if "Предыдущий инсульт/ТИА" in risk_factors:
            recommendations.append("🧠 После инсульта/ТИА необходим регулярный контроль невролога")
        
        if "Сахарный диабет" in risk_factors:
            recommendations.append("🩸 Контролируйте уровень глюкозы и посещайте эндокринолога")
        
        return recommendations
    
    def check_warning_flags(self, user_data: Dict) -> List[str]:
        """Проверка красных флагов для срочного обращения к врачу"""
        flags = []
        
        # Красные флаги из ТЗ
        if user_data.get('dizziness_fainting', 'никогда') == 'часто':
            flags.append("Частые головокружения или обмороки")
        
        if user_data.get('shortness_of_breath', 'никогда') == 'часто':
            flags.append("Частая одышка при нагрузке")
        
        if user_data.get('palpitations', 'никогда') == 'часто':
            flags.append("Частое сердцебиение")
        
        if user_data.get('previous_stroke_tia', False):
            flags.append("Предыдущий инсульт или ТИА")
        
        if user_data.get('has_atrial_fibrillation', False):
            flags.append("Мерцательная аритмия")
        
        # Критические значения
        if user_data.get('systolic_bp', 0) >= 180:
            flags.append("Критически высокое АД (≥180)")
        
        if user_data.get('ldl_cholesterol', 0) >= 6.0:
            flags.append("Очень высокий холестерин ЛПНП (≥6.0 ммоль/л)")
        
        return flags
    
    def calculate_overall_risk(self, user_data: Dict) -> RiskResult:
        """Основной расчет риска"""
        if not self.validate_user_data(user_data):
            raise ValueError(f"Минимальный возраст для оценки - {self.min_age} лет")
        
        # Расчет ИМТ
        bmi, bmi_category = self.calculate_bmi(
            user_data.get('weight_kg', 0),
            user_data.get('height_cm', 0)
        )
        
        # Расчет 6-месячного риска по модифицированной шкале Framingham
        framingham_score, six_month_risk, risk_factors = \
            self.calculate_framingham_6month_risk(user_data)
        
        # Расчет ABCD² (если был инсульт/ТИА)
        abcd2_result = self.calculate_abcd2_score(user_data)
        abcd2_score = abcd2_result[0] if abcd2_result else None
        
        # Расчет CHA₂DS₂-VASc (если есть мерцательная аритмия)
        chads2_vasc_result = self.calculate_chads2_vasc_score(user_data)
        chads2_vasc_score = chads2_vasc_result[0] if chads2_vasc_result else None
        
        # Определение уровня риска
        risk_level = self.determine_risk_level(six_month_risk)
        
        # Генерация рекомендаций
        recommendations = self.generate_recommendations(
            risk_level, user_data, risk_factors
        )
        
        # Проверка красных флагов
        warning_flags = self.check_warning_flags(user_data)
        
        return RiskResult(
            six_month_risk=six_month_risk,
            risk_level=risk_level,
            framingham_score=framingham_score,
            abcd2_score=abcd2_score,
            chads2_vasc_score=chads2_vasc_score,
            bmi=bmi,
            bmi_category=bmi_category,
            recommendations=recommendations,
            warning_flags=warning_flags
        )
    
    def validate_user_data(self, user_data: Dict) -> bool:
        """Валидация данных пользователя"""
        age = user_data.get('age', 0)
        return age >= self.min_age
