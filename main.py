from speechrec import speech_to_text, capture_interview_qa
from rag import RAGAnswerGenerator
from intervieweval import AnswerComparisonScorer
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

class InterviewEvaluationPipeline:
    def __init__(self, knowledge_base_dir, huggingface_api_key):
        self.knowledge_base_dir = knowledge_base_dir
        self.huggingface_api_key = huggingface_api_key
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.rag_generator = RAGAnswerGenerator(knowledge_base_dir, huggingface_api_key)
        self.scorer = AnswerComparisonScorer(huggingface_api_key, self.embeddings)

    def run_evaluation(self):
        print("Starting the interview evaluation process...")

        # Step 1: Capture the interview question and answer
        question, interviewee_answer = capture_interview_qa()
        print(f"\nInterviewer's question: {question}")
        print(f"Interviewee's answer: {interviewee_answer}")

        # Step 2: Generate the ideal answer using RAG
        ideal_answer = self.rag_generator.generate_answer(question)
        print(f"\nGenerated ideal answer: {ideal_answer}")

        # Step 3: Compare and score the answer
        result = self.scorer.score_answer(question, ideal_answer, interviewee_answer)

        # Step 4: Present the results
        print("\nEvaluation Results:")
        print(f"Final Score: {result['final_score']:.2f}")
        print(f"Similarity Score: {result['similarity_score']:.2f}")
        print(f"LLM Evaluation:\n{result['llm_evaluation']}")

        return result

def main():
    knowledge_base_dir = "path/to/your/knowledge/base"
    huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

    if not huggingface_api_key:
        raise ValueError("Please set the HUGGINGFACE_API_KEY environment variable.")

    pipeline = InterviewEvaluationPipeline(knowledge_base_dir, huggingface_api_key)
    pipeline.run_evaluation()

if __name__ == "__main__":
    main()