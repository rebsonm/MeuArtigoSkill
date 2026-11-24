"""AI execution identity: record observable facts, never infer a hidden model or host."""
from datetime import date, datetime
FIELDS = ('Model_provider', 'Execution_environment', 'Client_surface', 'Model_configuration', 'Execution_timestamp', 'Model_identification_source', 'Environment_identification_source', 'Meu_Artigo_version')
UNKNOWN = {"", "UNKNOWN", "NOT_EXPOSED", "NOT_RECORDED", "UNVERIFIED", "NOT_APPLICABLE", "UNINFORMED VERSION"}
GENERIC_MODELS = {"CHATGPT", "OPENAI", "CLAUDE", "ANTHROPIC", "GEMINI", "GOOGLE", "CODEX", "AI", "IA", "WORK"}
ENVIRONMENTS = {"CHAT", "WORK", "CODEX", "API", "OTHER", "NOT_EXPOSED"}
SURFACES = {"WEB", "DESKTOP_APP", "MOBILE_APP", "CLI", "IDE", "API", "OTHER", "NOT_EXPOSED"}
SOURCES = {"HOST_METADATA", "USER_REPORTED", "MODEL_SELF_REPORTED", "NOT_EXPOSED", "NOT_RECORDED"}
def clean(value):
    return " ".join(str(value or "").split())
def known(value):
    return clean(value).upper() not in UNKNOWN
def model_known(value):
    return known(value) and clean(value).upper() not in GENERIC_MODELS

def identity_issues(row):
    """Return missing/invalid metadata; old rows remain intact."""
    problems=[]
    for field in ("Platform_or_tool", "Model_or_version", "Date", *FIELDS):
        if not clean(row.get(field)):
            problems.append(field + " missing (record observed value or explicit NOT_EXPOSED)")
    day=clean(row.get("Date")); ts=clean(row.get("Execution_timestamp"))
    if known(day):
        try: date.fromisoformat(day)
        except ValueError: problems.append("Date must be the actual execution date YYYY-MM-DD")
    if known(ts):
        try:
            dt=datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if dt.tzinfo is None or dt.utcoffset() is None: raise ValueError()
            if known(day) and dt.date().isoformat()!=day: problems.append("Date and execution timestamp disagree in recorded timezone")
        except ValueError: problems.append("Execution_timestamp must be ISO 8601 with timezone offset")
    for field,allowed in (("Execution_environment",ENVIRONMENTS),("Client_surface",SURFACES),("Model_identification_source",SOURCES),("Environment_identification_source",SOURCES)):
        val=clean(row.get(field)).upper()
        if val and val not in allowed: problems.append(field+" has unsupported value")
    model=clean(row.get("Model_or_version")); source=clean(row.get("Model_identification_source")).upper()
    if model.upper() in GENERIC_MODELS: problems.append("Platform name alone is not a model/version")
    if model_known(model) and source in {"NOT_EXPOSED","NOT_RECORDED"}: problems.append("Model identity asserted without an identified source")
    return problems

def identity_record(row):
    out={"model":clean(row.get("Model_or_version")) if model_known(row.get("Model_or_version")) else "NOT_RECORDED", "date":clean(row.get("Date")) or "NOT_RECORDED"}
    out.update({f:clean(row.get(f)) or "NOT_RECORDED" for f in FIELDS})
    return out

def identity_label(record):
    return "; ".join(["model="+record["model"],"provider="+record["Model_provider"],"date="+record["date"],"timestamp="+record["Execution_timestamp"],"environment="+record["Execution_environment"],"client="+record["Client_surface"],"configuration="+record["Model_configuration"],"Meu Artigo="+record["Meu_Artigo_version"],"model source="+record["Model_identification_source"],"environment source="+record["Environment_identification_source"]])
