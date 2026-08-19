from langchain_core.tools import tool


@tool
def get_career_paths() -> str:
    """Suggest a strong career path based on the user's interests."""
    options = [
        "Data Science is an excellent fit if you enjoy analysis, experimentation, and deriving insights from data.",
        "Product Management is a great path if you enjoy strategy, customer empathy, and cross-functional execution.",
        "Cybersecurity is a strong choice if you enjoy solving security problems and protecting systems.",
    ]
    return "\n".join(options)


@tool
def get_learning_resources(career: str) -> list[str]:
    """Return learning resources relevant to a given career."""
    career_lower = career.lower()
    if "data" in career_lower and "science" in career_lower:
        return [
            "Take a Python for Data Science course",
            "Study statistics and machine learning fundamentals",
            "Practice with real datasets on Kaggle",
        ]
    if "product" in career_lower and "manage" in career_lower:
        return [
            "Read product management case studies",
            "Study user research and roadmapping",
            "Practice prioritization frameworks",
        ]
    if "cyber" in career_lower or "security" in career_lower:
        return [
            "Learn networking and Linux fundamentals",
            "Study security principles and threat modeling",
            "Practice on CTF-style challenges",
        ]
    return [
        "Review foundational concepts in the selected field",
        "Look for beginner-friendly courses and projects",
    ]


@tool(return_direct=True)
def transfer_to_education_advisor() -> str:
    """Transfer the conversation to the education advisor when the user asks about courses or studying."""
    return "Transfer to education advisor"


@tool(return_direct=True)
def transfer_to_career_advisor() -> str:
    """Transfer the conversation back to the career advisor when the user asks about careers or preferences."""
    return "Transfer to career advisor"
