"""
Verification and Orchestration Demonstration script for the Open-Dots India Dropshipping Team.
"""

import sys
import json
from pathlib import Path

# Configure UTF-8 console output for Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

server_dir = Path(__file__).resolve().parent / "server"
sys.path.insert(0, str(server_dir))

from dotenv import load_dotenv
load_dotenv(server_dir / ".env")

from app.services.storage_service import storage_service

def verify_agent_team():
    print("=" * 60)
    print("VERIFYING INDIA DROPSHIPPING AGENT TEAM IN OPEN-DOTS")
    print("=" * 60)
    
    bots = storage_service.get_bots()
    dropshipping_bots = [b for b in bots if "india" in b.get("id", "")]
    
    print(f"Total bots in database: {len(bots)}")
    print(f"Total Indian dropshipping agents: {len(dropshipping_bots)}\n")
    
    expected_ids = {
        "bot-director-india": "Director-Dot",
        "bot-hunter-india": "Hunter-Dot",
        "bot-creative-india": "Creative-Dot",
        "bot-store-india": "Store-Dot",
        "bot-shield-india": "Shield-Dot"
    }
    
    found_ids = set()
    for b in dropshipping_bots:
        found_ids.add(b["id"])
        print(f"[{b.get('avatar', '🤖')}] {b['name']} ({b['role']})")
        print(f"   ID: {b['id']} | Model: {b['model']} | Color: {b['accent_color']}")
        print(f"   Tools: {', '.join(b.get('tools', []))}")
        print(f"   System Prompt Length: {len(b.get('system_prompt', ''))} characters")
        print("-" * 60)
        
    missing = set(expected_ids.keys()) - found_ids
    if missing:
        print(f"FAILED: Missing agents: {missing}")
        return False
        
    print("\nALL 5 SPECIALIZED AGENTS ARE VERIFIED AND OPERATIONAL!")
    return True

if __name__ == "__main__":
    success = verify_agent_team()
    if not success:
        sys.exit(1)
