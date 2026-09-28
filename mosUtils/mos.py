# ------------------------------------------------------------------------------------------------------------------
# =============================================================================
# CENTAUR : MOS — Middle East Oil Security
# Prithwis Mukerjee | 2026
# =============================================================================
# ------------------------------------------------------------------------------------------------------------------
def authenticateOpenAI():

    import os
    import requests
    from google.colab import userdata
    from openai import OpenAI

    try:
        # Get key from Colab Secrets
        api_key = userdata.get("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in Colab Secrets")

        os.environ["OPENAI_API_KEY"] = api_key

        # Check identity
        headers = {"Authorization": f"Bearer {api_key}"}

        resp = requests.get("https://api.openai.com/v1/me",headers=headers)

        resp.raise_for_status()

        me = resp.json()

        name = me.get("name", "N/A")
        email = me.get("email", "N/A")

        print("OpenAI authentication successful ✔")
        print(f"Logged in as {name} {email}")

        return OpenAI(api_key=api_key)

    except Exception as e:

        print("❌ OpenAI credential check failed")
        print("Reason:", str(e))

        return None
		
# ------------------------------------------------------------------------------------------------------------------

def callLLM(client, _Role, _Input, _model):

    response = client.responses.create(
        model=_model,
        instructions=_Role,
        input=_Input
    )

    return response.output_text

# ------------------------------------------------------------------------------------------------------------------

