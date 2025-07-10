from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma 
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_groq import ChatGroq
from django.conf import settings
from dotenv import load_dotenv
import os


def web_loader(url):
    loader = WebBaseLoader(web_paths=[url], bs_kwargs=dict(parse_only=bs4.SoupStrainer()))

    text_doc = loader.load()
    return text_doc



def recursive_text_splitter(loaded_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    split_doc = text_splitter.split_documents(loaded_text)
    return split_doc


def embed_splitted_text(splitted_text, company_name):
    db = Chroma.from_documents(splitted_text, OllamaEmbeddings(model='nomic-embed-text'), persist_directory=f"../vectored_policies/{company_name}/")
    return db


def access_from_saved_vector_db(company_name):
    db = Chroma(
    persist_directory=f"../vectored_policies/{company_name}/",
    embedding_function=OllamaEmbeddings(model='nomic-embed-text')
)
    return db


def similarity_search(question, company_name, is_vectored: bool):
    if is_vectored:
        db = Chroma(
            persist_directory=f"../vectored_policies/{company_name}/",
            embedding_function=OllamaEmbeddings(model="nomic-embed-text")
        )
        db_count = db._collection.count()
        if db_count == 0:
            return 'pls get your policy embedded'
        res = db.similarity_search(question, k=1)
        if res:
            return res[0].page_content
        else:
            return "No similar content found."
    else:
        return "Please get your policy embedded."
    



def create_doc_chain(llm, prompt_input, company_name, is_embedded):
    if is_embedded:
        prompt = ChatPromptTemplate.from_template('''
Answer the questions elaborately based on the provided context only.
Please provide the most accurate and elaborate response based on the question
<context>
{context}
<context>
Questions:{input}
''')
        document_chain = create_stuff_documents_chain(llm , prompt)
        retriever = Chroma(persist_directory=f"../vectored_policies/{company_name}/", embedding_function=OllamaEmbeddings(model="nomic-embed-text")).as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        response=retrieval_chain.invoke({"input":prompt_input})
        return response['answer']
    else:
        return 'Please get your policy embedded.'
    

# llm = ChatGroq(api_key="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", model_name='llama3-8b-8192')
# print(create_doc_chain(llm, 'What is this doc about?', '1', True))

def train_rag(url, company_name):
    web = web_loader(url=url)
    text_split = recursive_text_splitter(web)
    embed_splitted_text(text_split, company_name)
    return 'Your embeddings are successfully saved.'


load_dotenv()

def load_ai(company_name, prompt_input):
    llm = ChatGroq(api_key='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', model_name='llama3-8b-8192')
    chain = create_doc_chain(llm, prompt_input, company_name, True)
    return chain
    