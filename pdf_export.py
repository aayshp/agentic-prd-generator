"""
Converts the PRD's markdown text into an actual PDF file (proper headings,
bold text, spacing) instead of raw .md text with # and ** symbols in it.
Pure-Python libraries only, so this works on Streamlit Cloud with no extra
system installs needed.
"""
import io
import re
import markdown as md_lib
from xhtml2pdf import pisa


def _clean_text(text: str) -> str:
    """
    Replaces 'fancy' unicode characters (smart quotes, special dashes) with
    plain ASCII equivalents. Without this, the PDF font can't display them
    and they show up as little black boxes instead.
    """
    replacements = {
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2011": "-",   # non-breaking hyphen
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
        "\u2022": "-",   # bullet character (markdown handles real bullets separately)
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text


def markdown_to_pdf_bytes(markdown_text: str) -> bytes:
    markdown_text = _clean_text(markdown_text)
    html_body = md_lib.markdown(markdown_text, extensions=["extra"])

    # Basic styling so headings/bold/lists actually look like a document
    html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11px; line-height: 1.5; }}
        h1 {{ font-size: 20px; margin-top: 20px; }}
        h2 {{ font-size: 16px; margin-top: 16px; border-bottom: 1px solid #ccc; }}
        h3 {{ font-size: 13px; margin-top: 12px; }}
        li {{ margin-bottom: 4px; }}
        strong {{ font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{
            border: 1px solid #ccc;
            padding: 6px 8px;
            text-align: left;
            vertical-align: top;
        }}
        th {{ background-color: #f2f2f2; }}
        td p, th p {{ margin: 0; padding: 0; }}
    </style>
    </head>
    <body>{html_body}</body>
    </html>
    """

    pdf_buffer = io.BytesIO()
    pisa.CreatePDF(html, dest=pdf_buffer)
    return pdf_buffer.getvalue()
