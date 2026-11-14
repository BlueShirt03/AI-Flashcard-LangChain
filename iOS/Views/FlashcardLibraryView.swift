//
//  FlashcardLibraryView.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 9/1/26.
//



import SwiftUI


// Display the user's generated flashcard sets and allows them
// to filter the library by quiz category
struct FlashcardLibraryView: View {
    
    // Tracks which category si currently selected by the user.
    @State private var selectedCategory = "All"
    
    // Creates the category is currently selected by the user.
    var categories: [String] {
        let uniqueCategories = Set(flashcardSet.map{ $0.category})
        return ["All"] + uniqueCategories.sorted()
    
    }
    
    
    // Recevies the flashcard sets from the parent view and allows
    // changes to review progress to be reflected back in the parent.
    @Binding var flashcardSet: [FlashcardSet]
    
    // Finds the original array indices of the flashcard sets that
    // match the selected category.
    var filteredIndices: [Int] {
        flashcardSet.indices.filter { index in
            selectedCategory == "All"
            || flashcardSet[index].category == selectedCategory
        }
    }
    
    var body: some View {
        ScrollView{
            
            VStack(spacing: 20){
                
                // Display a filter button for each available category.
                HStack(spacing: 12){
                    ForEach(categories, id: \.self) { category in
                        Button(category){
                            selectedCategory = category
                        }
                        .foregroundStyle(.black)
                        .padding(.horizontal, 18)
                        .padding(.vertical, 8)
                        .background(selectedCategory == category ? Color.gray.opacity(0.35): Color.gray.opacity(0.15))
                        .clipShape(Capsule())
                        
                    }
                }
                
                // Display the flashcard sets that match the selected category.
                ForEach(filteredIndices, id: \.self) { index in

                    let set = flashcardSet[index]

                    NavigationLink {
                        FlashcardView(
                            flashcards: set.flashcards,
                            category: set.category,
                            reviewedCardCount: $flashcardSet[index].reviewedCardCount
                        )
                    } label: {
                        FlashcardSetRow(
                            flashcardSet: set
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding()
        }
    }
}
