import json

class EvaluationObject:
    def __init__(self,model_response_objects):
        self.candidate_model_response_objects = model_response_objects
        self.scores=None
        self.evaluating_model_name=None
        self.evaluating_model_version=None


    def _get_input_text(self):
        return self.model_response_object._input_row.input_text


    def __str__(self):
        # Convert the dictionary to a JSON string
        return self.to_dict()


    def to_dict(self):
        """Converts the object properties to a dictionary."""
        # Serialize the model_response_objects
        model_responses = [response.to_dict() for response in
                           self.candidate_model_response_objects] if self.candidate_model_response_objects else []

        scores = [score.to_dict() for score in self.scores] if self.scores else []

        # Construct a dictionary of properties
        properties = {
            'model_responses': model_responses,
            'scores': scores,
            'evaluating_model_name': self.evaluating_model_name,
            'evaluating_model_version': self.evaluating_model_version
        }
        return properties
