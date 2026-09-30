from utils.validators import valid_pdf, valid_positive_number


def test_positive_number():
    assert valid_positive_number("5")
    assert not valid_positive_number("-1")


def test_pdf_extension(tmp_path):
    pdf = tmp_path / "notes.pdf"
    txt = tmp_path / "notes.txt"
    pdf.write_text("sample")
    txt.write_text("sample")
    assert valid_pdf(str(pdf))
    assert not valid_pdf(str(txt))
