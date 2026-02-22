
# ---------------------------------------------------------------------------------------------------------
# CENTAUR by Prithwis Mukerjee
# Utility Modules that perform
# back office functions for Colab Notebooks
#
#
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

def echo(result: dict, width: int = 100):
    import textwrap

    #token_usage = parse_usage(result.get("usage"))
    print("Response from ", result.get("header"), parse_usage(result.get("usage")),"\n")
    print("-" * width)

    for paragraph in result.get("content", "").strip().split("\n\n"):
        print(textwrap.fill(paragraph.strip(), width=width))
        print()
        
    return(result.get("content", ""))
    

# ---------------------------------------------------------------------------------------------------------
#import requests
#
#def readRemote(url, timeout=30):
#    response = requests.get(url, timeout=timeout)
#    response.raise_for_status()
#
#    text = response.content.decode("utf-8")
#    print(f"Character count: {len(text)}")
#    print(text[:100])
#
#    return text
#    
# ---------------------------------------------------------------------------------------------------------

import requests
import os
from urllib.parse import urlparse

def read_source(source, timeout=30):
    """
    Reads from either a URL or a local file path.
    Prints character count and first 100 characters.
    Returns decoded UTF-8 text.
    """

    parsed = urlparse(source)

    # If scheme is http/https → treat as URL
    if parsed.scheme in ("http", "https"):
        response = requests.get(source, timeout=timeout)
        response.raise_for_status()
        text = response.content.decode("utf-8")

    # Otherwise treat as local file
    else:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Local file not found: {source}")

        with open(source, "r", encoding="utf-8") as f:
            text = f.read()

    print(f"Character count: {len(text)}")
    print(text[:100])

    return text
