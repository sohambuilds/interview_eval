from speechrec import speech_to_text, capture_interview_qa
from rag import RAGAnswerGenerator
from intervieweval import AnswerComparisonScorer
import os

class InterviewEvaluationPipeline:
    def __init__(self, knowledge_base_dir, groq_api_key):
        self.knowledge_base_dir = knowledge_base_dir
        self.groq_api_key = groq_api_key
        self.rag_generator = RAGAnswerGenerator(knowledge_base_dir, groq_api_key)
        self.scorer = AnswerComparisonScorer(groq_api_key)

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
        print(f"ROUGE Scores: {result['rouge_scores']}")
        print(f"LLM Evaluation:\n{result['llm_evaluation']}")

        return result

def main():
    knowledge_base_dir = "RAG"
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("Please set the GROQ_API_KEY environment variable.")

    pipeline = InterviewEvaluationPipeline(knowledge_base_dir, groq_api_key)
    pipeline.run_evaluation()

if __name__ == "__main__":
    main()