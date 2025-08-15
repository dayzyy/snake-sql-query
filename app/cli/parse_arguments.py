import argparse
from deserializers.factory import DeserializerFactory

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process student and room data files."
    )
    
    parser.add_argument(
        "-sf",
        "--students-file",
        required=True,
        help="Path to the students file"
    )
    
    parser.add_argument(
        "-rf",
        "--rooms-file",
        required=True,
        help="Path to the rooms file"
    )

    parser.add_argument(
        "-fmt",
        "--file-format",
        required=True,
        choices=[format for format in DeserializerFactory.DESERIALIZERS.keys()],
        help="Path to the rooms file"
    )
    
    return parser.parse_args()
