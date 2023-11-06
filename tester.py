import unittest
from budget import BudgetCalculator

class Test(unittest.TestCase):
    def test_expense_proportions(self):
        budget = BudgetCalculator(income=5000, hours=160, rent=1000, car=500, gas=200, food=500, subscriptions=100, savings=1000, goal=30)
        expense_pie_chart, greatest_expense = budget.expense_proportions()
        self.assertEqual(expense_pie_chart['Rent'], 20)
        self.assertEqual(greatest_expense, 'Rent')

    def test_calculate_hourly_wage(self):
        budget = BudgetCalculator(income=5000, hours=160, rent=1000, car=500, gas=200, food=500, subscriptions=100, savings=1000, goal=30)
        hourly_wage = budget.calculate_hourly_wage()
        self.assertEqual(hourly_wage, 31.25)

    def test_calculate_daily_budget(self):
        budget = BudgetCalculator(income=5000, hours=160, rent=1000, car=500, gas=200, food=500, subscriptions=100, savings=1000, goal=30)
        daily_allowance = budget.calculate_daily_budget()
        self.assertEqual(daily_allowance, 10.0)

if __name__ == '__main__':
    unittest.main()
