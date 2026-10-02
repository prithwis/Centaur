# =============================================================================
# MOS — Middle East Oil Security
# WorldFacts — Real-World Evidence Collection and Preparation
#
# Prithwis Mukerjee | 2026
# https://www.linkedin.com/in/prithwis/
# =============================================================================


from mos import *
import time

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
    return callLLM(client,Role,Input,_model)
    #return mos.callLLM(client,Role,Input,_model)

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


# ------------------------------------------------------------------------------------------------------------------    
from pathlib import Path

def GetWorldFile(client, Role, pdf_file, md_dir, _model="gpt-5-mini"):

    pdf_file = Path(pdf_file)
    #md_path  = Path(md_path)
    
   # Generate MD filename automatically
    md_path = makeMDName(pdf_file, md_dir,length=20)
    print(f"Reading  : {pdf_file.name}")

    # Step 1: PDF → raw text
    rawText = PDF_to_Text(pdf_file)
    print(f"Extracted: {len(rawText):,} characters")

    # Step 2: raw text → clean Markdown
    cleanMD = LLM_CleanPDF(client, Role,rawText,pdf_file.name,_model)

    # Add provenance header
    header = f"""# SOURCE: {pdf_file.stem}

    **Source PDF:** `{pdf_file.name}`

    ---

    """
    cleanMD = header + cleanMD

    # Step 3: save
    md_path.parent.mkdir( parents=True, exist_ok=True)
    md_path.write_text(cleanMD,encoding="utf-8")

    print(f"Created  : {md_path.name}")
    print(f"Markdown : {len(cleanMD):,} characters")

    return md_path
    
# ------------------------------------------------------------------------------------------------------------------
from IPython.display import display, Markdown

def ShowMD(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        display(Markdown(f.read()))
        
# ------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------
# Prepares a list of MoneyControl URLs for a specified section
# ------------------------------------------------------------------------

def get_mc_links(baseURL, section):

    res = requests.get(baseURL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if (
            href.startswith("https://www.moneycontrol.com/")
            and section in href
        ):
            links.add(href)

    print(f"{section} links located : {len(links)}")

    return list(links)
    
# ------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------
# Extracts text from ONE MoneyControl URL
# ------------------------------------------------------------------------

def extract_mc(url):

    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        # Title
        h1 = soup.find("h1")

        if not h1:
            return None

        title = h1.get_text(strip=True)

        # Target article content container
        container = (
            soup.find("div", class_="content_wrapper") or
            soup.find("div", id="contentdata")
        )

        if not container:
            return None

        paragraphs = container.find_all("p")

        clean = []

        for p in paragraphs:

            text = p.get_text(" ", strip=True)

            # Remove junk
            if any(x in text.lower() for x in [
                "follow us",
                "invest now",
                "advertisement",
                "click here",
                "watch video"
            ]):
                continue

            if len(text.split()) < 8:
                continue

            clean.append(text)

        if len(clean) < 3:
            return None

        return {
            "title": title,
            "content": " ".join(clean[:6]),
            "source": "Moneycontrol",
            "url": url
        }

    except Exception as e:
        print("Error:", e)
        return None
        
# ------------------------------------------------------------------------
# Extracts valid stories from discovered MoneyControl links
# ------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_stories(mc_links, batch_size=10, delay=0.5):

    stories = []
    total = len(mc_links)

    for i, u in enumerate(mc_links, 1):

        art = extract_mc(u)

        if art:
            stories.append(art)

        # Status + throttle after every batch of 10
        if i % batch_size == 0:
            print(
                f"Processed {i}/{total} | Valid stories: {len(stories)}"
            )
            time.sleep(delay)

    # Print final partial batch, if any
    if total % batch_size != 0:
        print(
            f"Processed {total}/{total} | Valid stories: {len(stories)}"
        )

    print("-" * 40)
    print(f"Links examined : {total}")
    print(f"Valid stories  : {len(stories)}")

    return stories
    
# ------------------------------------------------------------------------
# Creates MOS LiveFeed file from scored stories
# ------------------------------------------------------------------------

from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

def CreateLiveFeed(stories, cutoff):

    selected = [
        s for s in stories
        if s["score"] >= cutoff
    ]

    timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%y%m%d_%H%M_IST")

    filename = Path(f"MOS-MC-LiveFeed_{timestamp}.txt")

    with open(filename, "w", encoding="utf-8") as f:

        for i, s in enumerate(selected, 1):

            f.write("=" * 80 + "\n")
            f.write(f"STORY  : {i}\n")
            f.write(f"SCORE  : {s['score']}\n")
            f.write(f"TITLE  : {s['title']}\n")
            f.write(f"SOURCE : {s['source']}\n")
            f.write(f"URL    : {s['url']}\n")
            f.write("-" * 80 + "\n")
            f.write(s["content"])
            f.write("\n\n")

    print(f"Stories selected : {len(selected)}")
    print(f"File created     : {filename}")

    return filename