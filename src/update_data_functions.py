import numpy as np
import time


def update_examiners_data(
    self,
    examiner,
    examiner_time,
    student=None,
    after_student_thread=False,
    only_update_time=False,
):
    with self.lock:
        examiners_index = self.examiners.loc[
            self.examiners["Examiner"] == examiner
        ].index

        if not only_update_time:
            if not after_student_thread:
                self.examiners.loc[examiners_index, "Current student"] = student
            else:
                self.examiners.loc[examiners_index, "Current student"] = "-"
                self.examiners.loc[examiners_index, "Total students"] += 1

        self.examiners.loc[examiners_index, "Working time"] = round(
            time.time() - examiner_time, 2
        )


def update_student_data(self, examiner, student, exam_time):
    with self.lock:
        bool_list = self.students["Student"] == student
        student_data = self.students.loc[bool_list]

        self.students.loc[bool_list, "Exam time"] = exam_time

        mood = np.random.choice(["bad", "good", "neutral"], p=[1 / 8, 1 / 4, 5 / 8])
        passed = (mood == "good") or (
            mood == "neutral" and student_data["Number of correct answers"].iloc[0] >= 2
        )

        if passed:
            self.students.loc[bool_list, "Status"] = "Passed"
        else:
            self.students.loc[bool_list, "Status"] = "Failed"
            self.examiners.loc[self.examiners["Examiner"] == examiner, "Failed"] += 1


def update_questions_data(self, student, question):
    bool_list_s = self.students["Student"] == student
    bool_list_q = self.questions["Question"] == question
    with self.lock:
        self.students.loc[bool_list_s, "Number of correct answers"] += 1
        self.questions.loc[bool_list_q, "Number of correct answers"] += 1
