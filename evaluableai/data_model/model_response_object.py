import json
import uuid

class ModelResponseObject:
    def __init__(self, response_id, response_text,input_row,model):
        self._response_id = response_id
        self._response_text = response_text
        self._input_row = input_row
        self._model = model

    @property
    def response_text(self):
        return self._response_text

    def get_candidate_model_name(self):
        return self._model.model_name

    def get_candidate_model_version(self):
        return self._model.model_version

    def get_input_text(self):
        return self._input_row.input_text

    def get_input_context(self):
        return self._input_row.context

    def get_input_id(self):
        return self._input_row.input_id

    def __repr__(self):
        return (f"ModelResponseObject(response_id={repr(self._response_id)}, "
                f"response_text={repr(self._response_text)}, "
                f"input_object={repr(self._input_row)}, "
                f"model={repr(self._model)})")
    
    def __str__(self):
        return self.to_dict()

    def to_dict(self):
        """Converts the object properties to a dictionary."""
        return {
            'response_id': str(self._response_id),
            'response_text': self._response_text,
            'input_row': self._input_row.to_dict(),
            'model_name': self.get_candidate_model_name(),
            'model_version': self.get_candidate_model_version()
        }
