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


def __init__(self, base_path: str = "."):
    """Initialize with a base directory path."""
    self.base_path = Path(base_path).resolve()


def create_folder(self, folder_path: str) -> bool:
    """
    Create a new folder.

    Args:
        folder_path: Path to the folder to create

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        full_path = self.base_path / folder_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Folder created: {full_path}")
        return True
    except Exception as e:
        print(f"✗ Error creating folder: {e}")
        return False


def create_file(self, file_path: str, content: str = "") -> bool:
    """
    Create a new file with optional content.

    Args:
        file_path: Path to the file to create
        content: Initial content for the file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        full_path = self.base_path / file_path
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ File created: {full_path}")
        return True
    except Exception as e:
        print(f"✗ Error creating file: {e}")
        return False


def write_file(self, file_path: str, content: str, mode: str = "w") -> bool:
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
        full_path = self.base_path / file_path
        with open(full_path, mode, encoding="utf-8") as f:
            f.write(content)
        action = "written to" if mode == "w" else "appended to"
        print(f"✓ Content {action}: {full_path}")
        return True
    except Exception as e:
        print(f"✗ Error writing to file: {e}")
        return False


def read_file(self, file_path: str) -> Optional[str]:
    """
    Read content from a file.

    Args:
        file_path: Path to the file to read

    Returns:
        str: File content, or None if error
    """
    try:
        full_path = self.base_path / file_path
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"✓ File read: {full_path}")
        return content
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return None


def append_to_file(self, file_path: str, content: str) -> bool:
    """
    Append content to a file.

    Args:
        file_path: Path to the file
        content: Content to append

    Returns:
        bool: True if successful, False otherwise
    """
    return self.write_file(file_path, content, mode="a")


def modify_file_line(self, file_path: str, line_number: int, new_content: str) -> bool:
    """
    Modify a specific line in a file.

    Args:
        file_path: Path to the file
        line_number: Line number to modify (1-based)
        new_content: New content for the line

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        full_path = self.base_path / file_path

        # Read all lines
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Check if line number is valid
        if line_number < 1 or line_number > len(lines):
            print(f"✗ Invalid line number: {line_number}")
            return False

        # Modify the line
        lines[line_number - 1] = (
            new_content + "\n" if not new_content.endswith("\n") else new_content
        )

        # Write back to file
        with open(full_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"✓ Line {line_number} modified in: {full_path}")
        return True
    except Exception as e:
        print(f"✗ Error modifying file line: {e}")
        return False


def delete_file(self, file_path: str) -> bool:
    """
    Delete a file.

    Args:
        file_path: Path to the file to delete

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        full_path = self.base_path / file_path
        full_path.unlink()
        print(f"✓ File deleted: {full_path}")
        return True
    except Exception as e:
        print(f"✗ Error deleting file: {e}")
        return False


def delete_folder(self, folder_path: str, force: bool = False) -> bool:
    """
    Delete a folder.

    Args:
        folder_path: Path to the folder to delete
        force: If True, delete non-empty folders

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        full_path = self.base_path / folder_path

        if force:
            shutil.rmtree(full_path)
        else:
            full_path.rmdir()  # Only works on empty directories

        print(f"✓ Folder deleted: {full_path}")
        return True
    except Exception as e:
        print(f"✗ Error deleting folder: {e}")
        return False


def list_contents(self, folder_path: str = ".") -> List[str]:
    """
    List contents of a folder.

    Args:
        folder_path: Path to the folder to list

    Returns:
        List[str]: List of folder contents
    """
    try:
        full_path = self.base_path / folder_path
        contents = []

        for item in full_path.iterdir():
            item_type = "📁" if item.is_dir() else "📄"
            contents.append(f"{item_type} {item.name}")

        print(f"Contents of {full_path}:")
        for item in contents:
            print(f"  {item}")

        return contents
    except Exception as e:
        print(f"✗ Error listing contents: {e}")
        return []


def copy_file(self, source_path: str, destination_path: str) -> bool:
    """
    Copy a file from source to destination.

    Args:
        source_path: Source file path
        destination_path: Destination file path

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        src = self.base_path / source_path
        dst = self.base_path / destination_path

        # Create destination directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src, dst)
        print(f"✓ File copied from {src} to {dst}")
        return True
    except Exception as e:
        print(f"✗ Error copying file: {e}")
        return False


def move_file(self, source_path: str, destination_path: str) -> bool:
    """
    Move a file from source to destination.

    Args:
        source_path: Source file path
        destination_path: Destination file path

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        src = self.base_path / source_path
        dst = self.base_path / destination_path

        # Create destination directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(src), str(dst))
        print(f"✓ File moved from {src} to {dst}")
        return True
    except Exception as e:
        print(f"✗ Error moving file: {e}")
        return False


def file_exists(self, file_path: str) -> bool:
    """Check if a file exists."""
    return (self.base_path / file_path).exists()


def folder_exists(self, folder_path: str) -> bool:
    """Check if a folder exists."""
    return (self.base_path / folder_path).is_dir()


def get_file_info(self, file_path: str) -> Optional[dict]:
    """
    Get information about a file.

    Args:
        file_path: Path to the file

    Returns:
        dict: File information or None if error
    """
    try:
        full_path = self.base_path / file_path
        stat = full_path.stat()

        info = {
            "name": full_path.name,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "is_file": full_path.is_file(),
            "is_dir": full_path.is_dir(),
            "absolute_path": str(full_path),
        }

        return info
    except Exception as e:
        print(f"✗ Error getting file info: {e}")
        return None


available_tools = {
    "current_time": cur_time,
    "run_command":run_command,
    "get_weather": get_weather,
    "initialise_base": __init__,
    "create_folder": create_folder,
    "create_file": create_file,
    "write_file":write_file,
    "read_file":read_file,
    "append_to_file":append_to_file,
    "modify_file_line":modify_file_line,
    "delete_file":delete_file,
    "delete_folder":delete_folder,
    "list_contents":list_contents,
    "copy_file" : copy_file,
    "move_file":move_file,
    "file_exists":file_exists,
    "folder_exists":folder_exists
}
