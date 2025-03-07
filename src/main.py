import pandas as pd
import threading as tr
import time
from queue import Queue
import sys

from thread_functions import *
from print_functions import *
from update_data_functions import *


class EventLoop:
    def __init__(self):
        self.students = pd.read_csv(
            "../data/students.txt", sep=" ", header=None, names=["Student", "Sex"]
        )
        self.examiners = pd.read_csv(
            "../data/examiners.txt", sep=" ", header=None, names=["Examiner", "Sex"]
        )
        self.questions = pd.read_csv(
            "../data/questions.txt", header=None, names=["Question"]
        )

        self.lock = tr.Lock()
        self._add_field_in_students_table()
        self._add_field_in_examiners_table()
        self._add_field_in_question_table()
        self.students_q = Queue()
        for student in self.students["Student"]:
            self.students_q.put(student)
       

    def _add_field_in_students_table(self):
        self.students["Status"] = "Queue"
        self.students["Number of correct answers"] = 0
        self.students["Initial Order"] = range(len(self.students))
        self.students["Exam time"] = 0.0

    def _add_field_in_examiners_table(self):
        self.examiners["Current student"] = "-"
        self.examiners["Total students"] = 0
        self.examiners["Failed"] = 0
        self.examiners["Working time"] = 0.0

    def _add_field_in_question_table(self):
        self.questions["Number of correct answers"] = 0

    def event_loop(self):
        self.time_start = time.time()
        self._update_exam_info()
        self._threads_handler()
        self._update_exam_info(final_results=True)

    _print_table = print_table
    _print_last_info = print_last_info
    _update_exam_info = update_exam_info
    _print_initial_data = print_initial_data
    _clear_console = clear_console

    _update_examiners_data = update_examiners_data
    _update_student_data = update_student_data
    _update_questions_data = update_questions_data

    _threads_handler = threads_handler
    _examiner_thread = examiner_thread
    _student_thread = student_thread
    _question_thread = question_thread

    _interruptible_sleep = interruptible_sleep


def main() -> int:
    try:
        loop = EventLoop()
        loop.event_loop()
    except KeyboardInterrupt:
        print("Программа завершена пользователем.")
        sys.exit(0) 
    except Exception as e:
            print(f"Error: {e}")    
    return 0


main()
