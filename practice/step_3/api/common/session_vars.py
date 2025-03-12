from contextvars import ContextVar

session_context: dict | None = ContextVar("session", default=dict())
