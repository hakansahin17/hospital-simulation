from .database import engine, Base, SessionLocal
from .models import Resource
from config import Config


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    db.query(Resource).delete()

    for resource in Config.INITIAL_RESOURCES:
        db.add(Resource(**resource))

    db.commit()
    db.close()
