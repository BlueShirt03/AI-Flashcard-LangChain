//
//  APIService.swift
//  AsoboFlashcardPOC
//
//  Created by Cristian Castillo on 8/3/26.
//

import Foundation

// Represents the response returned by the backend health endpoint.
struct HealthResponse: Codable{
    let status: String
}

// Defines errors that can occur while communicating with the backend API
enum APIError: Error{
    case invalidURL
    case invalidResponse
    case badStatusCode(Int)
    
}

// Handles communication between the iOS application and the FastAPI backend.
final class APIService {
    
    // Provides a single shared instance of the API service throughout the application.
    static let shared = APIService()
    
    // Prevents additional instances of APIService from being created.
    private init(){}
    
    // Base address of the locally running FastAPI backend.
    private let baseURL = "http://127.0.0.1:8000"
    
    // Checks whether the backend API is running and responding successfully.
    func checkHealth() async throws -> HealthResponse{
        guard let url = URL(string: "\(baseURL)/health") else {
            throw APIError.invalidURL
            }
        let (data, respone) = try await URLSession.shared.data(from: url)
        
        guard let httpResponse = respone as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        
        guard httpResponse.statusCode == 200 else {
            throw APIError.badStatusCode(httpResponse.statusCode)
        }
        
        // Converts the JSON response from the backend into a HealthResponse object.
        return try JSONDecoder().decode(HealthResponse.self, from: data)
    }
    
    
    // Sends quiz data to the backend and returns the generated flashcards
    // grouped by their associated quiz.
    func generateFlashcard(from quizData: QuizData) async throws -> [FlashcardResponse]{
        guard let url = URL(string: "\(baseURL)/flashcards/generate") else{
            throw APIError.invalidURL
        }
        
        // Configures the request to send quiz data to the flashcard generation endpoint
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Converts QuizData into JSON for the request body.
        request.httpBody = try JSONEncoder().encode(quizData)
        
        // Sends the request asynchronously and waits for the backend response.
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        
        // Accepts successful HTTP status codes and reports backend errors otherwise.
        guard (200...299).contains(httpResponse.statusCode) else {
            let errorMessage = String(data:data, encoding: .utf8) ?? "Unknown server error"
            print("Backend error: \(errorMessage)")
            throw APIError.badStatusCode(httpResponse.statusCode)
        }
        
        // Converts the backend JSON response into flashcard response objects.
        return try JSONDecoder().decode([FlashcardResponse].self, from: data)
    }
    
}

