from exam.models import ExamQuestion


class Parser:
    def get_spent_time(self, total_spent_time, exam, question):
        total_time = total_spent_time.split(":")
        time_remain = (int(total_time[0]) * 60) + int(total_time[1])
        exam_question_obj = ExamQuestion.objects.get(exam=exam, question__question=question)
        time_spent = exam_question_obj.time_per_question - time_remain
        return time_spent

data_parser = Parser()
