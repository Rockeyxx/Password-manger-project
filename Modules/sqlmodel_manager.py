from sqlmodel import Session, SQLModel, create_engine, select , Column
from sqlalchemy import create_engine , column
from typing import Optional, Type

from sqlmodel import SQLModel, Field

class Users(SQLModel, table=True):
    username: str = Field(SQLModel, primary_key=True)
    password: str

class Catagory(SQLModel, table=True):
    username_key: str = Field(foreign_key="users.username" , primary_key=True)
    catagory: str = Field(primary_key=True)

class Table_widget(SQLModel, table = True):
    ID:Optional[int]= Field(primary_key=True )
    username_key: str = Field(foreign_key="users.username")
    catagory:str = Field(foreign_key="catagory.catagory")
    tag_Label:str 
    username:str 
    password:str
    URL:str
    note:str 
    privet_note:str


class SqlModelManager:
    def __init__(self) -> None:
        self.engine = create_engine(f"sqlite:///DATABASE.db")
        self.create_database()

    def create_database(self):
        SQLModel.metadata.create_all(self.engine)

    def add_item(self, class_table, **item_data):
        session = Session(self.engine)
        item = class_table(**item_data)
        session.add(item)
        session.commit()
        session.close()

    def read(self, class_table) -> list:
        session = Session(self.engine)
        return session.exec(select(class_table)).all()

    def delete_item(self, class_table, **filters):
        session = Session(self.engine)
        item = session.exec(select(class_table).filter_by(**filters)).first()
        if item:
            session.delete(item)
            session.commit()
            session.close()

    def update_item(self, class_table, filters: dict, update_data: dict):
        session = Session(self.engine)
        item = session.exec(select(class_table).filter_by(**filters)).first()
        if item is not None:
            for key, value in update_data.items():
                setattr(item, key, value)
            session.commit()
            session.close()
            
if __name__=="__main__":
# Example usage:
    manager = SqlModelManager()
    manager.add_item(Catagory, username_key="omar", catagory="after")

    # #Read
    # all_users = manager.read(Users)
    # print(all_users)

    # # Delete
    # manager.delete_item(Users, username="omar")

    # # Update
    # manager.update_item(Users, {"username": "omar"}, {"password": "new_password"})
    username1 = "omar"

    manager.update_item(Catagory ,{"username_key": f"{username1}" , "catagory": f"after"}, {"catagory": f"changed"})
