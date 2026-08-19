from langgraph.prebuilt import create_react_agent

from agentTools import (
    get_career_paths,
    get_learning_resources,
    transfer_to_career_advisor,
    transfer_to_education_advisor,
)
from llm import get_model

career_prompt = """
You are a career advisor.
Help the user choose or refine a career path in a concise, client-friendly way.
Keep your response short, avoid long paragraphs, and do not use excessive markdown formatting.
If the user asks about courses, programs, certifications, or studying, explain briefly why you are transferring to the education advisor before doing so.
Always explain your reasoning clearly before transferring.
"""

education_prompt = """
You are an education advisor.
Help the user find courses, learning paths, and study resources in a clear and concise way.
Keep your response short, avoid long paragraphs, and do not use excessive markdown formatting.
If the user changes career preference or asks for career guidance, explain briefly why you are transferring back to the career advisor before doing so.
Always explain your reasoning clearly before transferring.
"""

model = get_model()

career_advisor = create_react_agent(
    model,
    [get_career_paths, get_learning_resources, transfer_to_education_advisor],
    prompt=career_prompt,
)

education_advisor = create_react_agent(
    model,
    [get_learning_resources, transfer_to_career_advisor],
    prompt=education_prompt,
)

__all__ = ["career_advisor", "education_advisor"]
