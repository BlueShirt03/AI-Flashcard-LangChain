//
//  FlashcardView.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/3/26.
//

import SwiftUI


// Displays flashcard set and manages navigation,
// review progress of the generated flashcards.
struct FlashcardView: View {
    
    let flashcards: [Flashcard]
    let category: String
    
    // Updates the review count stored in the parent FlashcardSet.
    @Binding var reviewedCardCount: Int
    
    // Tracks which individual flashcards have been reviewed.
    @State private var reviewedCards: [Bool]
    
    // Tracks the flashcard currently being displayed.
    @State private var currentIndex = 0
        
    // Initializes the reviewed state using any existing review progress.
    init(
           flashcards: [Flashcard],
           category: String,
           reviewedCardCount: Binding<Int>
       ) {
           self.flashcards = flashcards
           self.category = category
           self._reviewedCardCount = reviewedCardCount
           
           // Prevents the existing review count from exceeding
           // the number of flashcards in the set.
           let existingCount = min(
               reviewedCardCount.wrappedValue,
               flashcards.count
           )

           // Creates on Boolean value for each flashcard and restores
           // previously reviewed cards based on the existing count.
           _reviewedCards = State(
               initialValue: (0..<flashcards.count).map {
                   $0 < existingCount
               }
           )
       }

    var body: some View {
        ScrollView(){
            VStack(spacing: 20){
                
                Text("\(category) Flashcards")
                    .font(.largeTitle)
                    .bold()
                
                // Display an empty state if no flashcards were generated.
                if flashcards.isEmpty{
                    ContentUnavailableView(
                        "No Flashcards",
                        systemImage: "rectangle.stack.badge.minus",
                        description: Text("No flashcards were generated.")
                    )
                } else {
                    
                    // Shows the user's current position within the flashcard set.
                    Text(" \(currentIndex + 1) of \(flashcards.count)")
                        .foregroundStyle(.secondary)
                    
                    // Display the current flashcard and provides a binding
                    // to its individual reviewed state.
                    FlashcardItemView(
                        flashcard: flashcards[currentIndex],
                        index: currentIndex,
                        hasBeenReviewed: $reviewedCards[currentIndex]
                    )
                    
                }
                
                // Allows the user to move back and forth through the set.
                HStack {
                    
                    // Left arrow button
                    Button(){
                        if currentIndex > 0 {
                            currentIndex -= 1
                        }
                    } label: {
                        Image(systemName: "chevron.left")
                    }
                    .padding(20)
                    .background(Color(.systemGray6))
                    .clipShape(RoundedRectangle(cornerRadius: 30))
                    .disabled(currentIndex == 0)
                    
                    // Right arrow button
                    Button(){
                        if currentIndex < flashcards.count - 1{
                            currentIndex += 1
                        }
                    } label: {
                        Image(systemName: "chevron.right")
                    }
                    .padding(20)
                    .background(Color(.systemGray6))
                    .clipShape(RoundedRectangle(cornerRadius: 30))
                    .disabled(currentIndex == flashcards.count - 1)
                    
                }
                
               

            }
            
        }
        
        // Recalculates the total reviewed-card count whenever
        // an individual card's reviewed state changes.
        .onChange(of: reviewedCards) { _, newValue in
            reviewedCardCount = newValue.filter { $0 }.count
        }
       // .navigationTitle("Flashcards")
       // .navigationBarTitleDisplayMode(.inline)

        
    }
    
}

