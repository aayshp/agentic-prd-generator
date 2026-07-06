
import io
import markdown as md_lib
from xhtml2pdf import pisa


def markdown_to_pdf_bytes(markdown_text: str) -> bytes:
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
    </style>
    </head>
    <body>{html_body}</body>
    </html>
    """

    pdf_buffer = io.BytesIO()
    pisa.CreatePDF(html, dest=pdf_buffer)
    return pdf_buffer.getvalue()
