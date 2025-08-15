from file_handlers.file_handlers import TextFileReader 
from deserializers.factory import DeserializerFactory
from db.db import Database
from db.custom_queries import run_queries, create_indexes
from models.custom_models import Student, Room
import os

def process_data():
    students_data = TextFileReader.read('./data/students.json')
    rooms_data = TextFileReader.read('./data/rooms.json')

    deserializer = DeserializerFactory.get_deserializer('json')

    students = deserializer.deserialize(students_data)
    rooms = deserializer.deserialize(rooms_data)

    return students, rooms

def setup_db():
    Database.init_pool(
        host='db',
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        database=os.environ.get('MYSQL_DATABASE'),
    )

def main():
    students, rooms = process_data()

    setup_db()

    Student.manager.drop()
    Room.manager.drop()

    models = (Room, Student)

    for model in models:
        model.manager.create()

    print("INSERTING ROWS")
    for model, data in zip(models, (rooms, students)):
        rows = (model(**row) for row in data)
        model.manager.add_bulk(rows)

    print("CREATING INDEXES")
    create_indexes()

    print("EXECUTING QUERIES")
    run_queries()

if __name__ == "__main__":
    main()
