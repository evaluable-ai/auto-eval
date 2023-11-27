import unittest

from evaluableai.models.candidate_models.candidate_model_names import \
    CandidateModelName


class TestCandidateModelName(unittest.TestCase):

    def test_enum_members_exist(self):
        # Test if all expected members exist in the enum
        self.assertTrue(hasattr(CandidateModelName, 'HUGGING_FACE'))
        self.assertTrue(hasattr(CandidateModelName, 'OPEN_AI'))
        self.assertTrue(hasattr(CandidateModelName, 'OPEN_AI_CHAT'))
        self.assertTrue(hasattr(CandidateModelName, 'CUSTOM'))

    def test_enum_values(self):
        # Test the values of the enum members
        self.assertEqual(CandidateModelName.HUGGING_FACE.value, 'huggging_face')
        self.assertEqual(CandidateModelName.OPEN_AI.value, 'open_ai')
        self.assertEqual(CandidateModelName.OPEN_AI_CHAT.value, 'open_ai_chat')
        self.assertEqual(CandidateModelName.CUSTOM.value, 'custom')


if __name__ == '__main__':
    unittest.main()
