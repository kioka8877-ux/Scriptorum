# CONTINUATION — Scriptorum + PERTURABO CLIPPING (mode meme)

> Point de reprise pour un nouveau chat vierge. Date : 2026-08-15.
> Mission active : analyser le démon viral @zdak pour définir la doctrine du mode meme PERTURABO, via Scriptorum (GitHub Actions).

## 0. OÙ ON EST — les 2 rapports sont TERMINÉS ✅

### Rapport 1 — Analyse du démon (Kimi K3, fait)
`answers/question-2026-08-15-01.md` : identité @zdak, métriques (2.42M abonnés, 9.56 Mds vues, ~2 Shorts/jour), signature "sad Twitter post x meme Paul", 5 axes de pack meme (axe "born to be / forced to be" pré-validé par le top commentaire à 2651 likes).

### Rapport 2 — Dissection visuelle de la vidéo (Kimi K3, fait) ⭐
`answers/question-2026-08-15-02.md` : analyse frame par frame de la vidéo cible. **Doctrine du mode meme en 6 couches** :
1. Setup / faux post (quart haut, fixe, max 1.5 ligne, mots-clés colorés vert/rouge)
2. Preuve visuelle (card fixe, lumineuse dès f_01)
3. Label narratif `[sujet] at [A]:` → `[sujet] at [B]:` (un seul mot change, ~50% par version)
4. Réacteur émotionnel (2 clips contraste extrême d'une même œuvre pop-culture pour méta-blague)
5. Transition-pivot (flash/cut sec + impact sonore à 50-55% du runtime)
6. Watermark (semi-transparent, bas-gauche)

Règles d'assemblage : 5-7s max · tout visible dès frame 1 · une seule bascule · muet-compréhensible · un seul objet en mouvement · boucle invisible en bonus.

**Le rapport complet est déjà transcrit dans le chat précédent** (dissection + forces + faiblesses + doctrine + conclusion).

## 1. Où on en est (état exact)

### Le projet
- **PERTURABO/MONDES_FORGES/CLIPPING** : forge de clips viraux (YouTube Shorts/TikTok/Insta). Cloné localement dans `/tmp/opencode/PERTURABO` (sparse MONDES_FORGES/CLIPPING).
- Profil actif : **logo**, sous-mode à concevoir : **meme** (en plus de informatif). Siège en cours : `siege_20260810_205150`, campagne **NBA_WESTBROOK** (backlash tribute Westbrook).
- **Scriptorum** : repo GitHub `kioka8877-ux/Scriptorum` — workflow qui lit une question dans `questions/`, appelle un LLM, commit la réponse dans `answers/` (.md + .json).

### Le démon analysé
- Canal **@zdak** (Kadz, US) : 2.42M abonnés, 9.56 Mds vues, 1723 vidéos, ~2 Shorts/jour, 5-9s, zéro dialogue.
- Vidéo cible : "This Teacher MIGHT Be Picasso 🫪🎨" — 6.8M vues en 24h, format "sad Twitter post x meme Paul (All Quiet)".
- Rapport Kimi K3 #1 terminé (identité, métriques, signature, angles meme) : `answers/question-2026-08-15-01.md`.

### Ce qui est TERMINÉ
- **Rapport Kimi K3 #1** (démon complet) : `answers/question-2026-08-15-01.md`.
- **Rapport Kimi K3 #2** (dissection visuelle + doctrine 6 couches) : `answers/question-2026-08-15-02.md`.
- Question #2 : `questions/question-2026-08-15-02.md` (frames en `IMG:`).
- Frames extraites : `frames/f_01.jpg` → `f_11.jpg` (11 frames, ~0.5s entre chaque, vidéo 5.6s) — poussées sur GitHub.
- Note de continuation : `CONTINUATION.md` (ce fichier).
- Dernier run workflow (SUCCÈS) : **https://github.com/kioka8877-ux/Scriptorum/actions/runs/31894023578**
- Réponse livrée : `answers/question-2026-08-15-02.md`.

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

### Étape 3 — Consolider la doctrine du mode meme ⬅️ PROCHAINE ÉTAPE
Les 2 analyses sont terminées. La doctrine visuelle est définie (section 0). Il reste à l'implémenter dans le repo PERTURABO :
- `MONDES_FORGES/CLIPPING/PROFILES/logo/manifest.json` : ajouter `sub_mode: "meme"`.
- `MONDES_FORGES/CLIPPING/CONTRACTS/production_pack_schema_logo.json` : étendre l'enum `sub_mode`.
- Nouveau guide : `MONDES_FORGES/CLIPPING/GUIDE_UTILISATION/04_MODE_MEME.md` (modèle : `01_MODE_LOGO_INFORMATIF.md`) — intégrer les 6 couches + règles d'assemblage du rapport 2.
- Étendre les frégates : `F00_CAPTEURS/CODEBASE/capteurs.py` (scan YouTube virality par mot-clé SANS téléchargement), `F02_TYRANT_CAMP/CODEBASE/anglesmith.py`, `F04_COPYWRITER/CODEBASE/copywriter.py`, `F05_PACKAGER/CODEBASE/packager.py` (pack = textes + emotion + durée + règles de montage). **F01 non utilisé en mode meme.**

### Rappels de conception (décidés avec le user) — WORKFLOW MODE MEME RÉVISÉ ⭐
- **Pack = aspects textuels + référence aux règles de montage.** Le pack référence le guide `04_MODE_MEME.md` (réponse user : "Référence au guide 04_MODE_MEME.md" — PAS de bloc JSON dupliqué). OMNIS_WATCH charge le guide pour le rendu.
- **Workflow** :
  1. Opérateur fournit le **mot-clé** → **F00** scanne la viralité sur **TOUTES les sources** (YouTube + Google Trends + RSS + Reddit + Twitter + toute source disant ce qui est viral US et ce qui marchera en Shorts), SANS télécharger de clip.
  2. **F02** sort **5 angles** → chacun avec une **émotion** (différente entre angles, ou identique si nécessaire — **règle anti-spam**, à fixer).
  3. **F04** génère : **fake tweet**, **titre en haut** (si nécessaire), **texte d'émotion**.
  4. **F05** assemble le **pack dans EXPORT** : textes + emotion + durée fourchette + référence guide montage.
  5. **F01 et F03 sont SKIP** : pas de timecodes/segments. F03 (sélection segments vidéos longues) dépendait de F01 (assets+transcripts) — sans clip fourni, il n'a rien à sélectionner. Son rôle est remplacé par les règles de montage génériques du guide.
  6. **OMNIS_WATCH** récupère le pack dans EXPORT (via demonwatch) pour rendre la vidéo et sortir les vues.
- **Clé premium** : les **3 clés** disponibles (Kimi K3/Baseten, OpenRouter, NVIDIA nvapi) — utiliser selon disponibilité. Kimi K3/Baseten = référence testée et fonctionnelle.
- Chaque angle = 3 textes : `title` (haut), `tweet_text` (max 3 lignes), `reaction_text` (milieu, max 4 mots) + `emotion` (ajustable) + durée fourchette (demandée à l'opérateur F00/F01).
- **Pas** de timecodes, **pas** d'URL de meme dans le pack.

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
