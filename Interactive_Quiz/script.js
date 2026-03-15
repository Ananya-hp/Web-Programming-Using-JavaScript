// Quiz questions array
const quizData = [
    {
        question: "What does HTML stand for?",
        options: [
            "Hyper Trainer Marking Language",
            "Hyper Text Markup Language",
            "Hyper Text Marketing Language",
            "Hyper Text Markup Leveler"
        ],
        correct: 1
    },
    {
        question: "Which language is used for styling web pages?",
        options: ["HTML", "JQuery", "CSS", "XML"],
        correct: 2
    },
    {
        question: "Which language is used for web interactivity?",
        options: ["Python", "Java", "C++", "JavaScript"],
        correct: 3
    },
    {
        question: "Which tag is used to link CSS to HTML?",
        options: ["<script>", "<style>", "<css>", "<link>"],
        correct: 3
    },
    {
        question: "Which symbol is used for comments in JavaScript?",
        options: ["<!-- -->", "/* */", "//", "#"],
        correct: 2
    }
];

// DOM elements
const questionEl = document.getElementById("question");
const optionEls = document.getElementsByName("option");
const optionTexts = [
    document.getElementById("option0"),
    document.getElementById("option1"),
    document.getElementById("option2"),
    document.getElementById("option3")
];
const nextBtn = document.getElementById("next-btn");
const quizBox = document.getElementById("quiz-box");
const resultBox = document.getElementById("result-box");
const scoreText = document.getElementById("score-text");
const messageText = document.getElementById("message-text");
const restartBtn = document.getElementById("restart-btn");

// Feedback elements
const feedbackText = document.getElementById("feedback-text");
const submitFeedbackBtn = document.getElementById("submit-feedback-btn");
const feedbackMsg = document.getElementById("feedback-msg");

// Quiz state
let currentQuestionIndex = 0;
let score = 0;

// Load question
function loadQuestion() {
    const currentQuestion = quizData[currentQuestionIndex];
    questionEl.textContent = currentQuestion.question;

    currentQuestion.options.forEach((option, index) => {
        optionTexts[index].textContent = option;
        optionEls[index].checked = false;
    });
}

// Get selected answer
function getSelectedAnswer() {
    let selected = null;
    optionEls.forEach((option) => {
        if (option.checked) {
            selected = parseInt(option.value);
        }
    });
    return selected;
}

// Show result
function showResult() {
    quizBox.classList.add("hidden");
    resultBox.classList.remove("hidden");

    scoreText.textContent = `Your Score: ${score} / ${quizData.length}`;

    if (score === quizData.length) {
        messageText.textContent = "Excellent! 🎉";
    } else if (score >= quizData.length / 2) {
        messageText.textContent = "Good Job! 👍";
    } else {
        messageText.textContent = "Try Again! 💪";
    }
}

// Next button click
nextBtn.addEventListener("click", () => {
    const selectedAnswer = getSelectedAnswer();

    if (selectedAnswer === null) {
        alert("Please select an option before proceeding!");
        return;
    }

    if (selectedAnswer === quizData[currentQuestionIndex].correct) {
        score++;
    }

    currentQuestionIndex++;

    if (currentQuestionIndex < quizData.length) {
        loadQuestion();
    } else {
        showResult();
    }
});

// Restart quiz
restartBtn.addEventListener("click", () => {
    currentQuestionIndex = 0;
    score = 0;
    resultBox.classList.add("hidden");
    quizBox.classList.remove("hidden");
    loadQuestion();
});

// Feedback submit
submitFeedbackBtn.addEventListener("click", () => {
    if (feedbackText.value.trim() === "") {
        alert("Please write some feedback before submitting!");
        return;
    }

    feedbackMsg.textContent = "Thank you for your feedback! 😊";
    feedbackMsg.classList.remove("hidden");
    feedbackText.value = "";
});

// Initial load
loadQuestion();
