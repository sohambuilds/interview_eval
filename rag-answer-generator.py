import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import Groq
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader

class RAGAnswerGenerator:
    def __init__(self, knowledge_base_dir, groq_api_key):
        os.environ["GROQ_API_KEY"] = groq_api_key
        self.knowledge_base_dir = knowledge_base_dir
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.vectorstore = self._create_vectorstore()
        self.qa_chain = self._create_qa_chain()

    def _create_vectorstore(self):
        documents = []
        for filename in os.listdir(self.knowledge_base_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.knowledge_base_dir, filename)
                loader = TextLoader(filepath)
                documents.extend(loader.load())

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        return Chroma.from_documents(texts, self.embeddings)

    def _create_qa_chain(self):
        llm = Groq(temperature=0)
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever()
        )

    def generate_answer(self, question):
        return self.qa_chain.run(question)
