from __future__ import annotations

from typing import Callable, Dict, Any, TypedDict


class WorkflowFn(Callable[..., Dict[str, Any]]):
    ...

class InputField(TypedDict, total=False):
    # core
    name: str
    label: str
    type: str            # "string" | "number" | "email" | "select"
    required: bool
    default: Any
    example: Any
    options: list[str]   # for select

    # UI hints
    placeholder: str
    help_text: str

    # numeric constraints
    min: float
    max: float
    step: float

class WorkflowDefinition(TypedDict, total=False):
    name: str
    display_name: str
    description: str
    category: str
    input_schema: list[InputField]
    version: str
    function: WorkflowFn

    # UI / business metadata (optional)
    business_summary: str
    business_steps: list[str]
    step_outline: list[str]


WORKFLOW_TEMPLATES: Dict[str, WorkflowDefinition] = {}


def register(
    *,
    name: str,
    display_name: str,
    description: str,
    category: str,
    version: str = "1.0",
    input_schema: list[InputField] | None = None,
    business_summary: str = "",
    business_steps: list[str] | None = None,
    step_outline: list[str] | None = None,
):
    def decorator(fn: WorkflowFn):
        WORKFLOW_TEMPLATES[name] = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "category": category,
            "input_schema": input_schema or [],
            "version": version,
            "business_summary": business_summary,
            "business_steps": business_steps or [],
            "step_outline": step_outline or [],
            "function": fn,
        }
        return fn
    return decorator


def get_template(name: str) -> WorkflowDefinition:
    if name not in WORKFLOW_TEMPLATES:
        raise KeyError(f"Unknown workflow template: {name}")
    return WORKFLOW_TEMPLATES[name]


def list_templates() -> list[WorkflowDefinition]:
    return list(WORKFLOW_TEMPLATES.values())


