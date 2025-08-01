
from app.config import INPUT_DIR, OUTPUT_DIR
import os
import re

def justify_line(line: str, width: int) -> str:
    words = line.split()
    if len(words) <= 2:
        return " ".join(words).ljust(width)

    total_spaces = width - sum(len(word) for word in words)
    gaps = len(words) - 1

    space_between_words, extra = divmod(total_spaces, gaps)

    justified = ""
    for i, word in enumerate(words[:-1]):
        justified += word + " " * (space_between_words + (1 if i < extra else 0))
    justified += words[-1]
    return justified

def justify_paragraph(paragraph: str, width: int) -> list[str]:
    words = paragraph.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) <= width:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(justify_line(current_line, width))
            current_line = word

    if current_line:
        lines.append(current_line.ljust(width))

    return lines

def process_text_file(filename: str = "", width: int | None = None) -> list[str]:
    if not width or width <= 0:
        width = 40

    if not filename:
        file_path = next(INPUT_DIR.glob("*.txt"), None)
        if not file_path:
            raise FileNotFoundError("Nenhum arquivo .txt encontrado na pasta de entrada.")
    else:
        file_path = INPUT_DIR / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo '{filename}' não encontrado em {INPUT_DIR}.")

    text = file_path.read_text(encoding="utf-8")

    raw_paragraphs = text.split("\n\n")
    normalized_paragraphs = [re.sub(r'\s+', ' ', p.strip()) for p in raw_paragraphs]

    lines = []
    for paragraph in normalized_paragraphs:
        lines.extend(justify_paragraph(paragraph, width))
        lines.append("")

    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    base_name = file_path.stem
    output_file = OUTPUT_DIR / f"{base_name}_quebrado.txt"
    output_file.write_text("\n".join(lines), encoding="utf-8")

    return lines

