# =============================================================================
# MOS — Monte Carlo++ (MC++)
# An LLM-Based Geopolitical Simulation Framework
# Part of the Centaur Architecture
# Action -> Consequence -> Reaction -> ...
# Designed and Developed by Prithwis Mukerjee | 2026
# =============================================================================


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



import time

def callLLM(client, _Role, _Input, _model, _effort="medium"):

    start = time.perf_counter()

    response = client.responses.create(
        model=_model,
        instructions=_Role,
        input=_Input,
        reasoning={"effort": _effort}
    )

    elapsed = time.perf_counter() - start

    usage = response.usage
    reasoning_tokens = getattr(usage.output_tokens_details, "reasoning_tokens", 0) or 0
    cached_tokens = getattr(usage.input_tokens_details, "cached_tokens", 0) or 0

    visible_tokens = usage.output_tokens - reasoning_tokens
    throughput = usage.output_tokens / elapsed if elapsed > 0 else 0

    print(
        f"Model: {response.model} | "
        f"Effort: {_effort} | "
        f"Time: {elapsed:.1f}s | "
        f"Input: {usage.input_tokens:,} | "
        f"Cached: {cached_tokens:,} | "
        f"Output: {usage.output_tokens:,} | "
        f"Reasoning: {reasoning_tokens:,} | "
        f"Visible: {visible_tokens:,} | "
        f"Total: {usage.total_tokens:,} | "
        f"Speed: {throughput:.1f} tok/s | "
        f"Status: {response.status}"
    )

    return response.output_text

    


# ------------------------------------------------------------------------------------------------------------------

