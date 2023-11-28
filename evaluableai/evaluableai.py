import json
import logging

from evaluableai.models.candidate_models.null_model import NullModel
from evaluableai.models.evaluation_models.evaluating_model import EvaluatingModel
from evaluableai.models.evaluation_models.evaluating_model_name import EvaluatingModelName
from evaluableai.data_model.evaluation_object import EvaluationObject



# Assuming logging configuration is set up in a separate module or at the package level

class EvaluableAI:
    """
    Main class for the EvaluableAI package. This class is responsible for running the evaluation
    process.
    """

    def __init__(self, candidate_models_list=None, evaluating_model=None, input_frame=None):
        """
        Initializes the EvaluableAI instance with candidate models, an evaluating model, and an input frame.

        :param candidate_models_list: List of candidate models to be evaluated.
        :param evaluating_model: The model used for evaluation.
        :param input_frame: Input data frame for the models.
        """
        self._responses_by_input = None
        try:
            logging.info("Initializing EvaluableAI with candidate models and evaluating model")
            self._candidate_models_list = candidate_models_list
            self._evaluating_model = evaluating_model
            self._input_frame = input_frame

            if not self._evaluating_model:
                self._evaluating_model = EvaluatingModel(EvaluatingModelName.OPENAI, 'gpt-3.5-turbo', 'OPENAI_API_KEY')
        except Exception as e:
            logging.exception("Failed to initialize EvaluableAI: %s", str(e))
            raise

    def run(self):
        """
        Runs the evaluation process using predefined data.
        """
        try:
            logging.info("Running EvaluableAI with predefined data")
            self._responses_by_input, responses_by_model = self.generate_response_for_each_candidate_model()
            self.runnable()
            logging.info("EvaluableAI run completed")
        except Exception as e:
            logging.exception("Error during EvaluableAI run: %s", str(e))
            raise

    def run_with_user_data(self, json_array):
        """
        Runs the evaluation process using user-provided data.

        :param json_array: A JSON array containing user data.
        """
        try:
            logging.info(f"Running EvaluableAI with user data: {len(json_array)} items")
            model_responses_list = NullModel.from_json_array(json_array)
            responses_by_input = self._process_user_data(model_responses_list)
            self._responses_by_input = responses_by_input
            self.runnable()
            logging.info("EvaluableAI run with user data completed")
        except Exception as e:
            logging.exception("Error during EvaluableAI run with user data: %s", str(e))
            raise

    def _process_user_data(self, model_responses_list):
        """
        Processes user data and organizes it for the evaluation process.

        :param model_responses_list: List of model responses from user data.
        :return: A dictionary of responses organized by input.
        """
        responses_by_input = {}
        for model_response in model_responses_list:
            model_name = model_response.get_candidate_model_name() + ":" + model_response.get_candidate_model_version()
            input_key = str(model_response.get_input_id())
            if input_key not in responses_by_input:
                responses_by_input[input_key] = {}
            responses_by_input[input_key][model_name] = model_response

        return responses_by_input

    def runnable(self):
        """
        A helper method to run the evaluation process.
        """
        try:
            evaluation_objects = self.create_evaluation_objects(self._responses_by_input)
            evaluation_result = self.run_evaluation_models(evaluation_objects)
            self.save_to_json(evaluation_result)
        except Exception as e:
            logging.exception("Error in runnable method of EvaluableAI: %s", str(e))
            raise
            
    def generate_response_for_each_candidate_model(self):
        responses_by_model = {}
        responses_by_input = {}

        for candidate_model in self._candidate_models_list:
            model_name = candidate_model.model_name + ":" + candidate_model.model_version  # Assuming each model has a unique name
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

    def run_evaluation_models(self, evaluation_objects):
        return self._evaluating_model.run_evaluation(evaluation_objects)

    def save_to_json(self, evaluation_result, path='ui.json'):
        """
        Saves the evaluation result to a JSON file.

        :param evaluation_result: The evaluation result to be saved.
        :param path: The path to the JSON file where the result will be saved.
        """
        try:
            logging.info(f"Saving evaluation results to {path}")
            json_list = [eval_obj.to_dict() for eval_obj in evaluation_result]

            with open(path, 'w') as json_file:
                json.dump(json_list, json_file, indent=4)
            logging.info("Saved evaluation results to JSON")
        except Exception as e:
            logging.exception("Error saving evaluation")
