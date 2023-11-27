import unittest
from unittest.mock import Mock

from evaluableai.data_model.evaluation_object import EvaluationObject


class TestEvaluationObject(unittest.TestCase):

    def setUp(self):
        # Mocking model response objects
        self.mock_model_response_objects = [Mock(), Mock()]
        for mock_response in self.mock_model_response_objects:
            mock_response.to_dict.return_value = {'mock_key': 'mock_value'}

        # Create an instance of EvaluationObject
        self.evaluation_object = EvaluationObject(self.mock_model_response_objects)

    def test_init(self):
        # Test initialization
        self.assertEqual(self.evaluation_object.candidate_model_response_objects, self.mock_model_response_objects)
        self.assertIsNone(self.evaluation_object.scores)
        self.assertIsNone(self.evaluation_object.evaluating_model_name)
        self.assertIsNone(self.evaluation_object.evaluating_model_version)

    def test_to_dict(self):
        # Test the to_dict method
        result = self.evaluation_object.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result['model_responses']), len(self.mock_model_response_objects))
        for response in result['model_responses']:
            self.assertEqual(response, {'mock_key': 'mock_value'})


if __name__ == '__main__':
    unittest.main()
