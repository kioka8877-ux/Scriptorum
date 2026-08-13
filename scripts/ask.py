#!/usr/bin/env python3
"""
SCRIPTORUM — Scribe de l'Imperium
Lit les questions dans questions/, appelle l'API LLM, écrit les réponses
dans answers/ (fichier Markdown + JSON structuré).

Configuration via variables d'environnement :
  LLM_API_KEY   (requis)
  LLM_BASE_URL  (défaut: https://integrate.api.nvidia.com/v1)
  LLM_MODEL     (défaut: z-ai/glm-5.2)
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = ROOT / "questions"
ANSWERS_DIR = ROOT / "answers"
QUESTION_PREFIX = "question-"

BASE_URL = (os.environ.get("LLM_BASE_URL") or "https://integrate.api.nvidia.com/v1").rstrip("/")
MODEL = os.environ.get("LLM_MODEL") or "z-ai/glm-5.2"
API_KEY = os.environ.get("LLM_API_KEY") or ""


def log(msg: str) -> None:
    print(f"[SCRIPTORUM] {msg}")


def read_question(path: Path) -> dict:
    """Extrait la question depuis un fichier Markdown."""
    content = path.read_text(encoding="utf-8").strip()
    question = content

    for line in content.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith(("question", "q :", "q:", "question :", "question:")):
            question = line.split(":", 1)[-1].strip() if ":" in line else content
            break

    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)

    return {
        "path": path,
        "name": path.stem,
        "date": date_match.group(1) if date_match else path.stem[:10],
        "question": question,
    }


def call_llm(question: str) -> str:
    """Appelle l'API LLM (format compatible OpenAI) et retourne la réponse."""
    if not API_KEY:
        log("ERREUR : LLM_API_KEY manquante.")
        sys.exit(1)

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": (
                "Tu es Scriptorum, scribe de l'Imperium de l'Homme. "
                "Tu réponds de manière précise, structurée et utile."
            )},
            {"role": "user", "content": question},
        ],
        "temperature": 0.7,
    }).encode("utf-8")

    req = request.Request(
        f"{BASE_URL}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    last_err = None
    for attempt in range(4):
        try:
            with request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code == 429:
                wait = 10 * (attempt + 1)
                log(f"Rate limit (429) — nouvel essai dans {wait}s...")
                time.sleep(wait)
                last_err = f"429: {body[:200]}"
                continue
            log(f"ERREUR API ({e.code}) : {body[:500]}")
            sys.exit(1)
        except error.URLError as e:
            log(f"ERREUR réseau : {e}")
            sys.exit(1)
    else:
        log(f"ERREUR : rate limit persisté — {last_err}")
        sys.exit(1)

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        log(f"ERREUR : réponse API inattendue : {data}")
        sys.exit(1)


def write_answer(meta: dict, answer: str) -> None:
    """Écrit les fichiers Markdown et JSON dans answers/."""
    now = datetime.now(timezone.utc).isoformat()

    md_path = ANSWERS_DIR / f"{meta['name']}.md"
    json_path = ANSWERS_DIR / f"{meta['name']}.json"

    md_content = f"""# {meta['name']}

> Date : {meta['date']} — Modèle : {MODEL}

## Question

{meta['question']}

## Réponse

{answer}

---
_Généré par SCRIPTORUM, scribe de l'Imperium._
"""
    json_content = {
        "name": meta["name"],
        "date": meta["date"],
        "model": MODEL,
        "provider": BASE_URL,
        "question": meta["question"],
        "answer": answer,
        "generated_at": now,
    }

    md_path.write_text(md_content, encoding="utf-8")
    json_path.write_text(json.dumps(json_content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"Écrit : {md_path.name} + {json_path.name}")


def main() -> None:
    if not QUESTIONS_DIR.exists():
        log(f"Dossier questions introuvable : {QUESTIONS_DIR}")
        sys.exit(1)

    ANSWERS_DIR.mkdir(parents=True, exist_ok=True)
    questions = sorted(QUESTIONS_DIR.glob(f"{QUESTION_PREFIX}*.md"))

    if not questions:
        log("Aucune question trouvée.")
        return

    answered = 0
    for path in questions:
        meta = read_question(path)

        answer_md = ANSWERS_DIR / f"{meta['name']}.md"
        if answer_md.exists():
            log(f"Skippé (déjà répondu) : {meta['name']}")
            continue

        log(f"Question : {meta['name']} — {meta['question'][:60]}...")
        answer = call_llm(meta["question"])
        write_answer(meta, answer)
        answered += 1

    log(f"Terminé : {answered} réponse(s) écrite(s) dans answers/.")


if __name__ == "__main__":
    main()
