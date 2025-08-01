from fastapi import FastAPI, HTTPException
from pathlib import Path
from app.models import FileRequest
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

INPUT_DIR = Path(os.getenv("INPUT_PATH", "/input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_PATH", "/output"))


def justify_line(line: str, width: int) -> str:
    words = line.strip().split()
    if len(words) == 1:
        return words[0].ljust(width)
    total_spaces = width - sum(len(word) for word in words)
    gaps = len(words) - 1
    spaces = [total_spaces // gaps + (1 if i < total_spaces % gaps else 0) for i in range(gaps)]

    justified = ''.join(
        word + (' ' * spaces[i] if i < gaps else '') for i, word in enumerate(words)
    )
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


@app.post("/line-break")
def line_break(data: FileRequest):
    file_name = data.path
    width = data.width or 40

    if width <= 0 or width > 120:
        raise HTTPException(status_code=400, detail="Width must be between 1 and 120")

    file_path = INPUT_DIR / file_name

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

    justified_lines = []
    for paragraph in paragraphs:
        justified_lines.extend(justify_paragraph(paragraph, width))
        justified_lines.append("")

    if justified_lines and justified_lines[-1] == "":
        justified_lines.pop()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    final_path = OUTPUT_DIR / f"{file_name}_justify.txt"
    final_path.write_text('\n'.join(justified_lines), encoding="utf-8")

    return {"lines": justified_lines}
