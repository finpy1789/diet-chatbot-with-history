import gradio as gr
from typing import List, Any, Generator
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage


class PersistentChatBotUI:
    def __init__(self, diet_chatbot):
        """Initialize the UI with a chatbot instance."""
        self.diet_chatbot = diet_chatbot

    def stream_message_handler(
        self, user_message: str, history: list
    ) -> Generator:
        """Send message to chatbot and stream the response."""

        if history is None:
            history = []

        if not user_message or not user_message.strip():
            yield "", history
            return

        user_message = user_message.strip()

        # Add user message
        history.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        # Add placeholder assistant message
        history.append(
            {
                "role": "assistant",
                "content": "",
            }
        )

        yield "", history

        full_response = ""

        for chunk in self.diet_chatbot.stream_response(user_message):
            full_response += chunk

            history[-1]["content"] = full_response

            yield "", history

    def new_session_handler(self):
        """Create a new conversation and update UI."""
        self.diet_chatbot.new_session()
        return [], self.update_session_choices()

    def load_session_handler(self, session_id: str):
        """Load an existing conversation."""

        if not session_id:
            return [], self.update_session_choices()

        self.diet_chatbot.load_session(session_id)

        return (
            self._format_messages_for_ui(
                self.diet_chatbot.get_messages()
            ),
            self.update_session_choices(),
        )

    def _format_messages_for_ui(
        self, messages: List[BaseMessage]
    ) -> list:
        """Convert LangChain messages to Gradio message format."""

        ui_messages = []

        for msg in messages:

            if isinstance(msg, HumanMessage):
                ui_messages.append(
                    {
                        "role": "user",
                        "content": msg.content,
                    }
                )

            elif isinstance(msg, AIMessage):
                ui_messages.append(
                    {
                        "role": "assistant",
                        "content": msg.content,
                    }
                )

        return ui_messages

    def update_session_choices(self):
        """Update dropdown choices."""

        choices = self.diet_chatbot.get_previous_conversations()

        if self.diet_chatbot.session_id not in choices:
            choices.insert(
                0,
                self.diet_chatbot.session_id,
            )

        return gr.update(
            choices=choices,
            value=self.diet_chatbot.session_id,
        )

    def create_ui(self):

        with gr.Blocks(
            title="Diet Planning Assistant with History"
        ) as interface:

            gr.Markdown("# Diet Planning Assistant")

            gr.Markdown(
                "I can help you create balanced meal plans. Your conversations are saved!"
            )

            chatbot = gr.Chatbot(
                height=400
            )

            with gr.Row():

                with gr.Column(scale=3):

                    msg = gr.Textbox(
                        placeholder="Ask about nutrition or diet plans...",
                        show_label=False,
                    )

                with gr.Column(scale=1):

                    submit = gr.Button(
                        "💬 Send",
                        variant="primary",
                    )

            with gr.Row():

                session_choices = (
                    self.diet_chatbot.get_previous_conversations()
                )

                if (
                    self.diet_chatbot.session_id
                    not in session_choices
                ):
                    session_choices.insert(
                        0,
                        self.diet_chatbot.session_id,
                    )

                sessions = gr.Dropdown(
                    choices=session_choices,
                    value=self.diet_chatbot.session_id,
                    label="Previous Conversations",
                    interactive=True,
                )

                new = gr.Button(
                    "🆕 New Chat",
                    size="sm",
                )

            submit.click(
                self.stream_message_handler,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot],
            )

            msg.submit(
                self.stream_message_handler,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot],
            )

            new.click(
                self.new_session_handler,
                inputs=None,
                outputs=[chatbot, sessions],
            )

            sessions.change(
                self.load_session_handler,
                inputs=sessions,
                outputs=[chatbot, sessions],
            )

            interface.load(
                self.update_session_choices,
                inputs=None,
                outputs=sessions,
            )

        return interface