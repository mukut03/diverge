from pydantic import BaseModel, Field


class JournalRequest(BaseModel):
    """
    Input model for journal entry analysis.
    """
    entry: str = Field(..., title="Journal Entry", min_length=1)


class JournalAnalysis(BaseModel):
    """
    Output model for journal entry analysis.
    """
    analysis: str
    emotions: list[str] = Field(default_factory=list, title="Detected Emotions")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
