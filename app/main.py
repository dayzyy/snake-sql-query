from file_handlers.file_handlers import TextFileReader 
from deserializers.factory import DeserializerFactory
from cli.parse_arguments import parse_arguments

def process_data(students_file: str, rooms_file: str, format: str):
    students_data = TextFileReader.read(students_file)
    rooms_data = TextFileReader.read(rooms_file)

    deserializer = DeserializerFactory.get_deserializer(format)

    students = deserializer.deserialize(students_data)
    rooms = deserializer.deserialize(rooms_data)

    return students, rooms

def main():
    args = parse_arguments()
    students, rooms = process_data(args.students_file, args.rooms_file, args.format)

if __name__ == "__main__":
    main()
