import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [quizzes, setQuizzes] = useState([])
  const [error, setError] = useState([])
  const [selectedQuiz, setSelectedQuiz] = useState(null)

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

          <button type="button">
            Generate Flashcards
          </button>
        </section>
      )}

    </main>
  )
}

export default App
