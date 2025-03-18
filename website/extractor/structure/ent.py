from .document import Date

def result_to_str(result):
    formated_result = str()
    for i, cur_obj in enumerate(result):
        formated_result += cur_obj.text
        # текущий объект дата и следующий - дата, связанная с текущей
        if type(cur_obj) == Date and (i + 1 < len(result) and result[i + 1] == cur_obj.connection):
            formated_result += ' - '
        else:
            formated_result += '\n'
    return formated_result

class Ent:
    def __init__(self, input_info):
        self.text = None
        self.fact = input_info
        if type(input_info) == list:
            self.text = result_to_str(input_info)
        elif type(input_info) == str:
            self.text = input_info
        elif type(input_info):
            self.text = input_info.text

