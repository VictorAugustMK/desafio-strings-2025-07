from pathlib import Path
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os

from app.main import app

load_dotenv(dotenv_path=".env.test")

client = TestClient(app)


def test_line_break_default_width():
    input_dir = Path(os.getenv("INPUT_PATH", "tests/input"))
    output_dir = Path(os.getenv("OUTPUT_PATH", "tests/output"))
    test_filename = os.getenv("TEST_FILENAME", "teste.txt")

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = input_dir / test_filename
    file_path.write_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
                         "incididunt ut labore et dolore magna aliqua.", encoding="utf-8")

    response = client.post("/line-break", json={"path": test_filename})

    assert response.status_code == 200
    assert "lines" in response.json()
