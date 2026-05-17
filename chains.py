"""
LangChain chains module.
Contains chains for content summarization and MCQ generation.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


def create_summary_chain(model: ChatGoogleGenerativeAI):
    """
    Create a chain for summarizing study material.

    Args:
        model (ChatGoogleGenerativeAI): The LLM model to use

    Returns:
        A LangChain chain for content summarization
    """
    prompt_template = """
    Act as a documentation expert.
    Your job is to summarize the study material in bullet points.
    The study material is provided in triple quotes below.

    study material:
    ```{study_material}```

    Your response should only contain summarized content with any trailing or leading information about
    yourself.
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    chain = (
        prompt
        | model
        | StrOutputParser()
    )

    return chain


def create_mcq_chain(model: ChatGoogleGenerativeAI):
    """
    Create a chain for generating MCQ questions.

    Args:
        model (ChatGoogleGenerativeAI): The LLM model to use

    Returns:
        A LangChain chain for MCQ generation
    """
    prompt_template = """
    You are an expert in generating quiz questions from summarized data.
    Given a topic, your job is to generate 5 multiple choice questions using provided summarized content.

    The multiple choice question should follow following format
    'Here are the 5 MCQ's on topic:{topic}'
    Q1: Question 1
    Options:
    a. 
    b.
    c.
    d.

    Correct Answer: Correct option amongst a,b,c,d
    
    topic:
    {topic}

    summarized_content:
    {content_summary}

    If the {topic} is not relevant to the {content_summary}, respond as follow:
    'The provided topic is not from the knowledge bank, please provide relevant topic'
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    chain = (
        prompt
        | model
        | StrOutputParser()
    )

    return chain
