//
//  FlashcardStorage.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/11/26.
//

import Foundation

struct FlashcardStorage {
    
    static func save(_ flashcards: [Flashcard]) throws {
        let data = try JSONEncoder().encode(flashcards)
        
        let url = try FileManager.default
            .url(
                for: .documentDirectory,
                in: .userDomainMask,
                appropriateFor: nil,
                create: true
            )
            .appendingPathComponent("saved_flashcards.json")
        
        try data.write(to: url)
    }
    
    static func load() throws -> Flashcard {
        let url = try FileManager.default
            .url(
                for: .documentDirectory,
                in: .userDomainMask,
                appropriateFor: nil,
                create: true
            )
            .appendingPathComponent("saved_flashcards.json")
        
        let data = try Data(contentsOf: url)
        
        return try JSONDecoder().decode(Flashcard.self, from: data)
    }
}

