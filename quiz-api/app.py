import sqlite3
from flask import Flask, request
from services import AuthServices
from services import RequestServices
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ── Initialise la table Quiz au démarrage ─────────────────────
with app.app_context():
    from services.DBServices import DBServices
    db = DBServices()
    db.connection()
    db.create_tables()
    db.close()

# ── Utilisateurs ──────────────────────────────────────────────

@app.route('/users/register', methods=['POST'])
def RegisterUser():
    try:
        user = RequestServices.register_user(request.get_json())
        return {"id": user['id'], "username": user['username']}, 201
    except sqlite3.IntegrityError:
        return 'Ce pseudo est déjà pris', 409
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return str(e), 500

@app.route('/users/login', methods=['POST'])
def LoginUser():
    try:
        user = RequestServices.login_user(request.get_json())
        return {"id": user['id'], "username": user['username']}, 200
    except ValueError as e:
        return str(e), 401
    except Exception as e:
        return str(e), 500

@app.route('/users/<user_id>/history', methods=['GET'])
def GetUserHistory(user_id):
    try:
        history = RequestServices.get_user_history(user_id)
        return {"history": history}, 200
    except Exception as e:
        return str(e), 500

# ── Quiz ──────────────────────────────────────────────────────

@app.route('/quizzes', methods=['GET'])
def GetQuizzes():
    quizzes = RequestServices.get_quizzes()
    return {"quizzes": quizzes}, 200

@app.route('/quizzes', methods=['POST'])
def PostQuiz():
    if not AuthServices.verify_token(request.headers):
        return '', 401
    try:
        RequestServices.post_quiz(request.get_json())
    except sqlite3.IntegrityError:
        return 'Un quiz avec ce nom existe déjà', 409
    except Exception as e:
        return str(e), 500
    return '', 200

@app.route('/quizzes/<quiz_id>', methods=['DELETE'])
def DeleteQuiz(quiz_id):
    if not AuthServices.verify_token(request.headers):
        return '', 401
    try:
        RequestServices.delete_quiz(quiz_id)
    except Exception as e:
        return str(e), 500
    return '', 204

# ── Quiz Info ─────────────────────────────────────────────────

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    quiz_id = request.args.get('quizId')
    nb_question, scores = RequestServices.get_user_infos(quiz_id)
    return {'size': nb_question, 'scores': scores}, 200

# ── Questions ─────────────────────────────────────────────────

@app.route('/questions', methods=['GET'])
def GetQuestions():
    question_list = RequestServices.get_questions()
    return {"questions": question_list, "size": len(question_list)}, 200

@app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):
    quiz_id = request.args.get('quizId')
    try:
        if quiz_id:
            question = RequestServices.get_question_by_quiz(position, quiz_id)
        else:
            if not RequestServices.verifyPosition(position):
                return 'position not found', 404
            question = RequestServices.get_question(position)
    except Exception as e:
        return str(e), 404
    return question, 200

@app.route('/questions/<position>', methods=['DELETE'])
def DeleteQuestion(position):
    if not AuthServices.verify_token(request.headers):
        return '', 401
    if not RequestServices.verifyPosition(position):
        return 'Position not found', 404
    try:
        RequestServices.delete_question(position)
    except Exception as e:
        return str(e), 500
    return '', 204

@app.route('/questions/<position>', methods=['PUT'])
def PutQuestion(position):
    if not AuthServices.verify_token(request.headers):
        return '', 401
    if not RequestServices.verifyPosition(position):
        return 'position not found', 404
    try:
        RequestServices.put_question(position, request.get_json())
    except sqlite3.IntegrityError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500
    return '', 204

@app.route('/questions', methods=['POST'])
def PostQuestion():
    if not AuthServices.verify_token(request.headers):
        return '', 401
    try:
        RequestServices.post_question(request.get_json())
    except sqlite3.IntegrityError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500
    return '', 200

# ── Participations ────────────────────────────────────────────

@app.route('/participations', methods=['POST'])
def PostAnswers():
    try:
        good_answers, position_answers, score, player_name = RequestServices.post_answers(
            request.get_json())
    except IndexError as e:
        return {'error': str(e)}, 400
    except sqlite3.IntegrityError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500
    return {
        'answersSummaries': {
            'correctAnswerPosition': position_answers,
            'wasCorrect': good_answers
        },
        'playerName': player_name,
        'score': score
    }, 200

@app.route('/participations', methods=['DELETE'])
def DeleteParticipants():
    if not AuthServices.verify_token(request.headers):
        return '', 401
    try:
        RequestServices.delete_participants()
    except Exception as e:
        return str(e), 500
    return {}, 204

# ── Login ─────────────────────────────────────────────────────

@app.route('/login', methods=['POST'])
def Login():
    try:
        token_string = AuthServices.login(request.get_json()['password'])
        return {"token": token_string}, 200
    except ValueError as e:
        return str(e), 401

if __name__ == '__main__':
    app.run(debug=True)