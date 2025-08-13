from typing import List
from file_handlers.file_handlers import TextFileReader 
from deserializers.factory import DeserializerFactory

def get_data():
    students_file = '~/path/to/students.json'
    rooms_file = '~/path/to/rooms.json'
    format = students_file.split('.')[-1]

    students_data = TextFileReader.read(students_file)
    rooms_data = TextFileReader.read(rooms_file)

    deserializer = DeserializerFactory.get_deserializer(format)

    students = deserializer.deserialize(students_data)
    rooms = deserializer.deserialize(rooms_data)

    other_logic(students, rooms)

def other_logic(students: List, rooms: List):
    pass

def main():
    print("Hello from app!")


if __name__ == "__main__":
    main()
