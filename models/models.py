from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExpenseCategory(models.Model):
    """General Expense Category"""
    _name = 'easy_expenses.category'
    _description = 'Global Expense Category'
    _order = 'name'

    name = fields.Char(string="Category Name", required=True, unique=True)
    description = fields.Text(string="Description")
    expense_ids = fields.One2many('easy_expenses.expense', 'category_id', string="Expenses")

    @api.model
    def create_default_categories(self):
        """Create default categories with an 'Others' option"""
        default_categories = [
            {'name': 'Food', 'description': 'All expenses related to meals and beverages'},
            {'name': 'Transportation', 'description': 'Expenses for commuting and travel'},
            {'name': 'Home', 'description': 'Household expenses including rent and utilities'},
            {'name': 'Entertainment', 'description': 'Leisure and recreational activities'},
            {'name': 'Health', 'description': 'Medical expenses and wellness'},
            {'name': 'Finance', 'description': 'Savings, insurance, and loan payments'},
            {'name': 'Education', 'description': 'School fees, courses, and training'},
            {'name': 'Shopping', 'description': 'Personal shopping, clothing, and accessories'},
            {'name': 'Technology', 'description': 'Electronics, software, and online services'},
            {'name': 'Travel', 'description': 'Hotels, flights, and vacations'},
            {'name': 'Others', 'description': 'Expenses in a non-registered category'},
        ]

        for category in default_categories:
            existing_category = self.search([('name', '=', category['name'])], limit=1)
            if not existing_category:
                self.create(category)


class Expense(models.Model):
    """Predefined Expenses"""
    _name = 'easy_expenses.expense'
    _description = 'Global Predefined Expense'
    _order = 'name'

    name = fields.Char(string="Expense Name", required=True)
    category_id = fields.Many2one('easy_expenses.category', string="Category", required=True)

    @api.model
    def create_default_expenses(self):
        """Create default expenses with 'Others' for each category"""
        default_expenses = [
            # Food Expenses
            {'name': 'Supermarket Purchase', 'category_name': 'Food'},
            {'name': 'Restaurant Dine-In', 'category_name': 'Food'},
            {'name': 'Fast Food Takeout', 'category_name': 'Food'},
            {'name': 'Bakery Items', 'category_name': 'Food'},
            {'name': 'Coffee Purchase', 'category_name': 'Food'},
            {'name': 'Alcoholic Beverages', 'category_name': 'Food'},
            {'name': 'Catering Services', 'category_name': 'Food'},
            {'name': 'Meal Kit Subscription', 'category_name': 'Food'},
            {'name': 'Street Food', 'category_name': 'Food'},
            {'name': 'Others', 'category_name': 'Food'},

            # Transportation Expenses
            {'name': 'Gasoline Refill', 'category_name': 'Transportation'},
            {'name': 'Public Bus Ticket', 'category_name': 'Transportation'},
            {'name': 'Train Ticket', 'category_name': 'Transportation'},
            {'name': 'Uber/Lyft Ride', 'category_name': 'Transportation'},
            {'name': 'Taxi Fare', 'category_name': 'Transportation'},
            {'name': 'Car Rental', 'category_name': 'Transportation'},
            {'name': 'Bike Rental', 'category_name': 'Transportation'},
            {'name': 'Toll Charges', 'category_name': 'Transportation'},
            {'name': 'Parking Fees', 'category_name': 'Transportation'},
            {'name': 'Car Fixes', 'category_name': 'Transportation'},
            {'name': 'Flights', 'category_name': 'Transportation'},
            {'name': 'Others', 'category_name': 'Transportation'},

            # Home Expenses
            {'name': 'Rent Payment', 'category_name': 'Home'},
            {'name': 'Mortgage Payment', 'category_name': 'Home'},
            {'name': 'Electricity Bill', 'category_name': 'Home'},
            {'name': 'Water Bill', 'category_name': 'Home'},
            {'name': 'Gas Bill', 'category_name': 'Home'},
            {'name': 'Internet Bill', 'category_name': 'Home'},
            {'name': 'Home Insurance', 'category_name': 'Home'},
            {'name': 'Home Maintenance', 'category_name': 'Home'},
            {'name': 'Security System Subscription', 'category_name': 'Home'},
            {'name': 'Others', 'category_name': 'Home'},

            # Entertainment Expenses
            {'name': 'Movie Ticket', 'category_name': 'Entertainment'},
            {'name': 'Concert Ticket', 'category_name': 'Entertainment'},
            {'name': 'Gaming Subscription', 'category_name': 'Entertainment'},
            {'name': 'Streaming Service Subscription', 'category_name': 'Entertainment'},
            {'name': 'Theme Park Entry', 'category_name': 'Entertainment'},
            {'name': 'Gym Membership', 'category_name': 'Entertainment'},
            {'name': 'Club Membership Fee', 'category_name': 'Entertainment'},
            {'name': 'Bowling Alley Visit', 'category_name': 'Entertainment'},
            {'name': 'Sports Event Ticket', 'category_name': 'Entertainment'},
            {'name': 'Party', 'category_name': 'Entertainment'},
            {'name': 'Others', 'category_name': 'Entertainment'},
            
            # Health Expenses
            {'name': 'Doctor Consultation', 'category_name': 'Health'},
            {'name': 'Dentist Visit', 'category_name': 'Health'},
            {'name': 'Prescription Medications', 'category_name': 'Health'},
            {'name': 'Vitamins & Supplements', 'category_name': 'Health'},
            {'name': 'Medical Insurance', 'category_name': 'Health'},
            {'name': 'Mental Health Therapy', 'category_name': 'Health'},
            {'name': 'Weight Loss Program', 'category_name': 'Health'},
            {'name': 'Eye Exam & Glasses', 'category_name': 'Health'},
            {'name': 'Hearing Aid Purchase', 'category_name': 'Health'},
            {'name': 'Others', 'category_name': 'Health'},

            # Finance Expenses
            {'name': 'Savings Contribution', 'category_name': 'Finance'},
            {'name': 'Loan Repayment', 'category_name': 'Finance'},
            {'name': 'Credit Card Payment', 'category_name': 'Finance'},
            {'name': 'Investment Purchase', 'category_name': 'Finance'},
            {'name': 'Stock Trading Fees', 'category_name': 'Finance'},
            {'name': 'Insurance Premium', 'category_name': 'Finance'},
            {'name': 'Emergency Fund Contribution', 'category_name': 'Finance'},
            {'name': 'Retirement Savings', 'category_name': 'Finance'},
            {'name': 'Debt Consolidation Payment', 'category_name': 'Finance'},
            {'name': 'Advices', 'category_name': 'Finance'},
            {'name': 'Others', 'category_name': 'Finance'},

            # Education Expenses
            {'name': 'School Fees', 'category_name': 'Education'},
            {'name': 'College Tuition', 'category_name': 'Education'},
            {'name': 'Online Course Enrollment', 'category_name': 'Education'},
            {'name': 'Books & Study Materials', 'category_name': 'Education'},
            {'name': 'Educational Software', 'category_name': 'Education'},
            {'name': 'Private Tutor Fees', 'category_name': 'Education'},
            {'name': 'Exam Registration Fees', 'category_name': 'Education'},
            {'name': 'School Bus Fees', 'category_name': 'Education'},
            {'name': 'Educational Field Trips', 'category_name': 'Education'},
            {'name': 'Others', 'category_name': 'Education'},

            # Shopping Expenses
            {'name': 'Clothing Purchase', 'category_name': 'Shopping'},
            {'name': 'Shoes Purchase', 'category_name': 'Shopping'},
            {'name': 'Accessories Purchase', 'category_name': 'Shopping'},
            {'name': 'Electronics Purchase', 'category_name': 'Shopping'},
            {'name': 'Makeup & Beauty Products', 'category_name': 'Shopping'},
            {'name': 'Home & Furniture Purchase', 'category_name': 'Shopping'},
            {'name': 'Gift Shopping', 'category_name': 'Shopping'},
            {'name': 'Luxury Items', 'category_name': 'Shopping'},
            {'name': 'Grocery Shopping', 'category_name': 'Shopping'},
            {'name': 'Others', 'category_name': 'Shopping'},

            # Technology Expenses
            {'name': 'Software Subscription', 'category_name': 'Technology'},
            {'name': 'Online Service Subscription', 'category_name': 'Technology'},
            {'name': 'Cloud Storage Plan', 'category_name': 'Technology'},
            {'name': 'Mobile App Purchase', 'category_name': 'Technology'},
            {'name': 'Hardware Purchase', 'category_name': 'Technology'},
            {'name': 'Gadget & Device Purchase', 'category_name': 'Technology'},
            {'name': 'Tech Support Service', 'category_name': 'Technology'},
            {'name': 'Digital Content Purchase', 'category_name': 'Technology'},
            {'name': 'Others', 'category_name': 'Technology'},

            # Travel Expenses
            {'name': 'Flight Ticket', 'category_name': 'Travel'},
            {'name': 'Hotel Booking', 'category_name': 'Travel'},
            {'name': 'Vacation Package', 'category_name': 'Travel'},
            {'name': 'Tour & Sightseeing', 'category_name': 'Travel'},
            {'name': 'Car Rental for Trip', 'category_name': 'Travel'},
            {'name': 'Travel Insurance', 'category_name': 'Travel'},
            {'name': 'Local Transport in Destination', 'category_name': 'Travel'},
            {'name': 'Cruise Trip', 'category_name': 'Travel'},
            {'name': 'Souvenirs & Travel Shopping', 'category_name': 'Travel'},
            {'name': 'Others', 'category_name': 'Travel'},
            
            # Others category default expense
            {'name': 'Others', 'category_name': 'Others'},
        ]

        for expense in default_expenses:
            category = self.env['easy_expenses.category'].search([('name', '=', expense['category_name'])], limit=1)
            if category and not self.search([('name', '=', expense['name'])]):
                self.create({'name': expense['name'], 'category_id': category.id})


class UserExpenseCategory(models.Model):
    """User-Created Expense Categories"""
    _name = 'easy_expenses.user_category'
    _description = 'User Custom Expense Category'

    name = fields.Char(string="Category Name", required=True)
    user_id = fields.Many2one('res.users', string="User", required=True, default=lambda self: self.env.user)


class UserExpense(models.Model):
    """User-Created Expenses"""
    _name = 'easy_expenses.user_expense'
    _description = 'User Custom Expense'

    name = fields.Char(string="Expense Name", required=True)
    category_id = fields.Many2one('easy_expenses.user_category', string="Category", required=True)
    user_id = fields.Many2one('res.users', string="User", required=True, default=lambda self: self.env.user)


class ExpenseRecord(models.Model):
    """Records of actual expenses"""
    _name = 'easy_expenses.record'
    _description = 'Expense Record'
    _order = 'date desc'

    expense_id = fields.Many2one('easy_expenses.expense', string="Global Expense")
    user_expense_id = fields.Many2one('easy_expenses.user_expense', string="Custom Expense")
    amount = fields.Float(string="Amount", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    note = fields.Text(string="Note", help="Optional notes about the expense")
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, required=True)

    @api.constrains('amount')
    def _check_amount(self):
        """Ensure amount is positive"""
        for record in self:
            if record.amount <= 0:
                raise ValidationError("The expense amount must be greater than zero.")
