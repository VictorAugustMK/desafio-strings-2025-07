import pytest
from pathlib import Path
from app.services.text_processor import process_text_file
from app.config import INPUT_DIR, OUTPUT_DIR

@pytest.fixture(autouse=True)
def setup_and_teardown():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for f in OUTPUT_DIR.glob("*"):
        f.unlink()

    yield

    for f in OUTPUT_DIR.glob("*"):
        f.unlink()


def test_process_file():
    test_file = INPUT_DIR / "test.txt"
    test_file.write_text(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        encoding="utf-8"
    )

    lines = process_text_file(width=40)

    output_file = OUTPUT_DIR / "teste_quebrado.txt"
    assert output_file.exists()

    assert all(len(line) <= 40 for line in lines if line.strip() != "")

def test_process_multiple_paragraphs():
    text = "Primeiro parágrafo.\n\nSegundo parágrafo com mais texto."
    test_file = INPUT_DIR / "test_paragraphs.txt"
    test_file.write_text(text, encoding="utf-8")

    lines = process_text_file("test_paragraphs.txt", width=40)

    assert "" in lines

    joined = "\n".join(lines)
    assert "Primeiro parágrafo." in joined
    assert "Segundo parágrafo" in joined

def test_process_empty_file():
    test_file = INPUT_DIR / "test_empty.txt"
    test_file.write_text("", encoding="utf-8")

    lines = process_text_file("test_empty.txt", width=40)

    assert lines == [""]

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        process_text_file("arquivo_inexistente.txt", width=40)

