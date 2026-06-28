import random


def generate_quiz(text):

    questions = []


    # Split PDF text into sentences
    sentences = text.split(".")


    for sentence in sentences:

        sentence = sentence.strip()


        if len(sentence) > 30:


            words = sentence.split()


            # pick a random word as answer
            answer = random.choice(words)


            question_text = sentence.replace(
                answer,
                "_____"
            )


            options = [
                answer,
                "Option B",
                "Option C",
                "Option D"
            ]


            random.shuffle(options)


            questions.append({

                "question": 
                "Fill in the blank: " + question_text,

                "options": options,

                "answer": answer

            })


        if len(questions) == 5:
            break


    return questions
