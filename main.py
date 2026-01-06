# main.py
#
# Serveur d'agents Zero Obstacle
# - API FastAPI
# - Intégration Ollama
# - Agents : orchestrateur, PDF, admissibilité, préremplissage
#
# Dépendances :
#   pip install fastapi uvicorn[standard] httpx pydantic pypdf python-dotenv

import base64
import io
import os
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader

# Charger .env si présent (OLLAMA_URL, OLLAMA_MODEL)
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

app = FastAPI(title="Zero Obstacle Agents", version="0.1.0")

# CORS (MVP : tout autoriser, à restreindre plus tard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
#       Modèles Pydantic
# =========================


class ProgramRule(BaseModel):
    id: str
    description: str
    field: str
    operator: str
    value: Any
    required: bool = True


class OrchestrationRequest(BaseModel):
    task: str  # "pdf_extraction", "admissibility", "prefill", "general"
    text: Optional[str] = None
    pdf_base64: Optional[str] = None
    user_profile: Optional[Dict[str, Any]] = None
    program_rules: Optional[List[ProgramRule]] = None


class OrchestrationResponse(BaseModel):
    task: str
    result: Dict[str, Any]


# =========================
#       Utilitaires LLM
# =========================


async def call_ollama(prompt: str) -> str:
    """
    Appelle le modèle local via Ollama.
    Nécessite :
      - Ollama en cours d'exécution
      - modèle tiré (ollama pull ...)

    L'API utilisée est la génération simple (non streaming).
    """

    ollama_api_url = f"{OLLAMA_URL}/api/generate"
    generation_payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=120) as http_client:
        ollama_response = await http_client.post(ollama_api_url, json=generation_payload)
        ollama_response.raise_for_status()
        response_json = ollama_response.json()
    return response_json.get("response", "").strip()


# =========================
#          Agents
# =========================


def agent_extract_pdf_text(pdf_bytes: bytes) -> str:
    """
    Extraction brute du texte d'un PDF avec pypdf.
    Ne fait aucune interprétation juridique : seulement du texte.
    """

    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
    extracted_text_chunks: List[str] = []
    for pdf_page in pdf_reader.pages:
        try:
            extracted_text_chunks.append(pdf_page.extract_text() or "")
        except Exception:
            continue
    return "\n\n".join(extracted_text_chunks)


async def agent_structure_pdf_form_fields(raw_text: str) -> Dict[str, Any]:
    """
    Demande au LLM de transformer un texte brut de formulaire
    en liste structurée de champs (MVP).
    """

    structure_prompt = f"""
Tu es un assistant chargé de structurer des formulaires administratifs.

Texte brut du formulaire (extraits PDF) :
\"\"\"{raw_text[:6000]}\"\"\"  # limité pour éviter les prompts trop longs

Tâche :
1. Identifie les champs du formulaire (ex: nom, prénom, NAS, adresse, etc.).
2. Pour chaque champ, retourne un objet JSON :
   - "name" : nom machine (en_snake_case)
   - "label" : libellé affiché
   - "type" : "string", "date", "number", "boolean" ou "select"
   - "required" : true/false
   - "help_text" : courte explication

3. Retourne UNIQUEMENT un objet JSON valide :
{{
  "fields": [ ... ]
}}
"""
    llm_response = await call_ollama(structure_prompt)
    import json

    try:
        parsed_structured_data = json.loads(llm_response)
    except Exception:
        parsed_structured_data = {
            "fields": [],
            "raw_response": llm_response,
        }
    return parsed_structured_data


async def agent_admissibility(user_profile: Dict[str, Any], program_rules: List[ProgramRule]) -> Dict[str, Any]:
    """
    Applique STRICTEMENT les règles fournies.
    Pas de création de nouvelles règles.
    Les règles sont purement techniques, pas juridiques.
    """

    import json

    serialized_rules_json = json.dumps([rule.dict() for rule in program_rules], ensure_ascii=False)
    serialized_profile_json = json.dumps(user_profile, ensure_ascii=False)

    eligibility_check_prompt = f"""
Tu es un système de règles techniques. 
Tu DOIS appliquer UNIQUEMENT les règles fournies ci-dessous. 
Tu NE DOIS PAS inventer de nouvelles conditions.

Règles (JSON) :
{serialized_rules_json}

Profil utilisateur (JSON) :
{serialized_profile_json}

Tâche :
1. Pour chaque règle, indique si elle est satisfaite ou non.
2. Détermine :
   - "eligible": true/false (true uniquement si TOUTES les règles required=true sont satisfaites)
   - "failed_rules": liste des id des règles non satisfaites
   - "details": explication courte (sans interprétation juridique, juste technique)

Retourne un JSON strictement valide de la forme :
{{
  "eligible": true/false,
  "failed_rules": ["..."],
  "details": "..."
}}
"""

    llm_response = await call_ollama(eligibility_check_prompt)
    try:
        parsed_eligibility_result = json.loads(llm_response)
    except Exception:
        parsed_eligibility_result = {
            "eligible": False,
            "failed_rules": [],
            "details": f"Réponse non JSON du modèle : {llm_response}",
        }
    return parsed_eligibility_result


async def agent_prefill_form(user_profile: Dict[str, Any], fields_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propose un préremplissage strictement basé sur les données du profil.
    Ne devine pas des informations absentes.
    """

    import json

    serialized_fields_json = json.dumps(fields_schema, ensure_ascii=False)
    serialized_profile_json = json.dumps(user_profile, ensure_ascii=False)

    prefill_prompt = f"""
Tu dois préremplir un formulaire à partir d'un profil utilisateur.

Schéma des champs :
{serialized_fields_json}

Profil utilisateur :
{serialized_profile_json}

Règles :
- Tu n'inventes aucune information.
- Si une donnée n'est pas présente dans le profil, tu mets la valeur null.
- Tu respectes les types : string, number, boolean, date.

Retour attendu (JSON) :
{{
  "values": {{
    "<field_name>": <valeur_ou_null>
  }}
}}
"""
    llm_response = await call_ollama(prefill_prompt)
    try:
        parsed_prefilled_values = json.loads(llm_response)
    except Exception:
        parsed_prefilled_values = {
            "values": {},
            "details": f"Réponse non JSON du modèle : {llm_response}",
        }
    return parsed_prefilled_values


# =========================
#         Endpoints
# =========================


@app.get("/health")
async def health():
    return {"status": "ok", "model": OLLAMA_MODEL}


@app.post("/agent/orchestrate", response_model=OrchestrationResponse)
async def orchestrate(request: OrchestrationRequest):
    """
    Endpoint général appelé par WordPress.
    Selon task, route vers l'agent approprié.
    """

    if request.task == "pdf_extraction":
        if not request.pdf_base64:
            raise HTTPException(status_code=400, detail="pdf_base64 manquant")
        try:
            decoded_pdf_bytes = base64.b64decode(request.pdf_base64)
        except Exception:
            raise HTTPException(status_code=400, detail="pdf_base64 invalide")

        extracted_raw_text = agent_extract_pdf_text(decoded_pdf_bytes)
        structured_fields = await agent_structure_pdf_form_fields(extracted_raw_text)
        return OrchestrationResponse(
            task=request.task,
            result={
                "raw_text_preview": extracted_raw_text[:2000],
                "structured": structured_fields,
            },
        )

    if request.task == "admissibility":
        if not request.user_profile or not request.program_rules:
            raise HTTPException(status_code=400, detail="user_profile et program_rules sont requis")
        eligibility_result = await agent_admissibility(request.user_profile, request.program_rules)
        return OrchestrationResponse(task=request.task, result=eligibility_result)

    if request.task == "prefill":
        if not request.user_profile or not request.text:
            raise HTTPException(status_code=400, detail="user_profile et text (schéma) sont requis")
        import json

        try:
            parsed_fields_schema = json.loads(request.text)
        except Exception:
            raise HTTPException(status_code=400, detail="text doit contenir un JSON de schéma de champs")
        prefill_result = await agent_prefill_form(request.user_profile, parsed_fields_schema)
        return OrchestrationResponse(task=request.task, result=prefill_result)

    if request.task == "general":
        if not request.text:
            raise HTTPException(status_code=400, detail="text manquant pour task=general")
        general_question_prompt = f"""
Tu es un assistant Zero Obstacle.
Réponds de façon structurée, en expliquant clairement les étapes administratives,
sans inventer de lois ni de droits. Si une information n'est pas disponible, dis-le.
Question :
{request.text}
"""
        general_answer = await call_ollama(general_question_prompt)
        return OrchestrationResponse(task=request.task, result={"answer": general_answer})

    raise HTTPException(status_code=400, detail=f"Task inconnue: {request.task}")


# =========================
#           Démos
# =========================


@app.get("/demo/admissibility")
async def demo_admissibility():
    """
    Démo purement technique (non juridique).
    """

    demo_user_profile = {
        "province": "QC",
        "age": 35,
        "income": 25000,
        "single_parent": True,
    }
    demo_program_rules = [
        ProgramRule(
            id="age_min_18",
            description="Âge minimum 18 ans",
            field="age",
            operator=">=",
            value=18,
            required=True,
        ),
        ProgramRule(
            id="max_income_30000",
            description="Revenu maximal 30 000",
            field="income",
            operator="<=",
            value=30000,
            required=True,
        ),
    ]
    eligibility_check_result = await agent_admissibility(demo_user_profile, demo_program_rules)
    return {"profile": demo_user_profile, "rules": [rule.dict() for rule in demo_program_rules], "result": eligibility_check_result}


@app.get("/demo/prefill")
async def demo_prefill():
    """
    Démo de préremplissage sur un schéma fictif.
    """

    demo_user_profile = {
        "first_name": "Alex",
        "last_name": "Tremblay",
        "province": "QC",
        "email": "alex.tremblay@example.com",
    }
    demo_fields_schema = {
        "fields": [
            {"name": "first_name", "label": "Prénom", "type": "string", "required": True},
            {"name": "last_name", "label": "Nom", "type": "string", "required": True},
            {"name": "email", "label": "Courriel", "type": "string", "required": True},
            {"name": "phone", "label": "Téléphone", "type": "string", "required": False},
        ]
    }
    prefill_result = await agent_prefill_form(demo_user_profile, demo_fields_schema)
    return {"profile": demo_user_profile, "fields_schema": demo_fields_schema, "result": prefill_result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
