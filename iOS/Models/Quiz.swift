//
//  Quiz.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/3/26.
//


import Foundation

// Represents a possible answer for a quiz question.
struct Answer: Codable{
    let id: Int
    let text: String
    let isRightAnswer: Bool
    let questionId: Int
}

// Represents a quiz question, its possible answers,
// and the answers selected by the user.
struct Question: Codable{
    let id: Int
    let quizId: Int
    let text: String
    let answers: [Answer]
    let userAnswerIdList: [Int]
}

// Represents a complete quiz and all of its questions.
struct Quiz: Codable{
    let id: Int
    let title: String
    let tags: String
    let questions: [Question]
}

// Represents the top-level structure of the quiz data
// that is loaded by the iOS application and sent to the backend
struct QuizData: Codable{
    let result: [Quiz]
}


// Represents an incorrectly answered question and the
// informatoin needed to generate flashcards from it.
struct IncorrectQuestion: Codable{
    let questionId: Int
    let question: String
    let userAnsewrs: String
    let correctAnswers: String
}
