from flask import Flask, request, jsonify
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
folder_path = "db"

file_path = r'C:\Users\Adhiraj\Downloads\Corpus.pdf'

loader = PyPDFLoader(file_path)
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=80,
)
doc = text_splitter.split_documents(pages)

llm = ChatOllama(model="phi3")
QueryPrompt = PromptTemplate(
    input_variables=["questions"],
    template = """
    You are Bob. Your task is to generate 3 different versions of the given user question to retrive relevant documents from a vector database.Try to include the year, prices and names where ever required. By generating multiple perspectives on user questions, your aim is to overcome the limitations of the distance based similarity search. Provide alternative questions separated by newlines. 
    Original Question: {question},
    """
)

embedding_model = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma.from_documents(documents=doc, embedding=embedding_model, persist_directory = folder_path)

@app.route('/generate-response', methods=['POST'])
def aiChat():
    data = request.json
    question = data.get("message")

    retriever = MultiQueryRetriever.from_llm(
        db.as_retriever(),
        llm,
        prompt = QueryPrompt
    )
    prompt_template = """ You help customers by answering their questions based on the context fetched by retriever. Make sure not to make any changes to the context. Answer the questions based ONLY the context and if you don't have an answer from the provided information than ask the user to contact the business dealer. 
    Given these texts:
    -----
    {context}
    -----
    Please answer the following question:
    {question}

    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = chain.invoke(question)
    if isinstance(response, dict):
        response_text = response.get('text_content', '')
    else:
        response_text = str(response)
    try:
         return jsonify({'response': response_text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
    

if __name__ == '__main__':
    app.run(debug=True)
