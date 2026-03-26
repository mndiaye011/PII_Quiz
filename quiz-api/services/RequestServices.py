from models.__init import Question, Answer
from services.DBServices import DBServices
from datetime import datetime


def get_connection():
    dbConnection = DBServices()
    dbConnection.connection()
    return dbConnection


# ── Quiz ──────────────────────────────────────────────────────

def get_quizzes():
    dbConnection = get_connection()
    result = dbConnection.executeSelectQuery("SELECT * FROM Quiz ORDER BY id;")
    dbConnection.close()
    return result

def post_quiz(json_object):
    dbConnection = get_connection()
    name = json_object['name'].replace('"', "'")
    description = json_object.get('description', '').replace('"', "'")
    dbConnection.executeTransactionQuery(
        f'INSERT INTO Quiz (name, description) VALUES ("{name}", "{description}");'
    )
    dbConnection.close()

def delete_quiz(quiz_id):
    dbConnection = get_connection()
    # Dissocie les questions du quiz sans les supprimer
    dbConnection.executeTransactionQuery(
        f"UPDATE Question SET quiz_id = NULL WHERE quiz_id = {str(quiz_id)};"
    )
    dbConnection.executeTransactionQuery(
        f"DELETE FROM Quiz WHERE id = {str(quiz_id)};"
    )
    dbConnection.close()


# ── Questions ─────────────────────────────────────────────────

def verifyPosition(position):
    dbConnection = get_connection()
    result = dbConnection.executeSelectQuery(
        f"SELECT * FROM Question WHERE position={str(position)};")
    dbConnection.close()
    return len(result) > 0

def get_question_by_quiz(position, quiz_id):
    dbConnection = get_connection()
    result = dbConnection.executeSelectQuery(
        f"SELECT * FROM Question WHERE position={position} AND quiz_id={str(quiz_id)};")
    if len(result) != 1:
        raise Exception("Question non trouvée")
    question = result[0]
    answers = dbConnection.executeSelectQuery(
        f"SELECT text, isCorrect FROM Answer WHERE question_id={str(question['id'])};")
    for a in answers:
        a["isCorrect"] = bool(a["isCorrect"])
    question["possibleAnswers"] = answers
    dbConnection.close()
    return question

def get_questions():
    dbConnection = get_connection()
    result = dbConnection.executeSelectQuery(
        "SELECT * FROM Question ORDER BY position;")
    if len(result) <= 0:
        return []
    for obj in result:
        answers = dbConnection.executeSelectQuery(
            f"SELECT text, isCorrect FROM Answer WHERE question_id=\"{str(obj['id'])}\";")
        obj["possibleAnswers"] = answers
        for a in obj["possibleAnswers"]:
            a["isCorrect"] = bool(a["isCorrect"])
    dbConnection.close()
    return result

def get_question(position):
    dbConnection = get_connection()
    result = dbConnection.executeSelectQuery(
        f"SELECT * FROM Question WHERE position={position};")
    if len(result) != 1:
        raise Exception("No questions found")
    question = result[0]
    answers = dbConnection.executeSelectQuery(
        f"SELECT text, isCorrect FROM Answer WHERE question_id={str(question['id'])};")
    for a in answers:
        a["isCorrect"] = bool(a["isCorrect"])
    question["possibleAnswers"] = answers
    dbConnection.close()
    return question

def post_question(json_object):
    dbConnection = get_connection()
    question = Question.deserialize(json_object)
    # Récupère quiz_id si fourni
    quiz_id = json_object.get('quizId', None)
    quiz_id_sql = str(quiz_id) if quiz_id else "NULL"

    # Décale seulement les questions du même quiz
    if quiz_id:
        dbConnection.executeTransactionQuery(
            f"UPDATE Question SET position = position + 1 WHERE position >= {str(question.position)} AND quiz_id = {quiz_id_sql};"
        )
    else:
        dbConnection.executeTransactionQuery(
            f"UPDATE Question SET position = position + 1 WHERE position >= {str(question.position)};"
        )

    dbConnection.executeTransactionQuery(
        f'INSERT INTO Question (title, text, image, position, quiz_id) VALUES '
        f'("{question.title}", "{question.text}", "{question.image}", '
        f'{str(question.position)}, {quiz_id_sql});'
    )
    result = dbConnection.executeSelectQuery(
        "SELECT seq FROM sqlite_sequence WHERE name='Question';")
    if len(result) != 1:
        raise Exception("Error while inserting question")
    question.id = result[0]["seq"]
    for answer in question.answers:
        dbConnection.executeTransactionQuery(
            f'INSERT INTO Answer (text, isCorrect, question_id) VALUES '
            f'("{answer.text}", {str(answer.correct)}, {str(question.id)});'
        )
    dbConnection.close()

def delete_question(position):
    dbConnection = get_connection()
    dbConnection.executeTransactionQuery(
        f"DELETE FROM Question WHERE position={str(position)};")
    dbConnection.executeTransactionQuery(
        f"UPDATE Question SET position = position - 1 WHERE position >= {str(position)};")
    dbConnection.close()

def put_question(position, json_obj):
    question = Question.deserialize(json_obj)
    dbConnection = get_connection()
    position = int(position)
    result = dbConnection.executeSelectQuery(
        f"SELECT id FROM Question WHERE position={str(position)};")
    if len(result) != 1:
        raise Exception("No questions found")
    id = result[0]['id']
    if position != question.position:
        sign = 1 if question.position > position else -1
        while position != question.position:
            dbConnection.executeTransactionQuery(
                f"UPDATE Question SET position=position + {str(-sign)} WHERE position={str(position+sign)};")
            position += sign
    dbConnection.executeTransactionQuery(
        f'UPDATE Question SET title="{question.title}", text="{question.text}", '
        f'image="{question.image}", position={str(question.position)} WHERE id={str(id)};'
    )
    dbConnection.executeTransactionQuery(
        f"DELETE FROM Answer WHERE question_id={str(id)};")
    for answer in question.answers:
        dbConnection.executeTransactionQuery(
            f'INSERT INTO Answer (question_id, text, isCorrect) VALUES '
            f'({str(id)}, "{answer.text}", {str(answer.correct)});'
        )
    dbConnection.close()


# ── Quiz Info ─────────────────────────────────────────────────

def get_user_infos(quiz_id=None):
    dbConnection = get_connection()
    if quiz_id:
        result = dbConnection.executeSelectQuery(
            f"SELECT COUNT(*) as nbQuestion FROM Question WHERE quiz_id={str(quiz_id)};")
    else:
        result = dbConnection.executeSelectQuery(
            "SELECT COUNT(*) as nbQuestion FROM Question;")
    nbQuestion = result[0]['nbQuestion'] if result else 0
    scores = dbConnection.executeSelectQuery(
        "SELECT * FROM Participant ORDER BY score DESC;")
    dbConnection.close()
    return nbQuestion, scores


# ── Participations ────────────────────────────────────────────

def post_answers(json_object):
    playerName = json_object['playerName']
    answers = json_object['answers']
    quiz_id = json_object.get('quizId', None)

    dbConnection = get_connection()
    if quiz_id:
        result = dbConnection.executeSelectQuery(
            f"SELECT id FROM Question WHERE quiz_id={str(quiz_id)} ORDER BY position;")
    else:
        result = dbConnection.executeSelectQuery(
            "SELECT id FROM Question ORDER BY position;")

    if len(result) <= 0:
        raise Exception("No questions found")
    if len(result) != len(answers):
        raise IndexError("Number of answers is not the same as number of questions")

    position_answers = []
    good_answers = []
    for i, obj in enumerate(result):
        resultAnswer = dbConnection.executeSelectQuery(
            f"SELECT * FROM Answer WHERE question_id={str(obj['id'])};")
        if len(resultAnswer) <= 0:
            raise Exception("No answers found")
        for j, answer in enumerate(resultAnswer):
            if answer['isCorrect'] == 1:
                position_answers.append(j + 1)
                good_answers.append(j + 1 == answers[i])
                break

    score = len(list(filter(lambda x: x, good_answers)))
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dbConnection.executeTransactionQuery(
        f'INSERT INTO Participant (playerName, score, date) VALUES '
        f'("{playerName}", {str(score)}, "{dt_string}");'
    )
    dbConnection.close()
    return good_answers, position_answers, score, playerName

def delete_participants():
    dbConnection = get_connection()
    dbConnection.executeTransactionQuery("DELETE FROM Participant;")
    dbConnection.close()