from transformers import pipeline
import google.generativeai as genai
import os
os.environ['GOOGLE_API_KEY'] = "AIzaSyAvgIy_Ckc8o7aSc4I2NlRBPAFgmksXGVs"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

class Debater:
    def __init__(self, position):
        """
        Initialize the Debater with a specific position (e.g., 'Pro' or 'Con').
        """
        self.position = position
        self.memory = []  # Stores arguments and key points
        self.model = genai.GenerativeModel('gemini-pro')  # Using gemini

    def generate_opening_statement(self, topic):
        """
        Generate an opening statement based on the debate topic and position.
        """
        if self.position in ['Pro', 'pro']:
            prompt = f"Provide an opening statement for a debate supporting the topic '{topic}' in less than 100 words. Keep it simple and use simple words. Include salutations."
        else:
            prompt = f"Provide an opening statement for a debate opposing the topic '{topic}' in less than 100 words. Keep it simple and use simple words. Include salutations."
        response = self.model.generate_content(prompt)
        opening_statement = response.text
        self.memory.append(opening_statement)
        return opening_statement

    def generate_main_argument(self, topic, previous_points=[]):
        """
        Generate a main argument considering previous points (for coherence).
        """
        if self.position in ['Pro', 'pro']:
            prompt = f"Supporting the topic {topic}, build upon the previous points: {', '.join(previous_points)}. Use simple language."
        else:
            prompt = f"Opposing the topic {topic}, build upon the previous points: {', '.join(previous_points)}. Use simple language."
        response = self.model.generate_content(prompt)
        main_argument = response.text
        self.memory.append(main_argument)
        return main_argument

    def answer_question(self, question):
        prompt = f'''
        Question: {question}
        Answer:
        '''
        answer = self.model.generate_content(prompt).text
        return answer

    def generate_rebuttal(self, topic, opponent_points):
        """
        Generate a rebuttal based on the opponent's points.
        """
        if self.position in ['Pro', 'pro']:
            prompt = f"Supporting the topic {topic}, oppose the following points: {', '.join(opponent_points)}."
        else:
            prompt = f"Opposing the topic {topic}, oppose the following points: {', '.join(opponent_points)}."
        response = self.model.generate_content(prompt)
        rebuttal = response.text
        self.memory.append(rebuttal)
        return rebuttal

    def generate_closing_statement(self, topic):
        """
        Generate a closing statement that summarizes the debater's position.
        """
        if self.position in ['pro' ,'Pro']:
            prompt = f"Supporting the topic {topic}, provide a closing statement summarizing your arguments from {self.memory}. Keep it less than 70 words."
        else:
            prompt = f"Opposing the topic {topic}, provide a closing statement summarizing your arguments from {self.memory}. Keep it less than 70 words."
        response = self.model.generate_content(prompt)
        closing_statement = response.text
        self.memory.append(closing_statement)
        return closing_statement
