import unittest
from unittest.mock import Mock, patch
from evaluableai.evaluableai import EvaluableAI  # Adjust the import according to your package structure

class TestEvaluableAI(unittest.TestCase):

    def setUp(self):
        # Mock dependencies
        self.mock_candidate_models = [Mock(), Mock()]
        self.mock_evaluating_model = Mock()
        self.mock_input_frame = Mock()

        # Instantiate EvaluableAI with mocked dependencies
        self.evaluable_ai = EvaluableAI(self.mock_candidate_models, self.mock_evaluating_model, self.mock_input_frame)

    def test_init(self):
        # Test initialization
        self.assertIsNotNone(self.evaluable_ai)
        self.assertIs(self.evaluable_ai._candidate_models_list, self.mock_candidate_models)
        self.assertIs(self.evaluable_ai._evaluating_model, self.mock_evaluating_model)
        self.assertIs(self.evaluable_ai._input_frame, self.mock_input_frame)

    @patch('evaluableai.EvaluableAI.generate_response_for_each_candidate_model')
    @patch('evaluableai.EvaluableAI.runnable')
    def test_run(self, mock_runnable, mock_generate_response):
        # Test the 'run' method
        mock_generate_response.return_value = ({}, {})
        self.evaluable_ai.run()
        mock_generate_response.assert_called_once()
        mock_runnable.assert_called_once()

    # More test methods for other functionalities
    # ...

if __name__ == '__main__':
    unittest.main()
