"""
Inter-Process Communication (IPC) bus for Gideon Agentic OS.
Provides message queues, direct agent-to-agent pipes, and system broadcast channels.
"""

from typing import Dict, List, Any, Optional
from collections import deque
from datetime import datetime, timezone
import uuid

class IPCMessage:
    def __init__(
        self,
        sender_pid: int,
        target_pid: int,
        payload: Any,
        msg_type: str = "DATA",
        channel: Optional[str] = None
    ):
        self.msg_id: str = f"msg-{uuid.uuid4().hex[:8]}"
        self.sender_pid: int = sender_pid
        self.target_pid: int = target_pid
        self.payload: Any = payload
        self.msg_type: str = msg_type  # DATA, SIGNAL, RPC_REQ, RPC_RESP, BROADCAST
        self.channel: Optional[str] = channel
        self.timestamp: str = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "msg_id": self.msg_id,
            "sender_pid": self.sender_pid,
            "target_pid": self.target_pid,
            "msg_type": self.msg_type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }

class IPCBus:
    """
    Kernel Message Broker handling inter-agent queues and signal delivery.
    """
    def __init__(self, max_queue_size: int = 128):
        self.max_queue_size: int = max_queue_size
        self._mailboxes: Dict[int, deque] = {}
        self._subscribers: Dict[str, List[int]] = {}
        self._history: deque = deque(maxlen=200)

    def register_process(self, pid: int):
        if pid not in self._mailboxes:
            self._mailboxes[pid] = deque(maxlen=self.max_queue_size)

    def unregister_process(self, pid: int):
        self._mailboxes.pop(pid, None)
        for subscribers in self._subscribers.values():
            if pid in subscribers:
                subscribers.remove(pid)

    def send(self, sender_pid: int, target_pid: int, payload: Any, msg_type: str = "DATA") -> bool:
        if target_pid not in self._mailboxes:
            return False
        msg = IPCMessage(sender_pid, target_pid, payload, msg_type)
        self._mailboxes[target_pid].append(msg)
        self._history.append(msg)
        return True

    def receive(self, pid: int) -> Optional[IPCMessage]:
        if pid in self._mailboxes and self._mailboxes[pid]:
            return self._mailboxes[pid].popleft()
        return None

    def peek(self, pid: int) -> Optional[IPCMessage]:
        if pid in self._mailboxes and self._mailboxes[pid]:
            return self._mailboxes[pid][0]
        return None

    def broadcast(self, sender_pid: int, topic: str, payload: Any):
        subscribers = self._subscribers.get(topic, [])
        for sub_pid in subscribers:
            self.send(sender_pid, sub_pid, payload, msg_type="BROADCAST")

    def subscribe(self, pid: int, topic: str):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        if pid not in self._subscribers[topic]:
            self._subscribers[topic].append(pid)

    def get_history(self) -> List[Dict[str, Any]]:
        return [m.to_dict() for m in self._history]
