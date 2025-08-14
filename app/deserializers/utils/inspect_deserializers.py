from deserializers.deserializers import BaseDeserializer

def extract_format_from_deserializer(cls: type[BaseDeserializer]) -> str:
    name = cls.__name__
    if name.endswith("Deserializer"):
        return name[:-len("Deserializer")].lower()
    else:
        raise ValueError(
            "Deserializer class name must end with 'Deserializer'"
            "e.g: JSONDeserializer, XMLDeserializer, CSVDeserializer"
        )
