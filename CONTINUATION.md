# CONTINUATION — Scriptorum + PERTURABO CLIPPING (mode meme)

> Point de reprise pour un nouveau chat vierge. Date : 2026-08-15.
> Mission active : analyser le démon viral @zdak pour définir la doctrine du mode meme PERTURABO, via Scriptorum (GitHub Actions).

## 1. Où on en est (état exact)

### Le projet
- **PERTURABO/MONDES_FORGES/CLIPPING** : forge de clips viraux (YouTube Shorts/TikTok/Insta). Cloné localement dans `/tmp/opencode/PERTURABO` (sparse MONDES_FORGES/CLIPPING).
- Profil actif : **logo**, sous-mode à concevoir : **meme** (en plus de informatif). Siège en cours : `siege_20260810_205150`, campagne **NBA_WESTBROOK** (backlash tribute Westbrook).
- **Scriptorum** : repo GitHub `kioka8877-ux/Scriptorum` — workflow qui lit une question dans `questions/`, appelle un LLM, commit la réponse dans `answers/` (.md + .json).

### Le démon analysé
- Canal **@zdak** (Kadz, US) : 2.42M abonnés, 9.56 Mds vues, 1723 vidéos, ~2 Shorts/jour, 5-9s, zéro dialogue.
- Vidéo cible : "This Teacher MIGHT Be Picasso 🫪🎨" — 6.8M vues en 24h, format "sad Twitter post x meme Paul (All Quiet)".
- Rapport Kimi K3 #1 terminé (identité, métriques, signature, angles meme) : `answers/question-2026-08-15-01.md`.

### Ce qui est EN COURS
- **Analyse de la construction visuelle** (dissection des couches : titre/haut, réaction, texte) pour définir ce que le mode meme DOIT contenir pour l'audience US jeune.
- Question : `questions/question-2026-08-15-02.md` (frames en `IMG:`).
- Frames extraites : `frames/f_01.jpg` → `f_11.jpg` (11 frames, ~0.5s entre chaque, vidéo 5.6s) — déjà poussées sur GitHub.
- Dernier run workflow : **https://github.com/kioka8877-ux/Scriptorum/actions/runs/31892765496**
- **Réponse attendue** : `answers/question-2026-08-15-02.md` (si le run réussit).

## 2. Configuration technique (déjà en place — NE PAS recasser)

### Clés (jamais afficher, jamais committer)
Stockées dans `/tmp/opencode/.env` (perms 600) et en **secrets GitHub** du repo Scriptorum :
| Secret GitHub | Valeur |
|---|---|
| `LLM_BASE_URL` | `https://openrouter.ai/api/v1` |
| `LLM_MODEL` | `google/gemma-4-31b-it:free` |
| `LLM_API_KEY` | clé OpenRouter `sk-or-v1-...` (du user) |

- Token GitHub (clone/push/API) : `/tmp/opencode/ghtoken` — **à révoquer** (exposé dans un chat précédent).
- La clé `kzRe48rg...` = clé Baseten (marche pour Kimi K3), PAS une clé Gemini.

### Fichiers modifiés dans Scriptorum
- `scripts/ask.py` :
  - `read_question()` : envoie **tout** le contenu de la question (plus seulement la 1re ligne).
  - `extract_images()` : lignes `IMG:<url>` → `image_url`.
  - `extract_videos()` : lignes `VIDEO:<url>` → `video_url`.
- `.github/workflows/scriptorum.yml` : inchangé (lit les 3 secrets).

## 3. Ce que le NOUVEAU chat doit faire (ordre exact)

### Étape 1 — Récupérer le résultat de l'analyse visuelle
```bash
cd /tmp/opencode/Scriptorum
git pull origin main
```
Lire `answers/question-2026-08-15-02.md`. Si le fichier n'existe pas :
1. Vérifier le dernier run Actions (lien ci-dessus) ; si échec → relancer `workflow_dispatch` (POST via API GitHub avec token).
2. Les runs précédents ont échoué pour : (a) 404 CDN sur `raw.githubusercontent.com` (propagation ~30s, maintenant OK), (b) rate limit 429 modèle gratuit (temporaire, relancer).

### Étape 2 — Si le run échoue encore (429)
- Attendre 60-120s puis relancer `workflow_dispatch`.
- Si ça persiste : passer le secret `LLM_MODEL` à un autre modèle gratuit vision : `google/gemma-4-26b-a4b-it:free` ou `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`.
- **ATTENTION** : OpenRouter exige un solde ≥ $1 pour `video_url`. Solution gratuite = frames en images (`IMG:`), PAS `VIDEO:`.

### Étape 3 — Consolider la doctrine du mode meme
À partir du rapport visuel (#2) + rapport Kimi K3 (#1), rédiger dans le repo PERTURABO :
- `MONDES_FORGES/CLIPPING/PROFILES/logo/manifest.json` : ajouter `sub_mode: "meme"`.
- `MONDES_FORGES/CLIPPING/CONTRACTS/production_pack_schema_logo.json` : étendre l'enum `sub_mode`.
- Nouveau guide : `MONDES_FORGES/CLIPPING/GUIDE_UTILISATION/04_MODE_MEME.md` (modèle : `01_MODE_LOGO_INFORMATIF.md`).
- Étendre les frégates : `F00_CAPTEURS/CODEBASE/capteurs.py` (entrée durée opérateur), `F02_TYRANT_CAMP/CODEBASE/anglesmith.py`, `F04_COPYWRITER/CODEBASE/copywriter.py`, `F05_PACKAGER/CODEBASE/packager.py`.

### Rappels de conception (décidés avec le user)
- Mode meme : PERTURABO = **texte only**. Chaque angle = 3 textes : `title` (haut), `tweet_text` (max 3 lignes), `reaction_text` (milieu, max 4 mots). + `emotion` (ajustable) + durée fourchette (demandée à l'opérateur F00/F01). **Pas** de timecodes, **pas** d'URL de meme.
- OMNIS_WATCH/Lacrimae = rendu vidéo + choix des vidéos meme. PERTURABO livre la directive émotion.
- Workflow meme F00 : scan par mot-clé → infos virales à potentiel humour (audience US) → skip analyse vidéo source → opérateur injecte humour → axes → 5 axes validés.

## 4. Fichiers clés locaux
| Fichier | Rôle |
|---|---|
| `/tmp/opencode/.env` | clés (Baseten, OpenRouter, YouTube) — jamais afficher |
| `/tmp/opencode/ghtoken` | token GitHub — à révoquer |
| `/tmp/opencode/demon_data.json` | données YouTube API du démon |
| `/tmp/opencode/frames/f_*.jpg` | frames extraites (copie locale) |
| `/tmp/opencode/demo.mp4` | vidéo du démon (5.6s, issue de la release) |
| `/tmp/opencode/Scriptorum/answers/question-2026-08-15-01.md` | rapport Kimi K3 #1 |
| `/tmp/opencode/Scriptorum/answers/question-2026-08-15-02.md` | **rapport attendu** (analyse visuelle) |
