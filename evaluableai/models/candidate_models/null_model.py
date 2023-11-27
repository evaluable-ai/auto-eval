import json
import logging
import uuid

from evaluableai.data_model.input_row_object import InputRow
from evaluableai.data_model.model_response_object import ModelResponseObject


# Make sure to import InputRow if it's a separate class

class NullModel:
    def __init__(self, model_name, model_version):
        self._model_name = model_name
        self._model_version = model_version

    @property
    def model_name(self):
        return self._model_name

    @property
    def model_version(self):
        return self._model_version

    @classmethod
    def from_json_array(cls, json_array):
        data_array = [cls.parse_json(item) for item in json_array]
        response_objects = []

        for data in data_array:
            input_text = data.get('input', '')
            context = data.get('context', '')
            input_row = InputRow(input_text, context)  # Assuming InputRow is imported

            model_counter = 1
            for response in data.get('responses', []):
                response_id = uuid.uuid4()
                model = cls('empty_model', f'user_defined_version_{model_counter}')
                model_counter += 1
                response_object = ModelResponseObject(response_id,
                                                      response,
                                                      input_row,
                                                      model)
                response_objects.append(response_object)
        return response_objects

    @staticmethod
    def parse_json(item):
        if isinstance(item, str):
            try:
                return json.loads(item)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON: {item}")
                return None
        elif isinstance(item, (dict, list)):
            return item
        else:
            logging.error(f"Unsupported type: {type(item).__name__}")
            return None
