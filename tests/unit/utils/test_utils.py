import os
import tempfile
from datetime import datetime

from bosskit.utils import (
    format_datetime,
    format_duration,
    format_size,
    get_cpu_info,
    get_disk_usage,
    get_file_extension,
    get_file_hash,
    get_file_size,
    get_line_count,
    get_memory_usage,
    get_system_info,
    is_binary_file,
    read_file,
    truncate_text,
    write_file,
)


def test_file_operations():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"test content")
        tmp_path = tmp.name

    try:
        # Test write_file
        write_file(tmp_path, "new content")
        assert read_file(tmp_path) == "new content"

        # Test get_file_extension
        assert get_file_extension(tmp_path) == os.path.splitext(tmp_path)[1]

        # Test is_binary_file
        assert not is_binary_file(tmp_path)

        # Test get_file_size
        assert get_file_size(tmp_path) > 0

        # Test get_file_hash
        hash1 = get_file_hash(tmp_path)
        write_file(tmp_path, "different content")
        hash2 = get_file_hash(tmp_path)
        assert hash1 != hash2
    finally:
        os.unlink(tmp_path)


def test_string_utils():
    # Test truncate_text
    assert truncate_text("short text", 10) == "short text"
    assert truncate_text("very long text that needs to be truncated", 10) == "very long..."

    # Test format_size
    assert format_size(1024) == "1.0 KB"
    assert format_size(1024 * 1024) == "1.0 MB"
    assert format_size(1024 * 1024 * 1024) == "1.0 GB"

    # Test format_duration
    assert format_duration(60) == "1 minute"
    assert format_duration(3600) == "1 hour"
    assert format_duration(86400) == "1 day"

    # Test format_datetime
    now = datetime.now()
    assert format_datetime(now) == now.strftime("%Y-%m-%d %H:%M:%S")

    # Test get_line_count
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"line1\nline2\nline3")
        tmp_path = tmp.name

    try:
        assert get_line_count(tmp_path) == 3
    finally:
        os.unlink(tmp_path)


def test_system_utils():
    # Test get_system_info
    info = get_system_info()
    assert isinstance(info, dict)
    assert "platform" in info
    assert "python_version" in info

    # Test get_memory_usage
    mem = get_memory_usage()
    assert isinstance(mem, dict)
    assert "total" in mem
    assert "used" in mem

    # Test get_cpu_info
    cpu = get_cpu_info()
    assert isinstance(cpu, dict)
    assert "count" in cpu

    # Test get_disk_usage
    disk = get_disk_usage("/")
    assert isinstance(disk, dict)
    assert "total" in disk
    assert "used" in disk
    assert "free" in disk


def test_hash_functions():
    # Test get_file_hash with different algorithms
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"test content")
        tmp_path = tmp.name

    try:
        assert get_file_hash(tmp_path, algorithm="md5") != get_file_hash(tmp_path, algorithm="sha256")
        assert get_file_hash(tmp_path, algorithm="sha1") != get_file_hash(tmp_path, algorithm="sha256")
    finally:
        os.unlink(tmp_path)
