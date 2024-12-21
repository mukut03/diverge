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
    emotions: list[str]
    context: str
    needs: list[str]
    action_plan: list[str]
    reflection: str


# Response Model
class JournalResponse(BaseModel):
    emotions: list[str]
    context: str
    needs: list[str]
    action_plan: list[str]
    reflection: str


# class JournalRequest(BaseModel):
#     entry: str