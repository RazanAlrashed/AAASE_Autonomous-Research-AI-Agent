from pydantic import BaseModel, Field

class QualityScore(BaseModel):
    score: float = Field(description="Research quality score between 1 and 10")
    reasoning: str = Field( description="Explain why this score was given")