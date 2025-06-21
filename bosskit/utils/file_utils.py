import hashlib
import json
import os
import pickle
from pathlib import Path
from typing import Any, Optional

import yaml


def read_file(path: str, encoding: str = 'utf-8') -> str:
    """Read content from a file.

    Args:
        path: Path to the file
        encoding: File encoding (default: utf-8)

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file does not exist
        IOError: If file cannot be read
    """
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Error reading file {path}: {str(e)}")

def write_file(path: str, content: str, encoding: str = 'utf-8') -> None:
    """Write content to a file.

    Args:
        path: Path to the file
        content: Content to write
        encoding: File encoding (default: utf-8)

    Raises:
        IOError: If file cannot be written
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"Error writing to file {path}: {str(e)}")

def get_file_extension(path: str) -> str:
    """Get file extension from path.

    Args:
        path: Path to the file

    Returns:
        File extension (including leading .)
    """
    return Path(path).suffix

def is_binary_file(path: str) -> bool:
    """Check if a file is binary.

    Args:
        path: Path to the file

    Returns:
        True if file is binary, False otherwise
    """
    try:
        with open(path, 'rb') as f:
            content = f.read(1024)
            return b'\0' in content
    except Exception:
        return False

def get_file_size(path: str) -> int:
    """Get file size in bytes.

    Args:
        path: Path to the file

    Returns:
        File size in bytes
    """
    return os.path.getsize(path)

def get_file_hash(path: str, algorithm: str = 'sha256') -> str:
    """Get file hash.

    Args:
        path: Path to the file
        algorithm: Hash algorithm (default: sha256)

    Returns:
        Hexadecimal hash string
    """
    hash_func = getattr(hashlib, algorithm, None)
    if not hash_func:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    h = hash_func()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()

def read_json(path: str) -> Any:
    """Read JSON file.

    Args:
        path: Path to the JSON file

    Returns:
        Parsed JSON data

    Raises:
        ValueError: If JSON is invalid
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(path: str, data: Any, indent: int = 2) -> None:
    """Write data to JSON file.

    Args:
        path: Path to the JSON file
        data: Data to write
        indent: Number of spaces for indentation
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)

def read_yaml(path: str) -> Any:
    """Read YAML file.

    Args:
        path: Path to the YAML file

    Returns:
        Parsed YAML data

    Raises:
        ValueError: If YAML is invalid
    """
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def write_yaml(path: str, data: Any) -> None:
    """Write data to YAML file.

    Args:
        path: Path to the YAML file
        data: Data to write
    """
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)

def read_pickle(path: str) -> Any:
    """Read Pickle file.

    Args:
        path: Path to the Pickle file

    Returns:
        Unpickled data
    """
    with open(path, 'rb') as f:
        return pickle.load(f)

def write_pickle(path: str, data: Any) -> None:
    """Write data to Pickle file.

    Args:
        path: Path to the Pickle file
        data: Data to write
    """
    with open(path, 'wb') as f:
        pickle.dump(data, f)
