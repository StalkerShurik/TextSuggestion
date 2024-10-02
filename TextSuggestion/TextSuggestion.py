"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import email
import numpy as np
import pandas as pd
import reflex as rx

from data_process import process_raw_body
from model import NGramLanguageModel, TextSuggestion, WordCompletor
from rxconfig import config

N = 2

class State(rx.State):
    """The app state."""

    input_text: str = ""
    completed_word_1: str
    completed_word_2: str
    completed_word_3: str
    suggested_word: str

    def handle_change(self, value: str):
        self.input_text = value.split(' ')[-1]
        self.suggest()

    def suggest(self):
        self.final_completed_word = self.input_text

        words, probs = word_completor.get_words_and_probs(self.input_text)
        
        if len(probs) > 0:
            self.final_completed_word = words[np.argmax(np.array(probs))]


def suggestion():
    return rx.card(
        rx.flex(
            rx.flex(
                rx.text(State.final_completed_word, size="2", weight="bold"),
                direction="row",
                align_items="left",
                spacing="1",
            ),
            justify="between",
        )
    )

def index() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.input(
                placeholder="Write here!",
                value=State.input_text,
                on_change=State.handle_change,
            ),
            rx.flex(
                suggestion(),
                direction="column",
                spacing="1",
            ),
            direction="column",
            spacing="3",
        ),
        style={"maxWidth": 500},
    )


email_dataset = pd.read_csv('emails.csv')
corpus = []

for i in range(1000):
    mes = email.message_from_string(email_dataset['message'][i])
    text = mes.get_payload()
    text = process_raw_body(text)
    corpus.append(text.split(' '))

print("DATASET PREPARED")

word_completor = WordCompletor(corpus)
print("WORD COMPETOR READY")
n_gram_model = NGramLanguageModel(corpus, n=2)
print("NGRAM MODEL READY")
text_suggestion = TextSuggestion(word_completor, n_gram_model)
print("TEXT SUGGESTION READY")

app = rx.App()
app.add_page(index)