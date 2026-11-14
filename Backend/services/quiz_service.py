from Backend.models.quiz_models import QuizData, IncorrectQuestion, QuizIncorrectQuestions

def get_incorrect_questions(quiz_data: QuizData) -> list[QuizIncorrectQuestions]:

    # Collect the incorrect questions for each quiz.
    quiz_resutls = []
    processed_quiz_ids = set()

    for quiz in quiz_data.result:

        # Prevent duplicate quiz entries from being processed more than once.
        if quiz.id in processed_quiz_ids:
            continue

        incorrect_questions = []

        for question in quiz.questions:

            # Ignore questions that were never answered.
            if not question.userAnswerIdList:
                continue

            # Answers marked as correct in the quiz data.
            correct_answers = [
                answer
                for answer in question.answers
                if answer.isRightAnswer 
            ]

            # Answers the student actually selected for this question.
            user_answers = [
                answer
                for answer in question.answers
                if answer.id in question.userAnswerIdList
            ]

            correct_answer_ids = {answer.id for answer in correct_answers}
            user_answer_ids = {answer.id for answer in user_answers}

            # A mismatch means the question was answered incorrectly.
            if user_answer_ids != correct_answer_ids:
                incorrect_question = IncorrectQuestion(
                    questionId = question.id, 
                    question = question.text,
                    userAnswers=", ".join(answer.text for answer in user_answers),
                    correctAnswer=", ".join(answer.text for answer in correct_answers)
                )
                incorrect_questions.append(incorrect_question)



        if incorrect_questions:
            quiz_resutl = QuizIncorrectQuestions(
                quizId= quiz.id,
                incorrectQuestions= incorrect_questions
            )   

            quiz_resutls.append(quiz_resutl)
            processed_quiz_ids.add(quiz.id)

    return quiz_resutls