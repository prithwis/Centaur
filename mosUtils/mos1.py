# ------------------------------------------------------------------------------------------------------------------
# =============================================================================
# CENTAUR : MOS — Middle East Oil Security
# Prithwis Mukerjee | 2026
# =============================================================================
# ------------------------------------------------------------------------------------------------------------------

import mos


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
def LLM_CleanPDF(client,Role, rawText, sourceName, _model):

    


    Input=f"""
    SOURCE DOCUMENT: {sourceName}

    ====================
    RAW PDF TEXT
    ====================

    {rawText}
    """


    return mos.callLLM(
    client,
    Role,
    Input,
    _model
    )


    
# ------------------------------------------------------------------------------------------------------------------   

from pathlib import Path
from datetime import datetime
import re

def makeMDName(pdf_file, md_dir, length=20):

    # Original PDF filename without extension
    stem = Path(pdf_file).stem

    # Remove blanks and special characters
    stem = re.sub(r'[^A-Za-z0-9]', '', stem)

    # First 20 characters
    stem = stem[:length]

    # Creation date: YYMMDD
    date = datetime.now().strftime("%y%m%d")

    # filename: 20chars_yymmdd.md
    return Path(md_dir) / f"{stem}_{date}.md"


 
from pathlib import Path

def GetWorldFile(client, Role, pdf_file, md_dir, _model="gpt-5-mini"):

    pdf_file = Path(pdf_file)
    #md_path  = Path(md_path)
    
   # Generate MD filename automatically
    md_path = makeMDName(
        pdf_file,
        md_dir,
        length=20
    )

    print(f"Reading  : {pdf_file.name}")

    # Step 1: PDF → raw text
    rawText = PDF_to_Text(pdf_file)

    print(f"Extracted: {len(rawText):,} characters")

    # Step 2: raw text → clean Markdown
    cleanMD = LLM_CleanPDF(
        client, Role,
        rawText,
        pdf_file.name,
        _model
    )

    # Add provenance header
    header = f"""# SOURCE: {pdf_file.stem}

**Source PDF:** `{pdf_file.name}`

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

    return md_path
    
# ------------------------------------------------------------------------------------------------------------------
from IPython.display import display, Markdown

def ShowMD(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        display(Markdown(f.read()))