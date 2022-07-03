import pytest
from app.Calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_correct(self):
        assert self.calc.multiply(self, 3, 5) == 15

    def test_adding_correct(self):
        assert self.calc.adding(self, 3, 5) == 8

    def test_division_correct(self):
        assert self.calc.division(self, 25, 5) == 5

    def test_subtraction_correct(self):
        assert self.calc.subtraction(self, 25, 5) == 20
