import uuid

import pandas as pd


class InputRow:
    def __init__(self, input_text, context, input_id=None):
        self._input_id = input_id if input_id is not None else uuid.uuid4()
        self._input_text = input_text
        self._context = context

    def __repr__(self):
        return (f"InputObject(input_text={repr(self._input_text)}, "
                f"context={repr(self._context)}, input_id={repr(self._input_id)})")

    @property
    def input_id(self):
        return self._input_id

    @input_id.setter
    def input_id(self, value):
        raise ValueError("input_id cannot be changed once set.")

    @property
    def input_text(self):
        return self._input_text

    @input_text.setter
    def input_text(self, value):
        self._input_text = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @classmethod
    def from_csv(cls, csv_file_path, text_column, context_column, id_column=None):
        df = pd.read_csv(csv_file_path)
        return cls.from_dataframe(df, text_column, context_column, id_column)

    @classmethod
    def from_dataframe(cls, dataframe, text_column, context_column, id_column=None):
        input_objects = []
        for index, row in dataframe.iterrows():
            # Use the id_column if it's provided and not null, otherwise generate a new UUID
            input_id = row[id_column] if id_column and not pd.isnull(row[id_column]) else None
            input_object = cls(input_text=row[text_column], context=row[context_column], input_id=input_id)
            input_objects.append(input_object)
        return input_objects

    def __str__(self):
        # Convert the dictionary to a JSON string
        return self.to_dict()

    def to_dict(self):
        """Converts the object properties to a dictionary."""
        return {
            'input_id': str(self._input_id),  # Convert UUID to string
            'input_text': self._input_text,
            'context': self._context
        }
