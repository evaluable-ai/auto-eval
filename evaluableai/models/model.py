from abc import ABC, abstractmethod

class Model(ABC):
    @property
    @abstractmethod
    def model_name(self):
        """Abstract property for the model's name."""
        pass

    @property
    @abstractmethod
    def api_key(self):
        """Abstract property for the API key ENV."""
        pass

    @property
    @abstractmethod
    def model_version(self):
        """Abstract property for the Model Version."""
        pass