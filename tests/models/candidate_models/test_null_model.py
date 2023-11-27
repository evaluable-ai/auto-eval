import json
import unittest
from unittest.mock import Mock, patch

from evaluableai.models.candidate_models.null_model import NullModel


class TestNullModel(unittest.TestCase):

    def setUp(self):
        self.model_name = "empty_model"
        self.model_version = "user_defined_version_1"
        self.null_model = NullModel(self.model_name, self.model_version)

    def test_init(self):
        # Test initialization
        self.assertEqual(self.null_model.model_name, self.model_name)
        self.assertEqual(self.null_model.model_version, self.model_version)

    @patch('evaluableai.data_model.input_row_object.InputRow')
    @patch('evaluableai.data_model.model_response_object.ModelResponseObject')
    def test_from_json_array(self, mock_model_response_object, mock_input_row):
        # Test the from_json_array class method
        json_array = [
            json.dumps({"input": "test input", "context": "test context", "responses": ["response 1", "response 2"]})
        ]

        mock_input_row.return_value = Mock()
        mock_model_response_object.return_value = Mock()

        response_objects = NullModel.from_json_array(json_array)

        self.assertEqual(len(response_objects), 2)

    def test_parse_json_with_valid_string(self):
        # Test the parse_json static method with a valid JSON string
        json_string = json.dumps({"key": "value"})
        result = NullModel.parse_json(json_string)
        self.assertEqual(result, {"key": "value"})

    def test_parse_json_with_invalid_string(self):
        # Test the parse_json static method with an invalid JSON string
        with self.assertLogs(level='ERROR'):
            result = NullModel.parse_json("invalid json")
            self.assertIsNone(result)

    def test_parse_json_with_dict(self):
        # Test the parse_json static method with a dictionary
        dictionary = {"key": "value"}
        result = NullModel.parse_json(dictionary)
        self.assertEqual(result, dictionary)


if __name__ == '__main__':
    unittest.main()
