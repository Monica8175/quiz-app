console.log("JS Connected 🚀");

const fileInput = document.getElementById("pdfFile");
const fileName = document.getElementById("fileName");
const generateBtn = document.querySelector(".generate-btn");

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        fileName.textContent = "Selected: " + fileInput.files[0].name;
    }
});

generateBtn.addEventListener("click", () => {
    let file = fileInput.files[0];
    if (!file) {
        alert("Please upload a PDF first 📄");
        return;
    }

    let formData = new FormData();
    formData.append("pdf", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayQuiz(data.quiz);
    })
    .catch(error => {
        console.log(error);
        alert("Something went wrong ❌");
    });
});

function displayQuiz(quiz) {
    // Remove old quiz if exists
    const old = document.querySelector(".quiz-container");
    if (old) old.remove();

    let quizArea = document.createElement("div");
    quizArea.className = "quiz-container";
    quizArea.innerHTML = "<h2>🧠 Generated Quiz</h2>";

    quiz.forEach((q, index) => {
        let questionBox = document.createElement("div");
        questionBox.className = "question-box";
        questionBox.innerHTML = `
            <h3>Q${index + 1}. ${q.question}</h3>
            ${q.options.map(option => `
                <label>
                    <input type="radio" name="q${index}">
                    ${option}
                </label>
            `).join("")}
        `;
        quizArea.appendChild(questionBox);
    });

    document.querySelector(".container").appendChild(quizArea);
}
