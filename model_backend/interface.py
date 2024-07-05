import random
import streamlit as st

from langchain.llms import HuggingFaceHub

from langchain.prompts import PromptTemplate

import langchain_core

from langchain.chains import ConversationChain

import os

CONTEXT = """Reply as a home assistant with plain text without tags.
When asked to turn on lights say LIGHTSON.
When asked to turn off lights say LIGHTSOFF.
When asked to turn on fan say FANON.
When asked to turn off fan say FANOFF.

{summaries}
{question}

User: """

LIGHTSON = "LIGHTSON"
LIGHTSOFF = "LIGHTSOFF"
FANON = "FANON"
FANOFF = "FANOFF"

CONTEXT = """ You are a friendly home assistant. If the user asks you to turn the lights or fans off or on, say 'JOBDOONE'.


QUESTION: {question}
==============
{summaries}
==============
FINAL ANSWER IN ENGLISH: """

CONTEXT = '''
The following is a friendly conversation between a human and an AI.
The AI is talkative and provides lots of specific details from its context.
If the AI does not know the answer to a question, it truthfully says it does not know.

When asked to turn on lights say LIGHTSON.
When asked to turn off lights say LIGHTSOFF.
When asked to turn on fan say FANON.
When asked to turn off fan say FANOFF.

Current conversation: {history}

Human: {input}

AI:'''

class Model:
    def __init__(self, name: str = "google/flan-t5-large") -> None:
        self.name = name
        self.model = HuggingFaceHub(
                repo_id = name,
                model_kwargs = {"temperature": 0.9, "max_new_tokens": 250})

        self.context = CONTEXT

        self.prompt = PromptTemplate(
                input_variables=['history', 'input'],
                template=self.context)

        self.chain = ConversationChain(llm=self.model, prompt=self.prompt)

    def infer(self, message: str) -> str:
        output_str = self.chain({"input": message})['response']

        if FANON in output_str:
            st.success("Turning on fan!")

        if FANOFF in output_str:
            st.success("Turning off fan!")

        if LIGHTSON in output_str:
            st.success("Turning on lights!")

        if LIGHTSOFF in output_str:
            st.success("Turning off lights!")

        return output_str

    def set_context(self, context: str) -> None:
        self.context = context

    def context(self) -> str:
        return self.context


model = Model()

