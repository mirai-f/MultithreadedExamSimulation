import os
import time
import numpy as np
from tabulate import tabulate


def print_table(self, table, columns):
    print(
        tabulate(
            table[columns],
            headers="keys",
            tablefmt="grid",
            showindex=False,
        )
    )


def print_last_info(self, final_results=False):
    if not final_results:
        print(
            f"Remaining in queue: {len(self.students[self.students['Status'] == 'Queue'])} out of {len(self.students)}"
        )
        print(f"Time since exam start: {round(time.time() - self.time_start, 2)}")
    else:
        bool_list_pass = self.students["Status"] == "Passed"
        min_exam_time_pass = self.students.loc[bool_list_pass, "Exam time"].min()
        top_students = self.students.loc[
            (bool_list_pass) & (self.students["Exam time"] == min_exam_time_pass),
            "Student",
        ]

        failure_rate = self.examiners["Failed"] / self.examiners[
            "Total students"
        ].replace([np.inf, -np.inf], np.nan)
        self.examiners["Failure rate"] = failure_rate
        min_failure_exam_rate = failure_rate.min()
        top_examiners = self.examiners.loc[
            self.examiners["Failure rate"] == min_failure_exam_rate, "Examiner"
        ]

        bool_list_fail = self.students["Status"] == "Failed"
        min_exam_time_fail = self.students.loc[bool_list_fail, "Exam time"].min()
        expelled_students = self.students.loc[
            (bool_list_fail) & (self.students["Exam time"] == min_exam_time_fail),
            "Student",
        ]

        max_number_of_correct_answers = self.questions[
            "Number of correct answers"
        ].max()
        top_ans = self.questions.loc[
            self.questions["Number of correct answers"]
            == max_number_of_correct_answers,
            "Question",
        ]

        pass_rate = len(self.students[bool_list_pass]) / len(self.students)

        print(
            f"Time from the start of the exam to its completion: {round(time.time() - self.time_start, 2)}"
        )
        print(f"Names of top students: {', '.join(top_students.tolist())}")
        print(f"Names of top examiners: {', '.join(top_examiners.tolist())}")
        print(
            f"Names of students who will be expelled after the exam: {', '.join(expelled_students.tolist())}"
        )
        print(f"Best questions: {', '.join(top_ans.tolist())}")
        print(f"Result: the exam was {'' if pass_rate > 0.85 else 'un'}successful")


def update_exam_info(self, final_results=False):
    self._clear_console()
    status_order = {"Queue": 0, "Passed": 1, "Failed": 2}
    self.students = self.students.sort_values(
        by=["Status", "Initial Order"],
        key=lambda x: x.map(status_order) if x.name == "Status" else x,
    )

    students_columns = ["Student", "Status"]
    self._print_table(self.students, students_columns)
    print()

    examiner_columns = ["Examiner", "Total students", "Failed", "Working time"]
    if not final_results:
        examiner_columns.insert(1, "Current student")
    self._print_table(self.examiners, examiner_columns)
    print()

    # self._print_table(self.questions, ["Question", "Number of correct answers"])

    self._print_last_info(final_results)
    print()
    print()


def print_initial_data(self):
    print(self.examiners[self.examiners["Current student"] == "-"])
    while not self.students_q.empty():
        item = self.students_q.get()
        if item == "Петр":
            self.students.loc[self.students["Student"] == item, "Status"] = "Passed"
        print(item)

    print(tabulate(self.students, headers="keys", tablefmt="grid", showindex=False))
    print(tabulate(self.examiners, headers="keys", tablefmt="grid", showindex=False))
    print(tabulate(self.questions, headers="keys", tablefmt="grid", showindex=False))
    pass


def clear_console(self):
    os.system("cls" if os.name == "nt" else "clear")
