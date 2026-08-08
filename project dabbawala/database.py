from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL = 'sqlite:///dabbawala.db'

engine = create_engine(DATABASE_URL, echo=True)

def create_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session