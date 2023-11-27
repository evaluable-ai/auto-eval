import unittest
from unittest.mock import Mock, patch

from evaluableai.data_model.input_row_object import InputRow
from evaluableai.data_model.model_response_object import ModelResponseObject
from evaluableai.models.candidate_models.candidate_model import CandidateModel
from evaluableai.models.candidate_models.candidate_model_names import CandidateModelName


class TestCandidateModel(unittest.TestCase):

    @patch('os.getenv')
    def setUp(self, mock_getenv):
        # Mock environment variable for API key
        mock_getenv.return_value = 'test_api_key'

        # Mock parameters
        self.model_name = CandidateModelName.OPEN_AI
        self.model_version = 'gpt-3'
        self.api_key_env = 'TEST_API_KEY_ENV'

        # Create an instance of CandidateModel
        self.candidate_model = CandidateModel(self.model_name, self.model_version, api_key_env=self.api_key_env)

    def test_init_with_valid_model(self):
        # Test initialization with a valid model name
        self.assertEqual(self.candidate_model.model_name, self.model_name)
        self.assertEqual(self.candidate_model.model_version, self.model_version)

    def test_init_with_custom_model_without_auth_token(self):
        # Test initialization with a custom model without providing API auth token
        with self.assertRaises(ValueError):
            CandidateModel(CandidateModelName.CUSTOM, 'custom_version', api_auth_token=None)

    @patch('os.getenv', return_value=None)
    def test_init_with_missing_api_key(self, mock_getenv):
        # Test initialization with a missing API key
        with self.assertRaises(EnvironmentError):
            CandidateModel(self.model_name, self.model_version, api_key_env='MISSING_ENV')

    @patch('evaluableai.models.candidate_models.candidate_model.CandidateModel._create_instance')
    def test_generate_response(self, mock_create_instance):
        mock_model_instance = Mock()
        mock_create_instance.return_value = mock_model_instance

        # Create a mock response object
        mock_response = ModelResponseObject("response_id", "response_text", InputRow('input', 'testing'), "model")
        mock_model_instance.generate_response.return_value = mock_response

        test_input_row = InputRow('input', 'testing')
        response = self.candidate_model.generate_response(test_input_row)
        text = response.get_input_text()
        self.assertEqual(text, mock_response.get_input_text())


if __name__ == '__main__':
    unittest.main()
