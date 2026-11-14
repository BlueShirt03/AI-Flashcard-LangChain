//
//  FlashcardSetRow.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/31/26.
//


import SwiftUI

// Display a summary row for a flashcard set in the flashcard library.
struct FlashcardSetRow: View {
    
    let flashcardSet: FlashcardSet
    
    var body: some View {
        HStack(spacing: 25) {
            
            // Displays a visual placeholder representing a flashcard set.
            ZStack{
                RoundedRectangle(cornerRadius: 10)
                    .fill(.gray.opacity(0.25))
                    .frame(width:174, height: 130)
                
                Image(systemName: "rectangle.stack.fill")
                    .font(.system(size: 34))
            }
            
            // Display the quiz title, number of flashcards, and review progress.
            VStack(alignment: .leading, spacing: 22) {
                Text("\(flashcardSet.title) flashcards")
                    .lineLimit(1)
                    .truncationMode(.tail)
                
                Text("\(flashcardSet.flashcards.count) Flashcards")
                
                Text(flashcardSet.statusText)
            }
            // Gives the text content priority when SwiftUI distributes available space.
            .layoutPriority(1)
            
        }
        
    }
}
