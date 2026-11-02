"""
Virtual Filesystem (VFS) Driver for Gideon Agentic OS.
Provides sandboxed process file I/O within the workspace volume.
"""

from pathlib import Path
from typing import Dict, Any, List
from gideon.drivers.base import BaseDriver

class FilesystemDriver(BaseDriver):
    def __init__(self, workspace_root: Path):
        super().__init__("GIDEON_VFS_DRIVER")
        self.workspace_root = workspace_root.resolve()

    def initialize(self) -> bool:
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        self.is_active = True
        return True

    def _resolve_safe_path(self, relative_path: str) -> Path:
        target = (self.workspace_root / relative_path).resolve()
        if not str(target).startswith(str(self.workspace_root)):
            raise PermissionError(f"Access denied: path traversal out of sandbox: {relative_path}")
        return target

    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        if command == "read":
            rel_path = kwargs.get("path", "")
            safe_p = self._resolve_safe_path(rel_path)
            if not safe_p.exists():
                return {"ok": False, "error": f"File not found: {rel_path}"}
            content = safe_p.read_text(encoding="utf-8")
            return {"ok": True, "content": content, "bytes": len(content)}

        elif command == "write":
            rel_path = kwargs.get("path", "")
            content = kwargs.get("content", "")
            safe_p = self._resolve_safe_path(rel_path)
            safe_p.parent.mkdir(parents=True, exist_ok=True)
            safe_p.write_text(content, encoding="utf-8")
            return {"ok": True, "path": rel_path, "bytes": len(content)}

        elif command == "list":
            rel_path = kwargs.get("path", "")
            safe_p = self._resolve_safe_path(rel_path)
            if not safe_p.exists() or not safe_p.is_dir():
                return {"ok": False, "error": f"Directory not found: {rel_path}"}
            items = [p.name for p in safe_p.iterdir()]
            return {"ok": True, "items": items}

        return {"ok": False, "error": f"Unsupported VFS command: {command}"}
