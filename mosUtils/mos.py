# ------------------------------------------------------------------------------------------------------------------

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

import pymupdf

def PDF_to_Text(pdf_path):

    doc = pymupdf.open(pdf_path)

    pages = []
    for page_no, page in enumerate(doc, start=1):
        text = page.get_text("text")
        pages.append(f"\n\n===== PAGE {page_no} =====\n\n{text}")

    doc.close()

    return "\n".join(pages)
   
# ------------------------------------------------------------------------------------------------------------------   
def LLM_CleanPDF(client, rawText, sourceName, _model):

    Role = """
    You are a document-cleaning engine.

    Your task is to convert raw text extracted from a PDF into
    clean, well-structured Markdown.

    RULES

    1. Preserve ALL substantive factual content.
    2. Preserve all numbers, dates, quantities, percentages,
       names, units and factual claims.
    3. Preserve meaningful headings and section structure.
    4. Preserve useful tables. Reconstruct them as Markdown
       tables where reasonably possible.
    5. Remove advertisements, navigation menus, subscription
       prompts, cookie notices, social-media links, repeated
       headers and footers, page furniture and similar junk.
    6. Repair obvious line-break, hyphenation and formatting
       damage introduced by PDF extraction.
    7. Do NOT summarize.
    8. Do NOT interpret.
    9. Do NOT add information.
    10. Do NOT use outside knowledge.
    11. Do NOT correct or reconcile factual claims.
    12. If something is genuinely unclear or corrupted,
        preserve it rather than inventing content.

    Return ONLY the cleaned Markdown document.
    """


    Input=f"""
    SOURCE DOCUMENT: {sourceName}

    ====================
    RAW PDF TEXT
    ====================

    {rawText}
    """


    return callLLM(
    client,
    Role,
    Input,
    _model
    )


    
# ------------------------------------------------------------------------------------------------------------------    
from pathlib import Path

def GetWorld(client, pdf_path, md_path, _model="gpt-5-mini"):

    pdf_path = Path(pdf_path)
    md_path  = Path(md_path)

    print(f"Reading  : {pdf_path.name}")

    # Step 1: PDF → raw text
    rawText = PDF_to_Text(pdf_path)

    print(f"Extracted: {len(rawText):,} characters")

    # Step 2: raw text → clean Markdown
    cleanMD = LLM_CleanPDF(
        client,
        rawText,
        pdf_path.name,
        _model
    )

    # Add provenance header
    header = f"""# SOURCE: {pdf_path.stem}

**Source PDF:** `{pdf_path.name}`

---

"""

    cleanMD = header + cleanMD

    # Step 3: save
    md_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    md_path.write_text(
        cleanMD,
        encoding="utf-8"
    )

    print(f"Created  : {md_path.name}")
    print(f"Markdown : {len(cleanMD):,} characters")

    return cleanMD
    
# ------------------------------------------------------------------------------------------------------------------
from IPython.display import display, Markdown

def ShowMD(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        display(Markdown(f.read()))