from models import Question, Answer

def answer_to_dict(answer: Answer) -> dict:
    return {
        "id": answer.id,
        "text": answer.text,
        "isCorrect": answer.is_correct
    }

def dict_to_answer(data: dict) -> Answer:
    return Answer(
        id=data.get('id'),
        text=data['text'],
        is_correct=data['isCorrect']
    )

def question_to_dict(question: Question) -> dict:
    return {
        "id": question.id,
        "position": question.position,
        "title": question.title,
        "text": question.text,
        "image": question.image,
        "possibleAnswers": [answer_to_dict(answer) for answer in question.possible_answers]
    }

def dict_to_question(data: dict) -> Question:
    return Question(
        id=data.get('id'),
        position=data['position'],
        title=data['title'],
        text=data['text'],
        image=data.get('image'),
        possible_answers=[dict_to_answer(answer) for answer in data.get('possibleAnswers', [])]
    )
