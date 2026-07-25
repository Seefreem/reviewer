import json
import os
from datetime import datetime, timezone
from pathlib import Path


METADATA_SUFFIX = ".meta.json"


def metadata_path(vocabulary_path):
    """Return the sidecar metadata path for a vocabulary JSON file."""
    path = Path(vocabulary_path)
    return path.with_name(path.stem + METADATA_SUFFIX)


def default_metadata(vocabulary_path):
    """Build metadata for an existing vocabulary file without a sidecar."""
    path = Path(vocabulary_path)
    return {
        "title": path.stem,
        "description": "",
        "sourceLanguage": "English",
        "targetLanguage": "Chinese",
        "tags": [],
        "version": 1,
    }


def load_vocabulary(vocabulary_path):
    """Load and validate a vocabulary file and its optional metadata sidecar."""
    path = Path(vocabulary_path)
    with path.open("r", encoding="utf-8") as vocabulary_file:
        objects = json.load(vocabulary_file)
    if not isinstance(objects, list):
        raise ValueError("单词表文件的顶层内容必须是 JSON 数组。")

    metadata = default_metadata(path)
    sidecar = metadata_path(path)
    if sidecar.exists():
        with sidecar.open("r", encoding="utf-8") as metadata_file:
            saved_metadata = json.load(metadata_file)
        if not isinstance(saved_metadata, dict):
            raise ValueError("单词本元数据必须是 JSON 对象。")
        metadata.update(saved_metadata)
    return objects, metadata


def create_vocabulary(vocabulary_path, metadata):
    """Create an empty vocabulary JSON file and its metadata sidecar."""
    path = Path(vocabulary_path)
    if path.suffix.lower() != ".json":
        path = path.with_suffix(".json")
    if path.name.endswith(METADATA_SUFFIX):
        raise ValueError("单词表文件名不能以 .meta.json 结尾。")
    if path.exists():
        raise FileExistsError("该单词表文件已经存在。")

    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    complete_metadata = default_metadata(path)
    complete_metadata.update(metadata)
    complete_metadata["title"] = str(complete_metadata.get("title", "")).strip() or path.stem
    complete_metadata["tags"] = _normalise_tags(complete_metadata.get("tags", []))
    complete_metadata["version"] = 1
    complete_metadata["createdAt"] = now
    complete_metadata["updatedAt"] = now

    _atomic_json_write(path, [])
    try:
        _atomic_json_write(metadata_path(path), complete_metadata)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return str(path.resolve()), complete_metadata


def save_metadata(vocabulary_path, metadata):
    """Write metadata for a vocabulary file, preserving its creation date."""
    path = Path(vocabulary_path)
    complete_metadata = default_metadata(path)
    complete_metadata.update(metadata)
    complete_metadata["tags"] = _normalise_tags(complete_metadata.get("tags", []))
    complete_metadata["version"] = 1
    complete_metadata["updatedAt"] = datetime.now(timezone.utc).isoformat()
    _atomic_json_write(metadata_path(path), complete_metadata)
    return complete_metadata


def _normalise_tags(tags):
    if isinstance(tags, str):
        tags = tags.split(";")
    return [str(tag).strip() for tag in tags if str(tag).strip()]


def _atomic_json_write(path, data):
    path = Path(path)
    temporary_path = path.with_name("." + path.name + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")
            output_file.flush()
            os.fsync(output_file.fileno())
        os.replace(str(temporary_path), str(path))
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
