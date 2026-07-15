from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class OpportunitySignal(BaseModel):
    source: str
    title: str
    url: HttpUrl
    description: str = ""
    observed_at: datetime = Field(default_factory=datetime.now)
    demand_score: float = 0
    competition_score: float = 0
    printability_score: float = 0
    legal_risk_score: float = 0
    total_score: float = 0
