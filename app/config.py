import os
from dotenv import load_dotenv
from pathlib import Path

env_file = ".env.test" if os.getenv("ENV") == "test" else ".env"
load_dotenv(dotenv_path=env_file)

INPUT_DIR = Path(os.getenv("INPUT_PATH", "input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_PATH", "output"))
DEFAULT_WIDTH = int(os.getenv("DEFAULT_WIDTH", 40))
