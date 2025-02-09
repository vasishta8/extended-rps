from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore
import os 
import json
import re

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(
    api_key= groq_api_key 
)

def capitalizer(string):
    return " ".join([word.capitalize() for word in string.split()])

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None

def create_prompt(user_entity, system_entity):
    prompt = f"""User Entity: {user_entity} vs System Entity: {system_entity}"""
    return prompt

def user_vs_system(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a judge for a virtual game that decides which of the two provided 
                options - the one provided by the user, or the one in the system, is more powerful. Consider this game to 
                be a wild extension of the classic Rock-Paper-Scissors game. Your results 
                should always be the same, provided the two entities involved in the face-off are the same. 
                If the same two entities face off in the other order, that is, the user now provides an entity 
                that was previously with the system and vice versa, the result should be the opposite of that provided 
                earlier. The entities can be anything - superheroes, animals, objects, or even abstract concepts. If one entiry is able to 
                destroy the other entity through its own means, it wins. You get the idea. Your result should be of the following format in JSON:
                result: A singular word - "victory" or "defeat" - This is based on the user's entity winning or losing against the system entity.
                reasoning: Upto two sentences having the reasoning for the result - based on the entities' powers and abilities - this
                sentence should not include the terms 'user entity' or 'system entity' and should be a maximum of 50 words long.
                """,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.2,
    )
    json_output = chat_completion.choices[0].message.content
    parsed_json = json.loads(extract_json(json_output))
    return parsed_json

def rps_body(user_entity, system_entity, entities_used):
    # print(user_entity, system_entity, entities_used)
    if user_entity in entities_used:
        return {"result": "repeat", "reasoning": "No repeats allowed!"}
    prompt = create_prompt(user_entity, system_entity)
    result = user_vs_system(prompt)
    if (result['result'] == 'victory'):
        entities_used.add(user_entity)
    else:
        entities_used = set('Rock')
    return result     
