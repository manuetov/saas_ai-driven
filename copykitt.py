import os
from typing import List
import openai
from dotenv import load_dotenv
import argparse
import re

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

MAX_INPUT_LENGTH = 32

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"user_input: {user_input}")
    if (validate_length(user_input) <= MAX_INPUT_LENGTH):
        generate_branding_snippet(user_input)
        generate_keywords(user_input)
    else:
        raise ValueError(f"input demasiado largo, debe ser menor a {MAX_INPUT_LENGTH}. input enviado es: {user_input}")


def validate_length(prompt: str) -> bool:
    return len(prompt) 


def generate_keywords(prompt: str) -> List[str]:

    # Obtener la clave API desde la variable de entorno
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt = f"generate upbeat branding keywords research for {prompt}"
    print(enriched_prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Cambiado a Chat API
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generate response and translated to spanish language"},
            {"role": "user", "content": enriched_prompt}
        ],
        max_tokens=32
    )

    keywords_text: str = response['choices'][0]['message']['content']
    #print(f"keywords_text: {keywords_text}")
    keywords_array = re.split(",|\n|\*|-", keywords_text)
    #print(f"keywords_array: {keywords_array}")
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]

    print(f"keywords: {keywords_array}")
    return keywords_array


def generate_branding_snippet(prompt: str) -> str:

    # Obtener la clave API desde la variable de entorno
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt = f"generate upbeat branding snippet for {prompt}"
    print(enriched_prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Cambiado a Chat API
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generate a response traslate to spanish language"},
            {"role": "user", "content": enriched_prompt}
        ],
        max_tokens=32
    )

    branding_text: str = response['choices'][0]['message']['content']

    branding_text = branding_text.strip()
    last_char = branding_text[-1]
    if last_char not in {".", "!", "?"}:
        branding_text += "..."
        
    print(f"Branding: {branding_text}")
    return branding_text


if __name__ == "__main__":
    main()
