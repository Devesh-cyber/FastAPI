from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = 'sqlite:///expense.db'

engine = create_engine(DATABASE_URL)

def create_table():
    ''' Create all tables defined by SQLModel class '''
    
    SQLModel.metadata.create_all(engine)

def get_session():
    '''Dependency that provides a database per session'''

    with Session(engine) as session:
        yield session