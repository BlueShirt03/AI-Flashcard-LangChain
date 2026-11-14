//
//  FlashcardItemView.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/11/26.
//

import SwiftUI

// Displays a single flashcard and handles its flips and review behavior.
struct FlashcardItemView: View {
    
    // Flashcard content displayed by this view
    let flashcard: Flashcard
    
    // Position of the flashcard within the current set.
    let index: Int
    
    // Tracks whether this card has been reviewed and updates
    // the review state stored in the parent view.
    @Binding var hasBeenReviewed: Bool
    
    // Controls whether the front or back of the card is displayed.
    @State private var showBack = false
    
    // Tracks the card's rotation angle for the flip animation.
    @State private var rotation = 0.0
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15){
            
            // Displays the back and the explanation after the card is flipped.
            if showBack{
                VStack(alignment: .leading, spacing: 15){
                    
                    // Display the back of flashcard
                    Text(flashcard.back)
                    
                    Divider()
                    
                    // Display the explanation of flachcard
                    Text(flashcard.explanation)
                        .foregroundStyle(.black)
                }
                // Corrects the back content so it remains readable
                // while the entire card is rotated.
                .rotation3DEffect(.degrees(rotation), axis: (x:1 , y: 0, z: 0))
                
            } else{
                
                // Display the front side of the flashcard.
                Text(flashcard.front)
                    .foregroundStyle(.black)
                    
            }
        
            
        }
        .frame(maxWidth: 325, minHeight: 250, maxHeight: .infinity ,alignment: .center)
        .padding(10)
        .background(Color(.systemGray6))
        .clipShape(RoundedRectangle(cornerRadius: 16))
        
        // Marks the card as reviewed and flips it when tapped.
        .onTapGesture {
            
            // A card is only marked viewed the first time it is flipped.
            if !hasBeenReviewed {
                hasBeenReviewed = true
            }
            
            withAnimation(.easeInOut(duration: 0.5)){
                showBack.toggle()
                rotation += 180
            }
        }
        
        // Rotates the entire card to create the flip animation.
        .rotation3DEffect(
            .degrees(rotation),
            axis: (x: 1, y: 0, z: 0)
        )
    }
}


