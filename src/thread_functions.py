import threading as tr
import numpy as np
import time


def interruptible_sleep(self, rest_time, condition_func, interval=0.1):
    elapsed_time = 0

    while elapsed_time < rest_time:
        if condition_func():
            break
        time.sleep(interval)
        elapsed_time += interval

    return elapsed_time


def threads_handler(self):
    self.number_of_examiners = len(self.examiners)
    self.threads = []

    for i in range(self.number_of_examiners):
        examiner_name = self.examiners.loc[i, "Examiner"]
        thread = tr.Thread(target=self._examiner_thread, args=(examiner_name,), daemon=True)
        self.threads.append(thread)
        thread.start()

    self.students_q.join()
    for thread in self.threads:
        thread.join()


def examiner_thread(self, examiner):
    examiner_time = time.time()

    was_rest = False
    while not self.students_q.empty():
        if time.time() - self.time_start < 30 or was_rest:
            student = self.students_q.get()

            self._update_examiners_data(examiner, examiner_time, student=student)
            self._update_exam_info()

            self._student_thread(examiner, student)

            self._update_examiners_data(
                examiner, examiner_time, after_student_thread=True
            )
            self._update_exam_info()

            self.students_q.task_done()
        else:
            rest_time = np.random.uniform(12, 18)
            elapsed_time = self._interruptible_sleep(
                rest_time, condition_func=lambda: self.students_q.empty()
            )
            examiner_time += elapsed_time
            was_rest = True


def student_thread(self, examiner, student):
    exam_time = np.random.uniform(len(examiner) - 1, len(examiner) + 1)
    questions = self.questions.sample(n=3).iloc[:, 0]
    for question in questions:
        self._question_thread(question, examiner, student)

    time.sleep(exam_time)

    self._update_student_data(examiner, student, exam_time)


def question_thread(self, question, examiner, student):
    question_words = question.split(" ")
    num_words = len(question_words)
    bool_list_s = self.students["Student"] == student
    sex = self.students.loc[bool_list_s, "Sex"].values[0]

    temp = num_words * (num_words + 1) / 2
    probabilities = []
    probabilities = [(i + 1) / temp for i in range(num_words)]
    if sex == "М":
        probabilities = probabilities[::-1]

    ans = np.random.choice(question_words, p=probabilities)
    correct_ans = set()
    correct_ans.add(np.random.choice(question_words).tolist())
    while 1 / 3 < np.random.random() and not (correct_ans == set(question_words)):
        new_word = np.random.choice(question_words).tolist()
        correct_ans.add(new_word)

    if ans in correct_ans:
        self._update_questions_data(student, question)
