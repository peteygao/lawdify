import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI as OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Prevent deadlocks by NOT parallelizing tokenizer in development
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Initialise Nomic's embedding model through HuggingFace
embedding = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1.5",
    model_kwargs={"trust_remote_code": True},
)

chroma = Chroma("lawdify", embedding_function=embedding, persist_directory="./chromadb")

# Get just the string output from the LLM
output_parser = StrOutputParser()

# Initialise the LLM client (OpenAI compatible)
client = OpenAI(
    base_url=os.environ['BASE_URL'],
    model_name=os.environ['MODEL_NAME'],
    temperature=0.0,
    top_p=0.2,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
def ask_llm(question):
    relevant_docs = chroma.similarity_search(question,k=6)

    print("How many relevant docs?")
    print(len(relevant_docs))
    print("What's the final prompt?")
    print(f"===BEGIN===\n{"\n".join(map(lambda page: page.page_content.replace("\n",""), relevant_docs))}\n===END===\n{question}")

    # Initialise default system prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a world class litigation attorney and expert law scholar, please follow the instructions and answer based on the data and text provided between ===BEGIN=== and ===END===, do not make any conjectures outside of the referenced source of data. Please do not refer to yourself. Do not use Markdown. Thank you."),
        ("user", f"===BEGIN===\n{"\n".join(map(lambda page: page.page_content.replace("\n",""), relevant_docs))}\n===END===\n{{input}}")
    ])

    # Create the langchain chain
    chain = prompt | client | output_parser

    return { "message": chain.invoke({"input": question}) }
