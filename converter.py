from pypdf import PdfReader


def pdf_to_json(file, filename: str) -> dict:
    """Convert a PDF (path or file-like object) into an LLM-friendly dict."""
    reader = PdfReader(file)
    meta = reader.metadata

    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        pages.append({"page": number, "text": text, "char_count": len(text)})

    return {
        "source": filename,
        "metadata": {
            "title": meta.title if meta else None,
            "author": meta.author if meta else None,
            "page_count": len(reader.pages),
        },
        "pages": pages,
    }
