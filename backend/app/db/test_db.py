from app.db.database import engine
from sqlmodel import Session, text

def test_connection():
    with Session(engine) as session:
        result = session.exec(text("SELECT 1")).first()
        print("DB Connected:", result)

if __name__ == "__main__":
    test_connection()