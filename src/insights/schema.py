class Insight:
    def __init__(self, type, text, value, metadata=None):
        self.type = type
        self.text = text
        self.value = value
        self.metadata = metadata or {}

        # Will be filled by agent
        self.priority = None
        self.score = None
        self.action = None

    def to_dict(self):
        return {
            "type": self.type,
            "text": self.text,
            "value": self.value,
            "priority": self.priority,
            "score": self.score,
            "action": self.action
        }