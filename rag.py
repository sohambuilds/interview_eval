from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.schema import Document
import os
from langchain.retrievers import TimeWeightedVectorStoreRetriever

class RAGAnswerGenerator:
    def __init__(self, knowledge_base_dir, groq_api_key):
        os.environ["GROQ_API_KEY"] = groq_api_key
        self.knowledge_base_dir = knowledge_base_dir
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.vectorstore = self._create_vectorstore()
        self.llm = ChatGroq(model_name="mixtral-8x7b-32768", temperature=0)
        self.qa_chain = self._create_qa_chain()

    def _create_vectorstore(self):
        documents = []
        for filename in os.listdir(self.knowledge_base_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.knowledge_base_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    documents.append(Document(page_content=text, metadata={"source": filepath}))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        return FAISS.from_documents(texts, self.embeddings)

    def _create_qa_chain(self):
        # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        # return ConversationalRetrievalChain.from_llm(
        #     llm=self.llm,
        #     retriever=self.vectorstore.as_retriever(),
        #     memory=memory
        # )
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        retriever = TimeWeightedVectorStoreRetriever(
            vectorstore=self.vectorstore,
            decay_rate=0.01,
            k=5  # Retrieve top 5 most relevant documents
        )
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory
        )

    def generate_answer(self, question):
        result = self.qa_chain({"question": question})
        return result['answer']