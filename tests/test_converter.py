import io
import json

from fpdf import FPDF

from converter import pdf_to_json


def make_pdf(pages, title=None, author=None) -> io.BytesIO:
    """Build an in-memory PDF. Each item in `pages` is one page's text; "" means a blank page."""
    pdf = FPDF()
    if title:
        pdf.set_title(title)
    if author:
        pdf.set_author(author)
    for text in pages:
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        if text:
            pdf.cell(text=text)
    return io.BytesIO(pdf.output())


def test_extracts_text_per_page():
    result = pdf_to_json(make_pdf(["Hello page one", "Second page"]), "doc.pdf")

    assert result["source"] == "doc.pdf"
    assert result["metadata"]["page_count"] == 2
    assert [p["page"] for p in result["pages"]] == [1, 2]
    assert result["pages"][0]["text"] == "Hello page one"
    assert result["pages"][1]["char_count"] == len("Second page")


def test_reads_metadata():
    result = pdf_to_json(make_pdf(["x"], title="My Title", author="Phil"), "doc.pdf")

    assert result["metadata"]["title"] == "My Title"
    assert result["metadata"]["author"] == "Phil"


def test_missing_metadata_is_none():
    result = pdf_to_json(make_pdf(["x"]), "doc.pdf")

    assert result["metadata"]["title"] is None
    assert result["metadata"]["author"] is None


def test_output_is_json_serializable():
    result = pdf_to_json(make_pdf(["Hello"]), "doc.pdf")

    assert json.loads(json.dumps(result)) == result