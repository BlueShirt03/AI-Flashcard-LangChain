//
//  SampleData.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/5/26.
//


import Foundation

// Defines errors that can occur while loading the sample quiz data.
enum SampleDataDataError: LocalizedError{
    case fileNotFound
    case decodingFailed(Error)
    
    // Provides readable descriptions for sample data loading errors.
    var errorDescription: String? {
        switch self{
        case .fileNotFound:
            return "The mock quiz JSON file could not be found"
        case .decodingFailed(let error):
            return "Failed to decode the mock quiz JSON file: \(error.localizedDescription)"
        }
    }
}

// Provies access to the mock quiz data used by the POC.
enum SampleData {
    
    // Loads the bundled quiz JSON file and converts it into QuizData.
    static func loadQuiz() throws -> QuizData{
        
        // Locates the mock quiz JSON file included in the application bundle.
        guard let url = Bundle.main.url(forResource: "QuizzesWithUserAnswers", withExtension: "json") else {
            throw SampleDataDataError.fileNotFound
        }
        
        do {
            // Reads the JSON file and decodes it into the fronted quiz models.
            let data = try Data(contentsOf: url)
            return try JSONDecoder().decode(QuizData.self, from: data)
        } catch {
            throw SampleDataDataError.decodingFailed(error)
        }
    }
}
