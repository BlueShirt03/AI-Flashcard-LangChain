import { useEffect, useState } from 'react'
import { gerenateFlashcards } from './services/apiService'
import FlashcardView from './components/FlashcardView'
import './App.css'

  function App() {
  const [quizzes, setQuizzes] = useState([])
  const [error, setError] = useState('')
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [flashcards, setFlashcards] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [flashcardCache, setFlashcardCache] = useState({})

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

    if (flashcardCache[selectedQuiz.id]){
      setError('')
      setFlashcards(flashcardCache[selectedQuiz.id])
      console.log('Flashcards retrieved from cache.')
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

    setFlashcardCache((previousCache) => ({
      ...previousCache,
      [selectedQuiz.id]: quizResponse.flashcards
    }))

    console.log('Generated flashcards:', quizResponse.flashcards)

    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main>

      <header className='app-header'>
      <h1>AI Flashcard Generator</h1>

      <p>
        Generate Flashcards from incorrectly answered quiz questions
        using LangChain and AI.
      </p>
      </header>

      {error && <p className='error-message'>{error}</p>}

      <div className='quiz-list'>
        {quizzes.map((quiz) => (
          <div
            key={quiz.id}
            className={`quiz-card ${selectedQuiz?.id === quiz.id ? 'active' : ''}`}
          >

            <h3>{quiz.title}</h3>
            <p>Category: {quiz.tags}</p>

            <button
              type="button"
              disabled={isLoading}
              onClick={() => {
                setSelectedQuiz(quiz)
                setFlashcards(flashcardCache[quiz.id] || [])
                setError('')
              }}
            >
              Select Quiz
            </button>
          </div>
        ))}
      </div>

      {selectedQuiz && (
        <section className="selected-quiz">
          <h2>Selected Quiz: {selectedQuiz.title}</h2>
          <p>Category: {selectedQuiz.tags}</p>
          <p>Total Questions: {selectedQuiz.questions.length}</p>

          <button className="generate-button" type="button" onClick={handleGenerateFlashcards} disabled={isLoading}>

            {isLoading ? 'Generating Flashcards...' : 'Generate Flashcards'}

          </button>

          {flashcards.length > 0 && (
            <FlashcardView
              key={selectedQuiz.id}
              flashcards={flashcards}
              category={selectedQuiz.tags}
            />
            )}

        </section>
      )}

    </main>
  )
}

export default App
