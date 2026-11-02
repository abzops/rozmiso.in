import os
from pathlib import Path
from dotenv import load_dotenv

# Load local environment if present
base_dir = Path(__file__).resolve().parent
load_dotenv(base_dir / ".env")
load_dotenv(base_dir.parent / "open-dots" / "server" / ".env")

class GideonConfig:
    OS_NAME: str = "Gideon Agentic OS"
    OS_VERSION: str = "0.1.0-alpha (POC)"
    
    BASE_DIR: Path = base_dir
    DATA_DIR: Path = base_dir / "data"
    WORKSPACE_DIR: Path = base_dir / "workspace"
    
    # LLM Inference Hardware / Driver API
    NVIDIA_API_KEY: str = os.getenv(
        "NVIDIA_API_KEY",
        os.getenv("MODEL_API_KEY", "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")
    )
    NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "meta/llama-3.2-11b-vision-instruct")
    
    # Kernel & Scheduler Tunables
    MAX_PROCESSES: int = 16
    MAX_TOKENS_PER_STEP: int = 2048
    SCHEDULER_INTERVAL_SEC: float = 0.1
    IPC_MAX_QUEUE_SIZE: int = 128
    
    # Web Telemetry
    HOST: str = "127.0.0.1"
    PORT: int = 8080

    def __init__(self):
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

config = GideonConfig()
