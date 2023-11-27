import json
import os
import time
from datetime import datetime

import requests

from evaluableai.data_model.score_object import ScoreObject
from evaluableai.models.model import Model


class Openai(Model):
    BASE_API_URL = 'https://api.openai.com/v1/chat/completions'

    def __init__(self, model_version, api_key_env):
        self._model_name = 'Openai'
        self._model_version = model_version
        self._api_key_env = api_key_env
        self._api_key = os.getenv(api_key_env)

    @property
    def model_name(self):
        return self._model_name

    @property
    def api_key(self):
        return self._api_key

    @property
    def model_version(self):
        return self._model_version

    def get_header(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.api_key}",  # Replace with your actual API key
        }
        return headers

    def create_prompt(self, input_text, context, response):
        # Constructing the evaluation prompt
        prompt = f"Given the input: '{input_text}' and the context: '{context}', evaluate the following response:\n\n'{response}'"

        # Adding instructions for the evaluation at the end of the prompt
        prompt += """\nPlease evaluate each response for accuracy, relevance, and coherence. Give a score for each response for accuracy, relevance and coherence on a grade of 1 to 10 and then a final score for each response out of 10 based on 60 percent accuracy, 20 percent relevance and 20 percent coherence in the following json array format  
                   {
                   "{ Scores": [
                       {
                           "Accuracy": 5,
                           "Relevance": 5,
                           "Coherence": 5,
                           "Overall": 5
                       }
                   ] }Only give json back in above format in output
                   """
        return prompt

    def get_body(self, input_text, context, response):
        data = {
            'model': self.model_version,  # or the latest available models
            'messages': [
                {
                    "role": "user",
                    "content": self.create_prompt(input_text, context, response)
                }
            ],
            'response_format': {
                "type": "json_object"
            },
            'temperature': 0,  # Adjust as needed for creativity vs. precision
            # 'max_tokens': 4000,  # Adjust as needed based on expected length of evaluation
        }
        return data

    def run_evaluation(self, evaluation_objects):
        evaluations = []
        for evaluation_object in evaluation_objects:
            scores_list = []
            for candidate_model_response in evaluation_object.candidate_model_response_objects:
                input_text = candidate_model_response.get_input_text()
                context = candidate_model_response.get_input_context()
                response = candidate_model_response.response_text
                body = self.get_body(input_text, context, response)
                time.sleep(1)
                # Sending the prompt to the OpenAI API for evaluation
                response = requests.post(self.BASE_API_URL, headers=self.get_header(), data=json.dumps(body))

                # Check if the request was successful
                if response.status_code == 200:
                    # Append the evaluated text to the evaluations list
                    valid_response = response.json()['choices'][0]['message']['content'].strip()
                    score = json.loads(valid_response)["Scores"][0]
                    score_object = (ScoreObject(accuracy=score['Accuracy'], relevance=score['Relevance'],
                                                coherence=score['Coherence'], overall=score['Overall'],
                                                source=self.model_name + "::" + self.model_version + "::" + datetime.now().strftime(
                                                    "%Y-%m-%d %H:%M:%S")))
                    scores_list.append(score_object)
                else:
                    print(response.json())
            evaluation_object.scores = scores_list
            evaluation_object.evaluating_model_name = self.model_name
            evaluation_object.evaluating_model_version = self.model_version
            evaluations.append(evaluation_object)

        # need to fix this to handle errors and stop if output is not available
        return evaluations
