//
//  ContentView.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/3/26.
//

import SwiftUI

struct ContentView: View {
    
    //Stores the generated flashcard sets that will be displayed in the library.
    @State private var flashcardSets: [FlashcardSet] = []
    
    // Control navigation to the flashcard library after generation is complete.
    @State private var showLibrary = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                
                
                Text("Quiz Complete!")
                    .font(.largeTitle)
                    .fontWeight(.bold)

                Button("Create Flashcards") {
                    Task {
                        do {
                            // Loads the completed quiz data that will be sent to the backend.
                            let quizData = try SampleData.loadQuiz()

                            // Sends the quiz data to the backend and receives
                            // generated flashcards grouped by quiz.
                            let responses = try await APIService.shared.generateFlashcard(from: quizData)
                            
                            // Processes each quiz-specific flashcard response individually.
                            for response in responses{
                                
                                // Prevents a flashcard set from being added more than once.
                                if flashcardSets.contains(where: {$0.id == response.quizId}) {
                                    continue
                                }
                                
                                // Finds the original quiz that matches the quiz ID
                                // returned with the generated flashcards.
                                guard let quiz = quizData.result.first(where: {$0.id == response.quizId}) else {
                                    continue
                                }
                                
                            
                            // Combines the backend response with the original quiz
                            // information to create set for the flaschard library.
                            let newSet = FlashcardSet(
                                id: response.quizId,
                                title: quiz.title,
                                category: quiz.tags,
                                flashcards: response.flashcards,
                                reviewedCardCount: 0
                            )
                            
                            flashcardSets.append(newSet)
                        }
                            // Opens the library after all responses have been processed
                            showLibrary = true
                            
                        } catch {
                            print("Failed to generate flashcards: \(error)")
                        }
                    }
                }
                .buttonStyle(.borderedProminent)
            }
            .padding()
            
            // Navigates to the library and provides access to the generated sets.
            .navigationDestination(isPresented: $showLibrary) {
                FlashcardLibraryView(flashcardSet: $flashcardSets)
            }
        }
    }
}
