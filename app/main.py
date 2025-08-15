from file_handlers.file_handlers import TextFileReader 
from deserializers.factory import DeserializerFactory
from cli.parse_arguments import parse_arguments
from db.db import Database
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

    models = (Room, Student)

    # Create tables
    for model in models:
        model.manager.create()

    # Insert rows
    for model, data in zip(models, (students, rooms)):
        for row in data:
            model.manager.add(model(**row))

if __name__ == "__main__":
    main()
