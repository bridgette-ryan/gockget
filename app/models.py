from dataclasses import dataclass


# ----------------------------
# Data Model
# ----------------------------
# Note: Why TRUE / FALSE / ERROR
# FALSE = Never attempted yet
# TRUE  = Successfully downloaded
# ERROR = Attempted and failed
# ----------------------------

@dataclass
class ScrapeItem:
    url: str
    status: str = "FALSE"
    title: str = ""
    safe_title: str = ""

@dataclass
class LoadStats:
    total_rows: int = 0
    loaded: int = 0
    duplicates: int = 0
    ready: int = 0
    complete: int = 0
    errors: int = 0