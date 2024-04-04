import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")




def get_ai_response(prompt):
    """Takes in the prompt from the user's text and give it to the AI for processing"""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0

    )
    
    
    return response