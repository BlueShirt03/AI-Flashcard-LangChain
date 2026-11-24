import { useState } from "react"

function FlashcardView({flashcards, category}){
    const [currentIndex, setCurrentIndex] = useState(0)
    const [isFlipped, setIsFlipped] = useState(false)

    if (flashcards.length === 0) {
        return null
    }

    const currentCard = flashcards[currentIndex]

    function handleNext() {
        if (currentIndex < flashcards.length - 1){
            setCurrentIndex(currentIndex + 1)
            setIsFlipped(false)
        }
    }

    function handlePrevious(){
        if (currentIndex > 0){
            setCurrentIndex(currentIndex - 1)
            setIsFlipped(false)
        }
    }

    return(
        <section className="flashcard-container">
            <h2>{category} Flashcards</h2>

            <p>
                Card {currentIndex + 1} of {flashcards.length}
            </p>
            <progress
                className="flashcard-progress"
                value={currentIndex + 1}
                max={flashcards.length}
            />

            <button type="button" className="flashcard" onClick={() => setIsFlipped(!isFlipped)}>

                {isFlipped ? (
                    <>
                        <h3>{currentCard.back}</h3>
                        <p>{currentCard.explanation}</p>
                    </>
                ):(
                    <h3>{currentCard.front}</h3>
                )}

            </button>

            <p>Click to flip</p>

            <div className="flashcard-navigation">
                <button type="button" onClick={handlePrevious} disabled={currentIndex === 0}>
                    Previous 
                </button>

                <button type="button" onClick={handleNext} disabled={currentIndex === flashcards.length - 1}>
                    Next
                </button>
            </div>

        </section>
    )

}
export default FlashcardView
