from sqlmodel import SQLModel, Field
from datetime import datetime, date

class ExpenseTracker(SQLModel, table=True):
    '''Expense Tracker'''

    id : int | None = Field(default=None, description='The ID of the transaction', primary_key=True)
    title : str = Field(min_length=1, description='The title of the transaction')
    amount : float = Field(ge=0, description='The amount of the transaction')
    category : str = Field(min_length=1, description='The category of the transaction')
    payment_method : str = Field(min_length=1, description='Method by which payment was done')
    expense_date: date = Field(default_factory=date.today)
    description : str = Field(min_length=1, description='Describe the payment transaction')
    created_at : datetime = Field(default_factory=datetime.now)

class ExpenseTrackerCreate(SQLModel):
    '''Create Expense Tracker'''

    title: str = Field(min_length=1)
    amount: float = Field(ge=0)
    category: str
    payment_method: str
    expense_date: date
    description: str

class ExpenseTrackerRead(SQLModel):
    '''Read Expense Tracker'''

    id : int 
    title: str
    amount: float
    category: str
    payment_method: str
    expense_date: date
    description: str
    created_at: datetime

class ExpenseTrackerList(SQLModel):
    '''Read the list of expenses'''

    count: int 
    transactions: list[ExpenseTrackerRead]
    message: str = "Expense Retrieved Successfully"


class ExpenseTrackerUpdate(SQLModel):
    '''Update the expense transactions'''

    title: str
    amount: float
    category: str
    payment_method: str
    expense_date: date
    description: str

class ExpenseTrackerAnalysis(SQLModel):
    '''Analyze all the expense transactions'''

    total_transactions: int = Field(ge=0, description='Total number of transactions occured')
    total_expense: int = Field(ge=0, description='Total amount of expense transaction')
    average_expense: int = Field(ge=0, description='The average of all the expense transactions dont till now')
    highest_expense: int = Field(ge=0, description='Highest expense among all expense transactions')