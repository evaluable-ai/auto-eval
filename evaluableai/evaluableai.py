from evaluableai.data_model.evaluation_object import EvaluationObject
from evaluableai.models.candidate_models.null_model import NullModel
from evaluableai.models.evaluation_models.evaluating_model import EvaluatingModel
from evaluableai.models.evaluation_models.evaluating_model_name import EvaluatingModelName
import json

class EvaluableAI:

    _responses_by_input =None
    def __init__(self, candidate_models_list=None, evaluating_model=None, input_frame=None):
        self._candidate_models_list = candidate_models_list
        self._evaluating_model = evaluating_model
        self._input_frame = input_frame
        if not self._evaluating_model:
            self._evaluating_model = EvaluatingModel(EvaluatingModelName.OPENAI, 'gpt-3.5-turbo', 'OPENAI_API_KEY')

    def run(self):
        self._responses_by_input, responses_by_model = self.generate_response_for_each_candidate_model()
        self.runnable()

    def run_with_user_data(self,json_array):
        model_responses_list = NullModel.from_json_array(json_array)
        responses_by_input = {}
        for model_response in model_responses_list:
            model_name = model_response.get_candidate_model_name() +  ":" + model_response.get_candidate_model_version()
            input_key = str(model_response.get_input_id())
            if input_key not in responses_by_input:
                responses_by_input[input_key] = {}
            responses_by_input[input_key][model_name] = model_response

        self._responses_by_input = responses_by_input
        self.runnable()

    def runnable(self):
        evaluation_objects = self.create_evaluation_objects(self._responses_by_input)
        evaluation_result = self.run_evaluation_models(evaluation_objects)
        self.save_to_json(evaluation_result)


    def generate_response_for_each_candidate_model(self):
        responses_by_model = {}
        responses_by_input = {}

        for candidate_model in self._candidate_models_list:
            model_name = candidate_model.model_name  + ":" + candidate_model.model_version # Assuming each model has a unique name
            responses_by_model[model_name] = {}

            for input_row in self._input_frame:
                input_key = input_row.input_id  # Assuming each input row has a unique identifier
                if input_key not in responses_by_input:
                    responses_by_input[input_key] = {}

                response = candidate_model.generate_response(input_row)
                responses_by_model[model_name][input_key] = response
                responses_by_input[input_key][model_name] = response

        return responses_by_input, responses_by_model

    def create_evaluation_objects(self, responses_by_input):
        evaluation_objects = []

        for input_key, model_responses in responses_by_input.items():
            # Collect all responses for this input ID from different models
            all_responses_for_input = []
            for model_name, response in model_responses.items():
                all_responses_for_input.append(response)

            # Create an EvaluationObject for this input ID with all gathered responses
            evaluation_object = EvaluationObject(all_responses_for_input)
            evaluation_objects.append(evaluation_object)
        return evaluation_objects

    def run_evaluation_models(self,evaluation_objects):
        return self._evaluating_model.run_evaluation(evaluation_objects)

    def save_to_json(self, evaluation_result, path='ui.json'):
        json_list = [eval_obj.to_dict() for eval_obj in
                     evaluation_result]  # Convert each EvaluationObject to a dictionary

        with open(path, 'w') as json_file:
            json.dump(json_list, json_file, indent=4)




