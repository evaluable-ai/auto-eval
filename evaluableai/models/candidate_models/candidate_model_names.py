from enum import Enum


class CandidateModelName(Enum):
    HUGGING_FACE = 'huggging_face'
    OPEN_AI = 'open_ai'
    OPEN_AI_CHAT = 'open_ai_chat'
    CUSTOM = 'custom'
