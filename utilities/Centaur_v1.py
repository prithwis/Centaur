
# ---------------------------------------------------------------------------------------------------------
# Utility Modules that perform
# back office functions for Colab Notebooks
# used in Centaur based activities 

# ---------------------------------------------------------------------------------------------------------

import os
import requests
from google.colab import userdata

try:
    # Load key from Colab Secrets into environment
    api_key = userdata.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in Colab Secrets")

    os.environ["OPENAI_API_KEY"] = api_key
    print("API key loaded ✔")

    # Call OpenAI identity endpoint
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    resp = requests.get("https://api.openai.com/v1/me", headers=headers)
    resp.raise_for_status()   # catches 401 / 403 / etc.

    me = resp.json()
    name = me.get("name", "N/A")
    email = me.get("email", "N/A")

    print(f"Logged in as {name} {email}")

except Exception as e:
    print("❌ OpenAI credential check failed")
    print("Reason:", str(e))
	
	

# ---------------------------------------------------------------------------------------------------------


#| Model            | Best For                  | Notes                                       |
#| ---------------- | ------------------------- | ------------------------------------------- |
#| **GPT-4.1**      | Highest-quality reasoning | Ideal judge for complex scenario evaluation |
#| **GPT-4.1-mini** | Balanced reasoning & cost | Strong choice for adjudication logic        |
#| **GPT-4.1-nano** | High volume, low cost     | Good for simple reasoning tasks             |
#| **gpt-4o-mini**  | Prototyping & cheap       | Great starter, but upgrade recommended      |


# ---------------------------------------------------------------------------------------------------------


from openai import OpenAI

OpenAI_client = OpenAI()

# ---------------------------------------------------------------------------------------------------------

def OpenAI_llm_call(system_prompt, user_prompt, model="gpt-4o-mini"):          #Great starter, but upgrade recommended
    response = OpenAI_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    #return response.choices[0].message.content.strip()

    return {
    "header": f"OpenAI {model}",
    "content": response.choices[0].message.content.strip(),
    "usage": response.usage
    }


# ---------------------------------------------------------------------------------------------------------

def parse_usage(usage):

    completion_tokens = usage.completion_tokens
    prompt_tokens = usage.prompt_tokens
    total_tokens = usage.total_tokens

    #print(completion_tokens, prompt_tokens, total_tokens)
    return(f" | token usage {completion_tokens} + {prompt_tokens} = {total_tokens}")
	

# ---------------------------------------------------------------------------------------------------------

import textwrap

def reveal(result: dict, width: int = 100):
    import textwrap

    #token_usage = parse_usage(result.get("usage"))
    print("Response from ", result.get("header"), parse_usage(result.get("usage")),"\n")
    print("-" * width)

    for paragraph in result.get("content", "").strip().split("\n\n"):
        print(textwrap.fill(paragraph.strip(), width=width))
        print()
        
    return(result.get("content", ""))
    
import textwrap
import re

def interpret(result:dict, width: int =100):
    """
    Formats Centaur's structured output cleanly for console display.
    Preserves bullets and indentation.
    """

    #token_usage = parse_usage(result.get("usage"))
    print("Response from ", result.get("header"), parse_usage(result.get("usage")),"\n")
    print("-" * width)
    
    content = result.get("content", "").strip()
    lines = content.split("\n")

    for line in lines:

        stripped = line.strip()

        # Empty line
        if not stripped:
            print()
            continue

        # Top-level numbered headers (e.g., "1. Verdict:", "2. Explanation:")
        if re.match(r"^\d+\.", stripped):
            print()
            print(textwrap.fill(stripped, width=width))
            continue

        # Bullet sections (e.g., "- **Strategic Context**:")
        if stripped.startswith("-"):
            # Separate bullet marker from text
            bullet_text = stripped[1:].strip()

            wrapped = textwrap.fill(
                bullet_text,
                width=width,
                initial_indent="   - ",
                subsequent_indent="     "
            )
            print(wrapped)
            continue

        # Regular wrapped text (fallback)
        print(textwrap.fill(stripped, width=width))


# ---------------------------------------------------------------------------------------------------------

