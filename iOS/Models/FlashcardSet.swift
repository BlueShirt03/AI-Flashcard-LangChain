//
//  FlashcardSet.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/31/26.
//


// Represents a collection of generated flashcard associated with a quiz.
struct FlashcardSet: Identifiable{
    
    // Uses the original quiz ID to uniquely identify the flashcard set.
    let id: Int
    
    let title: String
    let category: String
    let flashcards: [Flashcard]
    
    // Tracks how many flashcards the user has reviewed in this set.
    var reviewedCardCount: Int
    
    // Calculates the current review status based on the user's progress.
    var statusText: String {
        if reviewedCardCount == 0{
            return "Not Started"
        } else if reviewedCardCount >= flashcards.count {
            return "Mastered"
        } else {
            return "\(reviewedCardCount) of \(flashcards.count) Reviewed"
        }
    }
    
}






