import csv

def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def csv_to_formated_questions(filename):
    with open('csv_questions/'+filename, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        # asd = list(csv_reader)
        # print(asd)
        current_chapter = 1
        chapter_questions = list()
        for row in csv_reader:
            # the questions of chapter ends then save it in a new file
            if row['Chapter'] != '' and int(row['Chapter']) != current_chapter:
                save_chapter_questions(filename.split('.')[0], current_chapter, chapter_questions)
                current_chapter = int(row['Chapter'])
                chapter_questions.clear()
            # use the gift format to obtain the answers and question
            destructured_gift = row['GIFT FORMAT'].encode(encoding='ASCII', errors='ignore').decode().split('{')
            destructured_gift = {
                'question': destructured_gift[0].rstrip(),
                'answers': destructured_gift[1][0:-1].rstrip().split('\n')[1:]
            }

            formated_question = {
                'Q': destructured_gift['question'],
                "correct_answers": '',
                "wrong_answers": '',
            }
            wrong_answers = 1
            correct_answers = 1
            for answer in destructured_gift['answers']:

                if answer.startswith('~'):
                    formated_question["wrong_answers"] += f"WA{wrong_answers}: {answer[1:]}\n"
                    wrong_answers += 1
                else:
                    formated_question["correct_answers"] += f"CA{correct_answers}: {answer[1:]}\n"
                    correct_answers += 1

            formated_question["correct_answers"] = formated_question["correct_answers"].rstrip()
            formated_question["wrong_answers"] = formated_question["wrong_answers"].rstrip()
            # print(formated_question)
            # if current_chapter == 1:
            #     break
            chapter_questions.append(formated_question)
        if len(chapter_questions) > 0:
            save_chapter_questions(filename.split('.')[0], current_chapter, chapter_questions)


def save_chapter_questions(bookname:str, chapter: int, questions: list):
    text_questions = ''
    filename = f'questions_chapters/{bookname}_chapter_{chapter}.txt'
    for index, question in enumerate(questions):
        formated_question = open_file('questions_format.txt').replace('<<QUESTION>>', f"Q{index+1}: {question['Q']}")
        formated_question = formated_question.replace('<<CORRECT_ANSWERS>>', f"{question['correct_answers']}")
        formated_question = formated_question.replace('<<WRONG_ANSWERS>>', f"{question['wrong_answers']}")

        text_questions += formated_question+'\n\n'
    text_questions = text_questions.rstrip()
    save_file(text_questions, filename)


csv_to_formated_questions('masteringapi.csv')
