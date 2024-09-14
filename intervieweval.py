import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.llms import Groq
from langchain.prompts import PromptTemplate

class AnswerComparisonScorer:
    def __init__(self, groq_api_key, embeddings):
        self.embeddings = embeddings
        self.llm = Groq(api_key=groq_api_key, temperature=0.2)
        
        self.eval_prompt = PromptTemplate(
            input_variables=["question", "ideal_answer", "actual_answer"],
            template="""
            Question: {question}
            Ideal Answer: {ideal_answer}
            Actual Answer: {actual_answer}
            
            Evaluate the actual answer based on the following criteria:
            1. Relevance to the question
            2. Accuracy of information
            3. Completeness of the response
            4. Clarity and articulation
            
            Provide a score out of 10 and a brief explanation for your scoring.
            
            Score (out of 10):
            Explanation:
            """
        )

    def compute_similarity(self, ideal_answer, actual_answer):
        ideal_embedding = self.embeddings.encode(ideal_answer)
        actual_embedding = self.embeddings.encode(actual_answer)
        similarity = cosine_similarity([ideal_embedding], [actual_embedding])[0][0]
        return similarity

    def llm_evaluation(self, question, ideal_answer, actual_answer):
        prompt = self.eval_prompt.format(
            question=question,
            ideal_answer=ideal_answer,
            actual_answer=actual_answer
        )
        response = self.llm(prompt)
        return response

    def score_answer(self, question, ideal_answer, actual_answer):
        similarity_score = self.compute_similarity(ideal_answer, actual_answer)
        llm_evaluation = self.llm_evaluation(question, ideal_answer, actual_answer)
        
        try:
            llm_score = float(llm_evaluation.split('\n')[0].split(':')[1].strip()) / 10
        except (IndexError, ValueError):
            print("Warning: Could not parse LLM score. Using similarity score only.")
            llm_score = similarity_score

        final_score = 0.4 * similarity_score + 0.6 * llm_score
        
        return {
            'final_score': final_score,
            'similarity_score': similarity_score,
            'llm_evaluation': llm_evaluation
        }
