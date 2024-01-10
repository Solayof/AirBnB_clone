#!/usr/bin/python3
"""FileStorage class
"""

import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """This class serializes instances to a JSON file
    and deserializes JSON files to instances
    """
    __file_path = "file.json"
    __objects = {}

    # __objects = {class.id : "address of BaseModel Instance"}

    def all(self):
        """Returns the dictionary `__objects`

        Returns:
            dict: A dictionary of all objects
        """
        return self.__objects

    def new(self, obj):
        """Updates the dictionary objects with a new object

        Args:
            obj: The new object to be added
        """
        # Construct key
        key = "{}.{}".format(obj.__class__.__name__, obj.id)

        # Assign Value to key
        self.__objects[key] = obj

    def save(self):
        """Serializes `__objects` to a JSON file(__file_path)
        """
        new_dict = {}
        for key, obj in self.__objects.items():
            new_dict[key] = obj.to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(new_dict, file)

    def reload(self):
        """Deserializes the JSON file (__file_path) to update the objects.
        If the JSON file (__file_path) doesn't exist, it does nothing
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                load_obj = json.load(file)
                for key, value in load_obj.items():
                    class_name, obj_id = key.split(".")
                    self.__objects[key] = globals()[class_name](**value)
        except FileNotFoundError:
            pass

    def all_classes(self):
        """Returns a dictionary of all available classes

        Returns:
            dict: Dictionary of all available classes
        """
        return {
            "BaseModel" : BaseModel,
            "User" : User
        }

    def create_instance(self, class_name):
        """Creates a new instance of the specified class and
        adds it to the dictionary.

        Args:
            class_name (str): The class name

        Returns:
            class: A new instance of the class
        """
        # create new instance of the class
        new_instance = globals()[class_name]()
        # Construct key
        key = "{}.{}".format(class_name, new_instance.id)
        # Assign Value to key
        self.__objects[key] = new_instance

        return new_instance
