from typing import List, Literal
from pydantic import BaseModel, Field


class AgriculturalAnalysis(BaseModel):
    querySummary: str = Field(
        description="Short summary of the farmer's problem."
    )

    detectedLanguage: str = Field(
        description="Detected farmer language, usually English or Hindi."
    )

    crop: str = Field(
        description="Detected or provided crop, or Unknown."
    )

    cropStage: str = Field(
        description="Detected/provided crop stage, or Unknown."
    )

    location: str = Field(
        description="Provided or extracted farmer location, or Not provided."
    )

    problemCategory: str = Field(
        description="Short farmer-friendly category for the problem."
    )

    possibleCauses: List[str] = Field(
        description="Up to three plausible causes, not guaranteed diagnoses."
    )

    riskLevel: Literal[
        "LOW",
        "MODERATE",
        "HIGH",
        "CRITICAL"
    ]

    reasoningSummary: str = Field(
        description=(
            "Short farmer-facing explanation for the assessment. "
            "Do not reveal internal chain-of-thought."
        )
    )

    recommendedActions: List[str] = Field(
        description="Concise practical next actions for the farmer."
    )

    avoidActions: List[str] = Field(
        description="Actions that should be avoided."
    )

    monitoringAdvice: str = Field(
        description="What the farmer should monitor next."
    )

    confidence: Literal[
        "Low",
        "Medium",
        "High"
    ]

    needsExpertHelp: bool = Field(
        description=(
            "True when physical inspection, testing, or expert evaluation "
            "is advisable."
        )
    )