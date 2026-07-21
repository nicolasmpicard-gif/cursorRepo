# Exam Quiz App

A simple local web app for practicing multiple-choice exam questions one at a time. After each answer, you get a one-sentence explanation of why the correct answer is correct.

## Run locally

From the repo root:

```bash
cd quiz-app
python3 -m http.server 8080
```

Then open [http://localhost:8080](http://localhost:8080) in your browser.

You can also open `quiz-app/index.html` directly in a browser, but using a local server is recommended.

## How it works

- Questions are defined in `quiz-app/questions.js`
- One question is shown at a time
- Choose an answer to see whether you were right and read a brief explanation
- Click **Next question** to continue
- At the end, you see your score and can restart

## Adding your course questions

Edit `quiz-app/questions.js` and add entries like this:

```javascript
{
  topic: "Exam outcome name",
  question: "Your question here?",
  options: ["Option A", "Option B", "Option C", "Option D"],
  correct: 0, // index of the correct option (0 = first)
  explanation: "One sentence explaining why the correct answer is correct.",
}
```

## Note

The attached course note images were not accessible in the cloud environment, so `questions.js` currently contains placeholder questions. Paste your exam outcomes and notes as text in chat to have the question bank populated from your materials.
