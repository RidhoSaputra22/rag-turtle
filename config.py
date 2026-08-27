from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


# DEBUG MODE

DEBUG_MODE = True

# =============================
# OLLAMA
# =============================

LLM_MODEL = "gemma4"

EMBED_MODEL = "embeddinggemma"


# =============================
# RAG
# =============================

CHROMA_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "turtle_knowledge"

KNOWLEDGE_PATH = BASE_DIR / "knowledge"

TOP_K = 4


# =============================
# PROMPT
# =============================

SKILL_PATH = (
    BASE_DIR
    / "prompts"
    / "skill.md"
)


# =============================
# AGENT
# =============================

MAX_RETRIES = 2


# =============================
# TURTLE
# =============================

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700