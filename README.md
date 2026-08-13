# SCRIPTORUM

> *"Le scribe transcrit, l'Imperium juge."*

Bot de question/réponse qui tourne sur **GitHub Actions**. Tu poses une question
dans le chat, elle est déposée dans `questions/`, le workflow appelle le modèle
**GLM 5.2** chez **NVIDIA**, puis committe la réponse dans `answers/`
(fichier **Markdown** lisible + **JSON** structuré réutilisable).

## Architecture

```
.github/workflows/scriptorum.yml   # Workflow : questions/ → réponse → commit
questions/                          # Questions posées (une par fichier)
answers/                            # Réponses (une .md + une .json par question)
scripts/ask.py                      # Scribe : appelle l'API LLM
```

## Flux

1. **Poser une question** : créer `questions/question-YYYY-MM-DD-NN.md` contenant la question.
2. **GitHub Actions** détecte le push sur `questions/` et lance `scriptorum.yml`.
3. **`scripts/ask.py`** lit chaque question, appelle `z-ai/glm-5.2` (NVIDIA), écrit la réponse dans `answers/`.
4. Le workflow committe automatiquement les réponses sur le repo.

## Configuration

### 1. Clé API

Le workflow lit la clé depuis les **secrets du repo** :

| Secret | Valeur |
|--------|--------|
| `LLM_API_KEY` | Ta clé API NVIDIA (obligatoire) |
| `LLM_BASE_URL` | Optionnel, défaut `https://integrate.api.nvidia.com/v1` |
| `LLM_MODEL` | Optionnel, défaut `z-ai/glm-5.2` |

### 2. Fichier de question

```markdown
Question : Quelle est la meilleure façon de structurer un JSON ?
```

### 3. Résultat

Dans `answers/` :

- `question-YYYY-MM-DD-NN.md` — réponse lisible
- `question-YYYY-MM-DD-NN.json` — réponse structurée (question, réponse, modèle, date)

```json
{
  "name": "question-2026-08-13-01",
  "date": "2026-08-13",
  "model": "z-ai/glm-5.2",
  "provider": "https://integrate.api.nvidia.com/v1",
  "question": "...",
  "answer": "...",
  "generated_at": "2026-08-13T00:00:00+00:00"
}
```

## Test local

```bash
export LLM_API_KEY=nvapi-xxxx
python scripts/ask.py
```
