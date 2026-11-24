import { useEffect, useState } from 'react'
import { gerenateFlashcards } from './services/apiService'
import './App.css'

  function App() {
  const [quizzes, setQuizzes] = useState([])
  const [error, setError] = useState([])
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [flashcards, setFlashcards] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() =>{
    async function loadQuizzes() {
      try{
        const response = await fetch('/mock_quiz_data.json')

        if (!response.ok){
          throw new Error('Failed to load quiz data.')
        }
        
        const data = await response.json()
        setQuizzes(data.result)
      } catch (err) {
        setError(err.message)
      }
    }
    loadQuizzes()
  }, [])

  async function handleGenerateFlashcards() {
    if (!selectedQuiz || isLoading){
      return
    }
  

  setIsLoading(true)
  setError('')
  setFlashcards([])

  try {
    const responses = await gerenateFlashcards(selectedQuiz)

    const quizResponse = responses.find(
      (response) => response.quizId === selectedQuiz.id
    )

    if(!quizResponse){
      throw new Error('No flashcards returned for the selected quiz.')
    }

    setFlashcards(quizResponse.flashcards)

    console.log('Generated flashcards:', quizResponse.flashcards)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main>

      <h1>AI Flashcard Generator</h1>

      <p>
        Generate Flashcards from incorrectly answered quiz questions
        using LangChain and AI.
      </p>

      {error && <p>{error}</p>}

      {quizzes.map((quiz) => (
        <div key={quiz.id}>
          <h3>{quiz.title}</h3>
          <p>Category: {quiz.tags}</p>

          <button type="button" onClick={() => setSelectedQuiz(quiz)}>
            Select Quiz
          </button>

        </div>
      ))}

      {selectedQuiz && (
        <section>
          <h2>Selected Quiz: {selectedQuiz.title}</h2>
          <p>Category: {selectedQuiz.tags}</p>
          <p>Total Questions: {selectedQuiz.questions.length}</p>

          <button type="button" onClick={handleGenerateFlashcards} disabled={isLoading}>
            {isLoading ? 'Generating Flashcards...' : 'Generate Flashcards'}
            {flashcards.length > 0 && (
              <p>Successfully generated {flashcards.length} flashcards.</p>
            )}
          </button>
        </section>
      )}

    </main>
  )
}

export default App
