import json
from pathlib import Path
import os
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

load_dotenv()


