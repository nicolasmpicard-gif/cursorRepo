const quizScreen = document.getElementById("quiz-screen");
const resultsScreen = document.getElementById("results-screen");
const topicTag = document.getElementById("topic-tag");
const progress = document.getElementById("progress");
const questionText = document.getElementById("question-text");
const optionsContainer = document.getElementById("options");
const feedback = document.getElementById("feedback");
const resultLabel = document.getElementById("result-label");
const explanation = document.getElementById("explanation");
const nextBtn = document.getElementById("next-btn");
const scoreSummary = document.getElementById("score-summary");
const scoreDetail = document.getElementById("score-detail");
const restartBtn = document.getElementById("restart-btn");

let questions = [];
let currentIndex = 0;
let score = 0;
let answered = false;

function shuffle(array) {
  const copy = [...array];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function startQuiz() {
  questions = shuffle(QUESTIONS);
  currentIndex = 0;
  score = 0;
  answered = false;

  quizScreen.classList.remove("hidden");
  resultsScreen.classList.add("hidden");
  renderQuestion();
}

function renderQuestion() {
  const current = questions[currentIndex];
  answered = false;

  topicTag.textContent = current.topic;
  progress.textContent = `Question ${currentIndex + 1} of ${questions.length}`;
  questionText.textContent = current.question;

  optionsContainer.innerHTML = "";
  feedback.classList.add("hidden");
  nextBtn.classList.add("hidden");

  current.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "option";
    button.textContent = option;
    button.addEventListener("click", () => selectAnswer(index, button));
    optionsContainer.appendChild(button);
  });
}

function selectAnswer(selectedIndex, selectedButton) {
  if (answered) {
    return;
  }

  answered = true;
  const current = questions[currentIndex];
  const isCorrect = selectedIndex === current.correct;

  if (isCorrect) {
    score += 1;
  }

  const optionButtons = optionsContainer.querySelectorAll(".option");
  optionButtons.forEach((button, index) => {
    button.disabled = true;

    if (index === current.correct) {
      button.classList.add("correct");
    }

    if (index === selectedIndex && !isCorrect) {
      button.classList.add("incorrect");
    }

    if (index === selectedIndex) {
      button.classList.add("selected");
    }
  });

  resultLabel.textContent = isCorrect ? "Correct!" : "Not quite.";
  resultLabel.className = `result-label ${isCorrect ? "correct" : "incorrect"}`;
  explanation.textContent = current.explanation;

  feedback.classList.remove("hidden");
  nextBtn.classList.remove("hidden");
  nextBtn.textContent =
    currentIndex === questions.length - 1 ? "See results" : "Next question";
}

function showResults() {
  quizScreen.classList.add("hidden");
  resultsScreen.classList.remove("hidden");

  const percent = Math.round((score / questions.length) * 100);
  scoreSummary.textContent = `You scored ${score} out of ${questions.length} (${percent}%)`;
  scoreDetail.textContent =
    percent === 100
      ? "Perfect score — great work."
      : "Review the explanations and try again to reinforce the material.";
}

nextBtn.addEventListener("click", () => {
  if (currentIndex < questions.length - 1) {
    currentIndex += 1;
    renderQuestion();
    return;
  }

  showResults();
});

restartBtn.addEventListener("click", startQuiz);

startQuiz();
