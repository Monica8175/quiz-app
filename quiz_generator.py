import random

def generate_quiz(text):
    questions = []
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 40]

    for sentence in sentences:
        words = sentence.split()
        # Pick a meaningful word (longer than 4 chars) as the answer
        candidates = [w for w in words if len(w) > 4 and w.isalpha()]
        if not candidates:
            continue

        answer = random.choice(candidates)
        question_text = sentence.replace(answer, "_____", 1)

        # Generate wrong options from other words in the text
        all_words = [w for w in text.split() if len(w) > 4 and w.isalpha() and w != answer]
        wrong_options = random.sample(all_words, min(3, len(all_words)))

        options = [answer] + wrong_options[:3]
        random.shuffle(options)

        questions.append({
            "question": "Fill in the blank: " + question_text,
            "options": options,
            "answer": answer
        })

        if len(questions) == 5:
            break

    return questions
