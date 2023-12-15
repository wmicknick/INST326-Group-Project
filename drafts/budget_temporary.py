from argparse import ArgumentParser
import sys

class BudgetCalculator:
    '''This class takes in data regarding income and expenses, and transforms this data into user metrics
        such as the proportion of income going to each expense. It also calculates the differnece between the user's
        budgetary goal and their current budget, and gives suggestions on how to match them.

        Attributes:
            income(float): total income entered
            hours(int): number of hours worked in a week
            rent(float): amount going towards living expenses per month
            car(float): car payment per month
            gas(float): gas costs per month
            food(float): food costs per month
            subscriptions(float): monthly total of subscriptions (e.g. Netflix, Disney+)
            goal(int): the daily allowance the user would like to have
    '''


    def __init__(self, income, hours, rent, car, gas, food, subscriptions, savings, goal):
        '''Initializes the class varibles, based on given parameters and used in other class methods.

            Args:
                See class documentation.
        '''
        self.income = income
        self.hours_worked = hours
        self.expenses = {
            'Rent': rent,
            'Car Payment': car,
            'Gas': gas,
            'Food': food,
            'Subscriptions': subscriptions,
            'Savings': savings
        }
        self.total_expenses = 0
        for item in self.expenses: #Total of all expenses
            self.total_expenses += self.expenses[item]
        self.over_budget = False # We will assume they are not over budget already (for now).
        self.goal = goal


    def expense_proportions(self):
        '''Calculates what proportion of the user's income is going towards each individual expense, as well as saving which expense in particular
            makes up the largest portion. In addition, any proportion of income which is not already expensed is saved as available allowance.

            Returns:
                expense_pie_chart(dict): what percentage of income each expense uses 
                greatest_expense(str): the expense with the largest proportion of income used, pulled from expense_pie_chart
            Side Effects:
                Modifies the expense_pie_chart dictionary.
        '''
        #proportion_of_income=float
        proportion_total = 0
        previous_proportion = 0
        expense_pie_chart = {} # Dictionary that holds what percentage of income each individual expense detracts from.

        for i in self.expenses: # For every expense, get the proportion of income it represents, and add it to the dict
            proportion_of_income = (self.expenses[i] / self.income) * 100
            proportion_total += proportion_of_income
            expense_pie_chart[f"{i}"] = proportion_of_income
            if proportion_of_income > previous_proportion:
                greatest_expense = f"{i}"
            previous_proportion = proportion_of_income

        if proportion_total < 100: # The difference between the total proportion of expenses and the total income is the proportion of money available to spend.
            free_money_proportion = 100 - proportion_total
            expense_pie_chart["Unspent income"] = free_money_proportion

        if proportion_total > 100: # If all of the expenses are more than their total income, they are spending too much already and have no budget.
            self.over_budget = True

        return expense_pie_chart, greatest_expense


    def hourly_wage(self):
        '''Gets the hourly wage of the user based on the quotient of income by hours worked per week.

            Returns:
                hourly_wage(float): how much the user gets paid per hour
        '''
        hourly_wage = self.income / self.hours_worked # Get the hourly wage of the user
        return hourly_wage


    def daily_budget(self):
        '''If the user is not currently spending more on expenses than they are making, this method calculates
            a daily allowance budget based on the user's income and total expenses.

            Returns:
                daily_allowance(float): the amount of money the user has available to spend freely, per day.
        '''
        if self.over_budget: 
            return "You are currently spending more than your income provides."
        else: # If they aren't over-budget already, divide the monthly free momney into a daily amount (allowance).
            monthly_allowance = self.income - self.total_expenses
            daily_allowance = (monthly_allowance / 30)
        return daily_allowance


    def allowance_goal_difference(self, current_allowance, budget_goal):
        '''Gets the difference between the user's current allowance and their entered goal allowance.

            Args:
                current_allowance(float): the amount of money that is currently free to spend per day
                budget_goal(int): the goal budget, entered by the user
            Returns:
                budget_deficit(float): difference between current allowance and goal allowance.
        '''
        budget_deficit = (budget_goal - current_allowance)
        return budget_deficit


    def suggest_actions(self, deficit_to_goal, greatest_expense, hourly_wage):
        '''Creates a new budget plan for the user, and tells them how many hours they would need to work additionally to make their budget. 
            For the new budget plan, it takes the origianl expenses dictionary and reduces the amount spent on each item by 5% until the goal
            daily budget is met, with the exception of the greatest expense, which is reduced by 10% per iteration.

            Args:
                deficit_to_goal(float): the difference between the current allowance and target allowance.
                greatest_expense(str): key of the biggest expense in the expense_pie_chart dictionary
                hourly_wage(float): the hourly wage of the user
            Side Effects:
                Modifies the revised_budget_plan dictionary.
            Returns:
                additional_hours_needed(int): the number of hours (rounded up) that the user must work in order to make up the allowance difference.
                revised_budget_plan(dict): similar to the self.expenses dict, except it's values are reduced to create extra money for the goal allowance.
        '''
        revised_budget_plan = {}
        revised_budget_plan = self.expenses # New dictionary that will hold a budget which meets the goal

        additional_hours_needed = (deficit_to_goal * 7) / hourly_wage

        while deficit_to_goal > 0: # While the budget is still in the red...
            for i in revised_budget_plan: # For every expense, reduce that expense until the budget goal is met
                if i == greatest_expense: # Biggest expense is reduced by 10%, while all others are reduced by 5%
                    expense_reduction_amount = self.expenses[i] * .10
                    revised_budget_plan[i] -= expense_reduction_amount
                    deficit_to_goal -= expense_reduction_amount
                else:
                    expense_reduction_amount = self.expenses[i] * .05
                    revised_budget_plan[i] -= expense_reduction_amount
                    deficit_to_goal -= expense_reduction_amount
                
        return additional_hours_needed, revised_budget_plan


    def display_summary(self, expenses, biggest_expense, allowance, gap_to_goal, extra_hours, spending_plan, goal):
        '''Displays information to the user relating to the program's calulations and conclusions.

            Args:
                expenses(dict): the pie chart dictionary containing expense proportions.
                biggest_expense(str): the largest expense the user is currently paying per month.
                allowance(float): the current allowance based on the entered data.
                gap_to_goal(float): the difference between the current allowance and target allowance.
                extra_hours(int): num of hours the user must work to make up allowance difference.
                spending_plan(dict): the new budgetary plan devised in the previous suggest_actions method.
                goal(int): the target allowance entered by the user.
            
            Returns:
                Several print statements that give budgetary info to the user.
        '''
        print(f"Here is an overview of your current spending: {self.expenses}\n")
        print(f"Your current daily allowance is {allowance}.")
        print(f"Your biggest expense per month is {biggest_expense}, which uses {expenses[biggest_expense]} percent of your income.\n")
        print(f"The difference between your current unspent income and your goal is ${gap_to_goal}. Let's look at how we can reduce this.\n")
        print(f"To increase your income amount to a suffience level for your goal, you would need to work {extra_hours} more hours each week.\n")
        print(f"Here is a suggested spending plan which will reduce your expenses to meet your daily allowance goal of {goal}:\n{spending_plan}\n")
        pass

def main():
    '''Creates an instance of the BudgetCalculator class based on the user-entered information, and calls several methods from this
        class to make budgetary calculations.

        Args:
            income(float): total income entered
            hours(int): number of hours worked in a week
            rent(float): amount going towards living expenses per month
            car(float): car payment per month
            gas(float): gas costs per month
            food(float): food costs per month
            subscriptions(float): monthly total of subscriptions (e.g. Netflix, Disney+)
            goal(int): the daily allowance the user would like to have
    '''
    # income, hours, rent, car, gas, food, subscriptions, savings, goal
    # python3 budget_temporary.py

    income = int(input("Enter your monthly income in $: "))
    hours = int(input("Enter the number of hours worked: "))
    rent = int(input("Enter how much you pay for rent in $: "))
    car = int(input("Enter how much you spend on your car in $: "))
    gas = int(input("Enter how much you pay for gas in $: "))
    food = int(input("Enter how much you spend on food in $: "))
    subscriptions = int(input("Enter how much you spend on subscriptions in $: "))
    savings = int(input("Enter how much you have in your savingsd account in $: "))
    goal = int(input("Enter your goal in $: "))

    # Create an instance of the BudgetCalculator class
    budget = BudgetCalculator(income, hours, rent, car, gas, food, subscriptions, savings, goal)

    # Call methods to input data, calculate budget, and display results
    expense_pie_chart, greatest_expense = budget.expense_proportions()
    hourly_wage = budget.hourly_wage()
    daily_allowance = budget.daily_budget()
    budget_deficit = budget.allowance_goal_difference(daily_allowance, goal)
    extra_hours, spending_reduction_plan = budget.suggest_actions(budget_deficit, greatest_expense, hourly_wage)
    budget.display_summary(expense_pie_chart, greatest_expense, daily_allowance, budget_deficit, extra_hours, spending_reduction_plan, goal)

def parse_args(arglist):
    """Parse command-line arguments.
        Args:
            arglist (list of str): list of arguments from the command line.
        Returns:
            namespace: the parsed arguments, as returned by
            argparse.ArgumentParser.parse_args().
    """
    parser = ArgumentParser()

    #parser.add_argument("income", type=float, help="What is your current income per month?")
    #parser.add_argument("hours", type=int, help="How many hours per week do you work?")
    #parser.add_argument("rent", type=float, help="What is your monthly rent/mortgage payment? (include utilities)")
    #parser.add_argument("car", type=float, help="What is your monthly car payment?")
    #parser.add_argument("gas", type=float, help="Approximately how much per month is spent on gas?")
    #parser.add_argument("food", type=float, help="Approximately how much per week do you spend on food?")
    #parser.add_argument("subscriptions", type=float, help="How much per month is spent on subscription services?")
    #parser.add_argument("savings", type=float, help="How much do you put into savings each month?")
    #parser.add_argument("goal", type=float, help="What is your daily budget goal?")
    
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main()
    # args.income, args.hours, args.rent, args.car, args.gas, args.food, args.subscriptions, args.savings, args.goal
