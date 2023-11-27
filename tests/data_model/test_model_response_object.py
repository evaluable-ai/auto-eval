import unittest
from unittest.mock import Mock

from evaluableai.data_model.model_response_object import ModelResponseObject  # Replace with the actual import path


class TestModelResponseObject(unittest.TestCase):

    def setUp(self):
        # Mock dependencies
        self.mock_input_row = Mock()
        self.mock_model = Mock()
        self.mock_model.model_name = "TestModel"
        self.mock_model.model_version = "1.0"

        # Mock attributes of input_row
        self.mock_input_row.input_text = "Sample input text"
        self.mock_input_row.context = "Sample context"
        self.mock_input_row.input_id = "12345"

        # Create an instance of ModelResponseObject
        self.response_id = "response_id_123"
        self.response_text = "Sample response"
        self.model_response_obj = ModelResponseObject(self.response_id, self.response_text, self.mock_input_row,
                                                      self.mock_model)

    def test_init(self):
        # Test initialization
        self.assertEqual(self.model_response_obj._response_id, self.response_id)
        self.assertEqual(self.model_response_obj._response_text, self.response_text)
        self.assertIs(self.model_response_obj._input_row, self.mock_input_row)
        self.assertIs(self.model_response_obj._model, self.mock_model)

    def test_response_text_property(self):
        # Test the response_text property
        self.assertEqual(self.model_response_obj.response_text, self.response_text)

    def test_get_candidate_model_name(self):
        # Test the get_candidate_model_name method
        self.assertEqual(self.model_response_obj.get_candidate_model_name(), "TestModel")

    def test_get_candidate_model_version(self):
        # Test the get_candidate_model_version method
        self.assertEqual(self.model_response_obj.get_candidate_model_version(), "1.0")

    def test_get_input_text(self):
        # Test the get_input_text method
        self.assertEqual(self.model_response_obj.get_input_text(), "Sample input text")

    def test_to_dict(self):
        # Test the to_dict method
        self.mock_input_row.to_dict.return_value = {'input_text': 'Sample input text', 'context': 'Sample context',
                                                    'input_id': '12345'}
        result = self.model_response_obj.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['response_id'], self.response_id)
        self.assertEqual(result['response_text'], self.response_text)
        self.assertEqual(result['input_row'], self.mock_input_row.to_dict())
        self.assertEqual(result['model_name'], "TestModel")
        self.assertEqual(result['model_version'], "1.0")


if __name__ == '__main__':
    unittest.main()
