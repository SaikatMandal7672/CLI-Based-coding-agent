import os
import shutil
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import requests


def cur_time():
    return datetime.now()


def run_command(cmd: str):
    result = os.system(cmd)
    return result


def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."

    return "Something went wrong"

BASE_PATH = Path(".").resolve()

def set_base_path(path: str):
    """Set the base directory for all operations."""
    global BASE_PATH
    BASE_PATH = Path(path).resolve()
    print(f"✓ Base path set to: {BASE_PATH}")

def write_file(file_path: str, content: str, mode: str = 'w') -> bool:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file
        content: Content to write
        mode: Write mode ('w' for overwrite, 'a' for append)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        full_path = BASE_PATH / file_path
        with open(full_path, mode, encoding='utf-8') as f:
            f.write(content)
        action = "written to" if mode == 'w' else "appended to"
        print(f"✓ Content {action}: {full_path}")
        return True
    except Exception as e:
        print(f"✗ Error writing to file: {e}")
        return False


available_tools = {
    "current_time": cur_time,
    "run_command":run_command,
    "get_weather": get_weather,
    "write_file":write_file,
  
}