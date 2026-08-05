from enum import Enum

class PaymentMethod(str, Enum):
    CASH = 'CASH'
    UPI = 'UPI'
    CREDIT_CARD = 'CREDIT_CARD'
    DEBIT_CARD = 'DEBIT_CARD'
    NET_BANKING = 'NET_BANKING'


class ExpenseCategory(str, Enum):
    FOOD = 'FOOD'
    TRAVEL = 'TRAVEL'
    SHOPPING = 'SHOPPING'
    HEALTH = 'HEALTH'
    EDUCATION = 'EDUCATION'
    BILLS = 'BILLS'
    ENTERTAINMENT = 'ENTERTAINMENT'
    OTHER = 'OTHER'