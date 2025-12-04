"""
Тесты для калькулятора риска инсульта
"""

import unittest
from stroke_risk_calculator import StrokeRiskCalculator


class TestStrokeRiskCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = StrokeRiskCalculator()
    
    def test_bmi_calculation(self):
        # Нормальный вес
        bmi, category = self.calculator.calculate_bmi(70, 170)
        self.assertAlmostEqual(bmi, 24.2, delta=0.1)
        self.assertEqual(category, "Нормальный вес")
        
        # Ожирение
        bmi, category = self.calculator.calculat
