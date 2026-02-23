import random
from enum import Enum

class SentenceSize(Enum):
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

_SENTENCES = {
    SentenceSize.TINY: [
        "The cat sat.",
        "I love tea.",
        "Sun rises."
    ],
    SentenceSize.SMALL: [
        'The brown fox jumps over dogs.'
        'Typing fast is ] satisfying!'
        'Keys clack, fingers attack.'
        'Hello, world! Lets code.'
        'Caps lock is my mortal enemy.'
    ],
    SentenceSize.MEDIUM: [
        "I accidentally wore socks that didn’t match today.",
        "The dog tried to chase its own shadow again.",
        "Bananas on the ceiling make for a funny breakfast.",
        "He spilled coffee on his homework right before class.",
        "Cats often ignore you until you sit down to read.",
    ],
    SentenceSize.LARGE: [
        "The quick brown fox jumps over the lazy dog while the birds chirp happily in the morning sun.",
        "As she strolled along the riverbank, the wind carried the scent of blooming flowers, filling her with a sense of peace and nostalgia.",
        "Learning to type accurately and quickly takes patience and consistent practice, but the rewards are immense for any aspiring writer or coder."
    ]
}

def get_random_sentence(size: SentenceSize) -> str:
    sentences: list[str] = _SENTENCES[size]
    return random.choice(sentences)