import json
class ScoreObject:
    def __init__(self, accuracy, relevance, coherence, overall,source):
        self.accuracy = accuracy
        self.relevance = relevance
        self.coherence = coherence
        self.overall = overall
        self.source= source

    def __repr__(self):
        return (f"ScoreObject(accuracy={self.accuracy}, "
                f"relevance={self.relevance}, coherence={self.coherence}, "
                f"overall={self.overall})")

    def to_dict(self):
        # Placeholder for the to_dict method
        # Converts the object properties to a dictionary
        return {
            'accuracy': self.accuracy,
            'relevance': self.relevance,
            'coherence': self.coherence,
            'overall': self.overall,
            'source': self.source
        }

    def __str__(self):
        return self.to_dict()



