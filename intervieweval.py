import logging
import asyncio
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from rouge import Rouge

class AnswerComparisonScorer:
    def __init__(self, groq_api_key):
        self.llm = ChatGroq(model_name="mixtral-8x7b-32768", temperature=0.2)
        self.rouge = Rouge()
        
        self.eval_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert evaluator of interview answers."),
            ("human", """
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
            """)
        ])

    def compute_rouge_scores(self, ideal_answer, actual_answer):
        scores = self.rouge.get_scores(actual_answer, ideal_answer)
        return {
            'rouge-1': scores[0]['rouge-1']['f'],
            'rouge-2': scores[0]['rouge-2']['f'],
            'rouge-l': scores[0]['rouge-l']['f']
        }

    async def llm_evaluation(self, question, ideal_answer, actual_answer):
        messages = self.eval_prompt.format_messages(
            question=question,
            ideal_answer=ideal_answer,
            actual_answer=actual_answer
        )
        response = await self.llm.ainvoke(messages)
        return response.content

    def parse_llm_score(self, llm_evaluation):
        try:
            score_line = next(line for line in llm_evaluation.split('\n') if line.startswith("Score"))
            score = float(score_line.split(':')[1].strip().split('/')[0])
            return score / 10  # Normalize to 0-1 range
        except Exception as e:
            logging.error(f"Error parsing LLM score: {e}")
            return 0.5  # Default score if parsing fails

    async def score_answer(self, question, ideal_answer, actual_answer):
        try:
            rouge_scores = self.compute_rouge_scores(ideal_answer, actual_answer)
            llm_evaluation = await self.llm_evaluation(question, ideal_answer, actual_answer)
            llm_score = self.parse_llm_score(llm_evaluation)

            rouge_score = sum(rouge_scores.values()) / len(rouge_scores)
            final_score = 0.5 * rouge_score + 0.5 * llm_score

            return {
                'final_score': final_score,
                'rouge_scores': rouge_scores,
                'llm_evaluation': llm_evaluation,
                'llm_score': llm_score
            }
        except Exception as e:
            logging.error(f"Error in score_answer: {e}")
            raise

# Wrapper function for synchronous calls
def score_answer_sync(self, question, ideal_answer, actual_answer):
    return asyncio.run(self.score_answer(question, ideal_answer, actual_answer))