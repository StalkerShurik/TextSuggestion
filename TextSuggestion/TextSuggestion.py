"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    suggested_text: str = ""

def suggestion():
    return rx.card(
        rx.flex(
            rx.flex(
                rx.text(State.suggested_text + "Hello", size="2", weight="bold"),
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
                value=State.suggested_text,
                on_change=State.set_suggested_text,
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

app = rx.App()
app.add_page(index)
