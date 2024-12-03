import json
from functools import wraps

def validate_json(method):
    """
    Decorator to validate JSON data before performing operations.
    Ensures that the file contains a valid structure.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        data = self._load_json()
        if not isinstance(data, dict):
            raise ValueError("JSON data must be a dictionary.")
        for key in ["connections", "scraped_texts", "persons"]:
            if key not in data:
                data[key] = []
        self._save_json(data)
        return method(self, *args, **kwargs)
    return wrapper

class FileManager:
    def __init__(self, file_path: str):
        """
        Initializes the FileManager with the path to the JSON file.
        :param file_path: Path to the JSON file.
        """
        self.file_path = file_path

    def _load_json(self):
        """
        Loads and returns the JSON data from the file.
        :return: JSON data as a dictionary.
        """
        try:
            with open(self.file_path, "r", encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"connections": [], "scraped_texts": [], "persons": []}
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in the file.")

    def _save_json(self, data: dict) -> None:
        """
        Saves the JSON data to the file.
        :param data: Dictionary to save as JSON.
        """
        with open(self.file_path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @validate_json
    def connection_exists(self, profile: str) -> bool:
        """
        Checks if a connection already exists in either 'connections' or 'scraped_texts'.
        :param profile: Profile identifier to check.
        :return: True if the profile exists, False otherwise.
        """
        data = self._load_json()
        connections = data.get("connections", [])
        scraped_texts = data.get("scraped_texts", [])

        return any(conn["profile"] == profile for conn in connections) or \
               any(scraped["profile"] == profile for scraped in scraped_texts)

    @validate_json
    def add_connections(self, new_connections: list) -> None:
        """
        Adds new connections to the 'connections' list if they are not duplicates.
        :param new_connections: List of connection dictionaries to add.
        """
        data = self._load_json()
        existing_profiles = {conn for conn in data.get("connections", [])}
        scraped_profiles = {scraped for scraped in data.get("scraped_texts", [])}

        filtered_connections = [conn for conn in new_connections
                                if conn not in existing_profiles and
                                conn not in scraped_profiles]

        data["connections"].extend(filtered_connections)
        self._save_json(data)

    @validate_json
    def get_next_connection(self) -> dict:
        """
        Retrieves and removes the first connection from the 'connections' list.
        Moves it to 'scraped_texts' after retrieval.
        :return: The first connection dictionary or None if no connections exist.
        """
        data = self._load_json()
        if not data.get("connections"):
            return None

        next_connection = data["connections"].pop(0)
        data.setdefault("scraped_texts", []).append(next_connection)
        self._save_json(data)

        return next_connection

    @validate_json
    def add_person(self, person_data: dict) -> None:
        """
        Adds a person's data to the 'persons' list.
        :param person_data: Dictionary containing the person's data.
        """
        if not isinstance(person_data, dict):
            raise ValueError("Person data must be a dictionary.")

        data = self._load_json()
        if not any(person["profile"] == person_data["profile"] for person in data.get("persons", [])):
            data.setdefault("persons", []).append(person_data)
            self._save_json(data)

    @validate_json
    def get_all_persons(self) -> list:
        """
        Retrieves all persons stored in the JSON file.
        :return: List of persons.
        """
        data = self._load_json()
        return data.get("persons", [])
    
    @validate_json
    def get_connections(self) -> list:
        """
        Retrieves all connections stored in the JSON file.
        :return: List of connections.
        """
        data = self._load_json()
        return data.get("connections", [])
    
    @validate_json
    def remove_connection(self, connection) -> None:
        """
        Removes a connection from the 'connections' list and adds it to 'scraped_texts'.
        :param connection: Connection dictionary to remove.
        """
        data = self._load_json()
        connections = data.get("connections", [])
        scraped_texts = data.get("scraped_texts", [])

        if connection in connections:
            connections.remove(connection)
            scraped_texts.append(connection)

        self._save_json(data)