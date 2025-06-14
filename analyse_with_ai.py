"""Quickstart
Install the openai package using the following pip command:
pip install openai"""

import os
import textwrap
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
import anthropic
from groq import Groq
from save_data import DatabaseManager

open_ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))   #here or as self?
# Initialize the AI client
claude_client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))





class Ai_Analyse():
    def __init__(self, transcript_text, record_id=None, content=None, ):
        self.content = content
        self.model_open_ai = "gpt-4o-mini"
        self.record_id = record_id
        self.content = transcript_text




    def name_the_speaker_ai(self):
        response = open_ai_client.chat.completions.create(
            model=self.model_open_ai,
            messages=[
                {
                    "role":    "system" ,
                    "content": "You are an expert at analyzing dialogue transcripts and identifying any real names that are mentioned within the conversation, even if they are only used once."
                } ,
                {
                    "role":    "user" ,
                    "content": (
                        "Below is a transcript. Please return a list of speakers, assigning real names when mentioned in the dialogue. "
                        "For example: Speaker C (NAME A, maybe or can be also NAME A1), Speaker B, Speaker A. "
                        "Do not invent names — only use what’s actually spoken."
                    )
                } ,
                {
                    "role":    "user" ,
                    "content": self.content
                }
            ],
            temperature=0.0,
            max_tokens=200 # token as answer
        )

        # Display the generated text
        text = response.choices[0].message.content
        wrapped_text = textwrap.fill(text , width=80)
        print("result done with GPT40 mini")
        print(wrapped_text)


    def analysis_global_first_try(self):
        response = open_ai_client.chat.completions.create(
        model = self.model_open_ai ,
        messages = [
            {"role":    "system" ,
             "content": "You are an AI trained to analyze couple dialogues from natural conversations."} ,
            {"role": "user" , "content": (
                "Here is a conversation transcript between two people. "
                "Please analyze and output in this exact format, replacing Speaker A and Speaker B with actual names if mentioned in the transcript. "
                "If no names are found, use Speaker A and Speaker B.\n\n"
                "Speaker A Problems (or [Name]):\n"
                "- List the main emotional or communication problems this person shows.\n\n"
                "Speaker B Problems (or [Name]):\n"
                "- List the main emotional or communication problems this person shows.\n\n"
                "Shared Problems:\n"
                "- List problems that affect both or their relationship.\n\n"
                "Conclusions & Explanation:\n"
                "- Summarize what is happening beneath the surface and what could help resolve their conflict.\n\n"
                "Please keep your answer concise but detailed enough for understanding.\n\n"
                "Transcript:\n"
            )} ,
            {"role": "user" , "content": self.content} ,
        ] ,
        temperature = 0.7 ,
        max_tokens = 400 ,
        )

        text = response.choices[0].message.content
        print(text)
        wrapped_text = textwrap.fill(text , width=80)
        print("result done with GPT40 mini")
        print(wrapped_text)


    def speaker_analysis(self):
        # Generate a response using the OpenAI API
        response = open_ai_client.chat.completions.create(
            model=self.model_open_ai,
            messages=[
                {"role": "system" , "content": "You are an AI trained analyze dialogues."} ,
                {"role": "user" , "content": "Here is the transcript. Please identify how many speakers are talking. One Sentence answer: what are their roles/relationships. And format in the next line, when possible, can you identify names, when not , dont write anything?"} ,
                {"role": "user" , "content": self.content} ,
            ],
            temperature=0.7,
            max_tokens=200 # token as answer
        )

        # Display the generated text
        text = response.choices[0].message.content
        wrapped_text = textwrap.fill(text , width=80)
        print("result done with GPT40 mini")
        print(wrapped_text)


    def problem_analysis(self):
        # Specify the model to use
        model = "claude-3-5-sonnet-latest"

        # Prompt the user for input
        user_prompt = f"Here is a transcript of our last talking. {self.content}"

        # Define the system message to set the behavior of the assistant
        system_message = ("You act like an well know, experienced psychologist. Your highly skilled in identifying problems in couple relationships. And gives tips to solve them."
                          "best is, your able to nail you answers down. Problem and solution are not longer than one sentence!"
                          "Voice and tone is appealing to our target audience, they are between 28 and 38yo."
                          "when you can identify problems between the lines, feel free to give special advice")

        # Create the message payload
        messages = [
            {"role": "user" , "content": user_prompt}
        ]

        # Generate a response using the Claude API
        response = claude_client.messages.create(
            model=model ,
            system=system_message ,
            messages=messages ,
            max_tokens=150 ,
            temperature=0.7
        )

        # Display the generated text
        print("Generated text:\n" , response.content[0].text)


    def basic_groq_analysing(self, groq_model = "llama3-8b-8192", groq_heat = 0.8):
        db = DatabaseManager() # Initialize the Groq client
        print(self.content)
        # client = Groq(api_key= "KEY_GROQ")
        groq_api_key = os.getenv("GROQ_API_KEY")
        groq_client = Groq(api_key=groq_api_key)

        # client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Specify the model to use


        # "llama-3.3-70b-versatile"
        # Grok-2
        # "llama3-8b-8192"
        # "llama-7b-hf"


        # System's task
        system_prompt = ("You act like an well know, experienced psychologist. Your highly skilled in identifying problems in couple relationships. And gives tips to solve them."
                          "best is, your able to nail you answers down. Problem and solution are not longer than one sentence!"

                         )

        nothing  = ("You act like an well know, experienced psychologist. Your highly skilled in identifying problems in couple relationships. And gives tips to solve them."
                          "best is, your able to nail you answers down. Problem and solution are not longer than one sentence!"
                          "Voice and tone is appealing to our target audience, they are between 28 and 38yo."
                          "when you can identify problems between the lines, feel free to give special advice"
                         )

        # User's request
        user_prompt = f"Here is a transcript of our last talking. {self.content}"

        # Generate a response using the Groq API
        response = groq_client.chat.completions.create(
            model=groq_model ,
            messages=[
                {"role": "system" , "content": system_prompt} ,
                {"role": "user" , "content": user_prompt}
            ] ,
            temperature= groq_heat ,  # Controls creativity (0 = deterministic, 1 = creative)
            max_tokens=200  # Limits the length of the output
        )
        raw_text = response.choices[0].message.content
        # save in sql
        db.save_analysis(
            recording_id=self.record_id,
            analysis_type="relationship_analysis" ,
            model=groq_model ,
            temp=groq_heat ,
            analysis_file=raw_text
        )

        # Display the generated text

        wrapped_text = textwrap.fill(raw_text , width=80)

        print("Generated text:\n" , wrapped_text)


    def test_open_file():
        app = Ai_Analyse()
        app.open_existing_file("transcripts/20250605_211200_recording.txt")
        if app.content:
            print("Loaded content:")
            print(app.content[:300])
        else:
            print("Failed to load content.")



"""
# for debug

if __name__ == "__main__":
    app = DatabaseManager()
    app.open_existing_file("transcripts_prefabricated/before_midnight_generic_version.txt")
    print(app.content[:300])"""