# iA_GPT_Zero_obstacle

Base de travail pour l'orchestrateur Zéro Obstacle, utilisable en auto-hébergement sur PC Windows (FastAPI + Ollama) avec un plugin WordPress prêt à l'emploi.

## Contenu principal
- `main.py` : serveur FastAPI avec agents (extraction PDF, admissibilité, préremplissage, général) appelant Ollama via HTTP.
- `install_zero_obstacle.bat` / `start_zero_obstacle.bat` : scripts Windows pour installer les dépendances et démarrer le serveur.
- `test_api.py` : vérifications rapides des endpoints `/health` et `/agent/orchestrate`.
- `wordpress/zero-obstacle-agent/` : plugin WordPress qui appelle l'orchestrateur (shortcode `[zero_obstacle_form]`).
- `prompts/` et `api/` : composants hérités de la première version (Docker + Celery + OpenAI/Supabase) laissés pour compatibilité éventuelle.

## Démarrage rapide (PC Windows + Ollama)
1. Installer Ollama et télécharger un modèle, par exemple :
   ```powershell
   ollama pull llama3.1
   ```
2. Copier ce dépôt sur votre PC et lancer :
   ```bat
   install_zero_obstacle.bat
   start_zero_obstacle.bat
   ```
3. L'API répond sur `http://localhost:8080`. Endpoints utiles :
   - `/health`
   - `/agent/orchestrate` (tasks : `pdf_extraction`, `admissibility`, `prefill`, `general`)
   - `/demo/admissibility`, `/demo/prefill`, `/demo/pdf`

## Tester rapidement
```bash
python test_api.py
```

## Plugin WordPress
1. Zipper le dossier `wordpress/zero-obstacle-agent` et téléverser-le dans `wp-content/plugins` via l'interface d'extensions.
2. Dans Réglages > Zero Obstacle Agent, définir l'URL FastAPI (ex : `http://VOTRE_PC:8080`).
3. Ajouter le shortcode `[zero_obstacle_form]` dans une page pour relayer les questions vers l'agent.

## Variables d'environnement
Référence dans `.env.example` :
- `OLLAMA_URL`, `OLLAMA_MODEL` pour l'usage local.
- Variables OpenAI/Supabase/Redis conservées pour l'ancienne pile Docker (si vous en avez besoin).

## Ancienne pile Docker (optionnelle)
Les fichiers `docker-compose.yml`, `api/`, et `prompts/` proviennent de la première itération (FastAPI + Celery + Redis + Supabase + OpenAI). Ils peuvent être conservés ou supprimés selon vos besoins ; la nouvelle approche n'en dépend pas.
Plateforme MVP d'orchestration d'agents auto-hébergeables pour le projet « Zero Obstacle ».

## Contenu du dépôt

- `main.py` : serveur FastAPI avec orchestrateur et agents (extraction PDF, admissibilité, préremplissage, questions générales) utilisant Ollama.
- `wordpress-plugin/zero-obstacle-agent/zero-obstacle-agent.php` : plugin WordPress minimal pour relayer les questions vers l'orchestrateur.
- `install_zero_obstacle.bat` / `start_zero_obstacle.bat` : scripts Windows pour installer les dépendances et démarrer le serveur.
- `test_api.py` : tests manuels simples pour vérifier que l'API répond localement.

## Prérequis

- Python 3.10+ sur la machine Windows qui héberge l'API.
- Ollama en cours d'exécution avec un modèle disponible (par défaut `llama3.1`).
- Accès réseau entre WordPress (PlanetHoster) et l'API (port 8080 par défaut).

## Mise en route rapide

1. **Installer l'API sur Windows**
   ```bat
   install_zero_obstacle.bat
   ```
2. **Démarrer le serveur**
   ```bat
   start_zero_obstacle.bat
   ```
3. **Vérifier la disponibilité**
   ```bash
   python test_api.py
   ```
4. **Installer le plugin WordPress**
   - Zipper le dossier `wordpress-plugin/zero-obstacle-agent` puis téléverser-le via l’interface WP.
   - Configurer l’URL de l’API dans « Réglages → Zero Obstacle Agent » (ex. `http://TON_PC:8080`).
   - Ajouter le shortcode `[zero_obstacle_form]` dans une page ou un article.

## Endpoints clés

- `GET /health` : vérifie que le serveur répond et retourne le modèle Ollama configuré.
- `POST /agent/orchestrate` : route les tâches `pdf_extraction`, `admissibility`, `prefill`, `general` vers les agents dédiés.
- Démos : `GET /demo/admissibility`, `GET /demo/prefill`.

## Notes importantes

- Les règles d’admissibilité doivent être fournies explicitement dans les requêtes (`program_rules`), aucune logique juridique n’est inventée.
- Le préremplissage ne devine pas d’informations absentes du profil utilisateur.
- Le parsing JSON des réponses LLM est volontairement simple pour rester un MVP ; prévoir du durcissement pour la production.
