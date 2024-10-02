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
    input_text_copy: str
    completed_word_1: str
    completed_word_2: str
    completed_word_3: str
    suggested_word: str

    def handle_change(self, value: str):
        self.input_text_copy = value.split(' ')
        self.suggest()

    def suggest(self):
        self.final_completed_word = self.input_text_copy

        words = text_suggestion.suggest_text(self.input_text_copy)[0]
        
        if len(words) > 0:
            self.completed_word_1 = words[0]
        else:
            self.completed_word_1 = ""

        if len(words) > 1:
            self.completed_word_2 = words[1]
        else:
            self.completed_word_2 = ""

        if len(words) > 2:
            self.completed_word_3 = words[2]
        else:
            self.completed_word_3 = ""

        if len(words) > 3:
            self.suggested_word = ' '.join(words[3:])
        else:
            self.suggested_word = ""


def block(text):
    return rx.card(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.text(text, size="2", weight="bold"),
                    direction="column",
                    spacing="1",
                ),
                direction="row",
                align_items="left",
                spacing="1",
            ),
            justify="between",
        )
    )

def suggestion():
    return rx.card(
        rx.flex(
            rx.flex(
                block(State.completed_word_1),
                block(State.completed_word_2),
                block(State.completed_word_3),
                block(State.suggested_word),
                #rx.text(State.suggested_word, size="2", weight="bold"),
                direction="column",
                align_items="left",
                spacing="4",
            ),
            #justify="between",
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
                spacing="3",
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