import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from rouge import Rouge

class AnswerComparisonScorer:
    def __init__(self, groq_api_key):
        self.llm = ChatGroq(model_name="mixtral-8x7b-32768", temperature=0.2)
        self.rouge = Rouge()
        
        self.eval_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert evaluator of interview answers, particularly for introductions and greetings."),
            ("human", """
            Question: {question}
            Ideal Answer: {ideal_answer}
            Actual Answer: {actual_answer}
            
            Evaluate the actual answer based on the following criteria:
            1. Appropriateness of the greeting
            2. Clarity in stating the name
            3. Expression of enthusiasm or pleasure to meet
            4. Overall professionalism and politeness
            
            Provide a score out of 10 and a brief explanation for your scoring.
            
            Score (out of 10):
            Explanation:
            """)
        ])

    def compute_rouge_scores(self, ideal_answer, actual_answer):
        scores = self.rouge.get_scores(actual_answer, ideal_answer)
        return {
            'rouge-1': scores[0]['rouge-1']['f'],
            'rouge-2': scores[0]['rouge-2']['f'],
            'rouge-l': scores[0]['rouge-l']['f']
        }

    def llm_evaluation(self, question, ideal_answer, actual_answer):
        messages = self.eval_prompt.format_messages(
            question=question,
            ideal_answer=ideal_answer,
            actual_answer=actual_answer
        )
        response = self.llm(messages)
        return response.content

    def score_answer(self, question, ideal_answer, actual_answer):
        rouge_scores = self.compute_rouge_scores(ideal_answer, actual_answer)
        llm_evaluation = self.llm_evaluation(question, ideal_answer, actual_answer)
        
        # Handle potential errors in LLM score parsing
        try:
            llm_score_line = [line for line in llm_evaluation.split('\n') if line.startswith("Score:")][0]
            llm_score = float(llm_score_line.split(':')[1].split('/')[0].strip()) / 10
        except (IndexError, ValueError):
            print("Warning: Could not parse LLM score. Using default score of 0.5.")
            llm_score = 0.5

        # Calculate ROUGE score, handling potential zero values
        rouge_values = list(rouge_scores.values())
        non_zero_rouge = [score for score in rouge_values if score > 0]
        if non_zero_rouge:
            rouge_score = np.mean(non_zero_rouge)
        else:
            print("Warning: All ROUGE scores are zero. Using minimum score of 0.01.")
            rouge_score = 0.01

        # Calculate final score
        final_score = 0.3 * rouge_score + 0.7 * llm_score
        
        return {
            'final_score': final_score,
            'rouge_scores': rouge_scores,
            'llm_evaluation': llm_evaluation,
            'llm_score': llm_score,
            'rouge_score': rouge_score
        }