import unittest
import uuid
from unittest.mock import Mock, patch

from evaluableai.data_model.input_row_object import InputRow


class TestInputRow(unittest.TestCase):

    def setUp(self):
        self.input_text = "Sample text"
        self.context = "Sample context"
        self.input_id = uuid.uuid4()
        self.input_row = InputRow(self.input_text, self.context, self.input_id)

    def test_init(self):
        # Test initialization
        self.assertEqual(self.input_row.input_text, self.input_text)
        self.assertEqual(self.input_row.context, self.context)
        self.assertEqual(self.input_row.input_id, self.input_id)

    def test_to_dict(self):
        # Test the to_dict method
        result = self.input_row.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['input_text'], self.input_text)
        self.assertEqual(result['context'], self.context)
        self.assertEqual(result['input_id'], str(self.input_id))

    def test_input_id_immutable(self):
        # Test that input_id is immutable
        with self.assertRaises(ValueError):
            self.input_row.input_id = uuid.uuid4()

    @patch('pandas.read_csv')
    def test_from_csv(self, mock_read_csv):
        # Mock pandas read_csv method
        mock_read_csv.return_value = Mock()
        mock_df = mock_read_csv.return_value
        mock_df.iterrows.return_value = iter(
            [(0, {'text_column': 'text', 'context_column': 'context', 'id_column': self.input_id})])

        input_objects = InputRow.from_csv('dummy.csv', 'text_column', 'context_column', 'id_column')
        self.assertIsInstance(input_objects, list)
        self.assertEqual(len(input_objects), 1)
        self.assertEqual(input_objects[0].input_text, 'text')
        self.assertEqual(input_objects[0].context, 'context')
        self.assertEqual(input_objects[0].input_id, self.input_id)


if __name__ == '__main__':
    unittest.main()
