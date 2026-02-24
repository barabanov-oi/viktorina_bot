def build_question_prompt(topic_id: int, difficulty: str, language: str) -> str:
    return (
        "Сгенерируй 1 вопрос викторины в JSON без markdown: "
        '{"question":str,"answers":[str,str,str,str],"correct_index":int,"explanation":str,"tags":[str]} '
        f"Тема id={topic_id}, сложность={difficulty}, язык={language}."
    )
