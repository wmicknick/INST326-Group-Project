import unittest
from budget_final import BudgetCalculator

class TestBudgetCalculator(unittest.TestCase):
    def test_expense_proportions(self):
        budget = BudgetCalculator(income=2500, hours=40, rent=1500, car=400, gas=250, food=150, subscriptions=50, savings=100, goal=30)
        expense_pie_chart, greatest_expense, free_money_proportion = budget.expense_proportions()
        self.assertEqual(expense_pie_chart['Rent'], 60)
        self.assertEqual(free_money_proportion, 2)
        self.assertEqual(greatest_expense, 'Rent')

    def test_calculate_hourly_wage(self):
        budget = BudgetCalculator(income=2500, hours=40, rent=1500, car=400, gas=250, food=150, subscriptions=50, savings=100, goal=30)
        hourly_wage = budget.hourly_wage()
        hourly_wage_trim = f"{hourly_wage:.2f}"
        self.assertEqual(hourly_wage_trim, '62.50')

    def test_calculate_daily_budget(self):
        budget = BudgetCalculator(income=2500, hours=40, rent=1500, car=400, gas=250, food=150, subscriptions=50, savings=100, goal=30)
        daily_allowance = budget.daily_budget()
        daily_allowance_trim = f"{daily_allowance:.2f}"
        self.assertEqual(daily_allowance_trim, '1.67')

    def test_allowance_goal_difference(self):
        budget = BudgetCalculator(income=2500, hours=40, rent=1500, car=400, gas=250, food=150, subscriptions=50, savings=100, goal=30)
        daily_allowance = budget.daily_budget()
        deficit_to_goal = budget.allowance_goal_difference(30, daily_allowance)
        deficit_to_goal_trim = f"{deficit_to_goal:.2f}"
        self.assertEqual(deficit_to_goal_trim, '28.33')

if __name__ == '__main__':
    unittest.main()
