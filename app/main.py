from file_handlers.file_handlers import TextFileReader 
from deserializers.factory import DeserializerFactory
from cli.parse_arguments import parse_arguments
from db.db import Database
from models.custom_models import Student, Room
import os

def process_data(students_file: str, rooms_file: str, format: str):
    students_data = TextFileReader.read(students_file)
    rooms_data = TextFileReader.read(rooms_file)

    deserializer = DeserializerFactory.get_deserializer(format)

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
    # args = parse_arguments()
    # students, rooms = process_data(args.students_file, args.rooms_file, args.format)

    setup_db()

    Student.manager.create()
    Room.manager.create()

if __name__ == "__main__":
    main()
