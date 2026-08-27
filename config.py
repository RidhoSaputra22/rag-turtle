from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


# DEBUG MODE

DEBUG_MODE = True

# =============================
# OLLAMA
# =============================

LLM_MODEL = "qwen3:0.6b"

EMBED_MODEL = "embeddinggemma"


# =============================
# RAG
# =============================

CHROMA_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "turtle_knowledge"

KNOWLEDGE_PATH = BASE_DIR / "knowledge"

TOP_K = 8


# =============================
# PROMPT
# =============================

SKILL_PATH = (
    BASE_DIR
    / "prompts"
    / "skill.md"
)

PLAN_SKILL_PATH = (
    BASE_DIR
    / "prompts"
    / "plan.md"
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
