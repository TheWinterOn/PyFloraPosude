import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


db_engine = db.create_engine("sqlite:///user_database/user_database.db")
Base.metadata.create_all(bind=db_engine)


# CRUD User
def db_add_user(name, surname, username, password):
    with Session(bind=db_engine) as session:
        user_exists = (
            session.query(User).filter(User.username == username).one_or_none()
        )

        if user_exists:
            return

        user = User(name=name, surname=surname, username=username, password=password)
        session.add(user)
        session.commit()


def db_get_users():
    with Session(bind=db_engine) as session:
        users = session.query(User).all()
        return users


def db_update_user(name, surname, username, password):  # TODO preko user varijable
    with Session(bind=db_engine) as session:
        current_user = session.query(User).filter(User.username == username)
        current_user.update(
            values={
                "name": name,
                "surname": surname,
                "username": username,
                "password": password,
            }
        )
        session.commit()
        print(current_user)


def db_delete_user(user_id):
    with Session(bind=db_engine) as session:
        user = session.query(User).filter(User.id == user_id).one_or_none()

        if user:
            session.delete(user)
            session.commit()
        else:
            print("No such user!")  # TODO write message in gui that user doesn't exist


# Login
def db_login(username, password):
    with Session(db_engine) as session:
        user = (
            session.query(User)
            .filter(User.username == username, User.password == password)
            .one_or_none()
        )

        return user


# db_add_user(
#     name="Daniel",
#     surname="Zima",
#     username="admin",
#     password="admin",
# )

# db_update_user(
#     name="Daniel",
#     surname="Zima",
#     username="admin",
#     password="admin",
# )


# korisnici = db_get_users()
# for item in korisnici:
#     print(item.name, item.surname, item.username)
