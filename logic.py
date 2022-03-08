"""
--------------------------------------------------
Programm by: Technohamster

Python version:        Year:
        3.8            2020

Thank you for using my programm! Good luck)
---------------------------------------------------
"""

import os, process, excelwriter, datetime


def load_answers(path):
    """
    Загрузка эталонных данных, конфигурирование словаря с критериями оценки
    :param path: папка с файлом эталонных данных и файлом с критериями
    :return: словарь данных {input[]: expect output}, словарь оценок {5: criteria, 4: criteria, 3: criteria}
    """
    answers = {}
    criteria = {}
    indata_path = path + '/CorrectData.txt'
    criteria_path = path + '/Marks.txt'

    with open(indata_path) as inf:
        for line in inf:
            text = line.strip()
            text = [i for i in text.split('[]')]
            correcttext = text[0].replace('|', '\n')
            answers[correcttext] = text[1]

    with open(criteria_path) as inc:
        for line in inc:
            text = line.strip()
            text = [i for i in text.split('|')]
            criteria[float(text[1])] = text[0]

    return answers, criteria



def start_checking(correct_dir, test_dir, xlfile=None):
    """
    Основная функция, запускающая проверку
    :param correct_dir: Папка с файлом ответов и критериями оценки
    :param test_dir: Папка с тестируемыми файлами
    :param xlfile: файл excel для записи ответов
    :return:
    """
    test_files = load_files(test_dir)
    task_number = [m for m in [i for i in correct_dir.split('-')][1].split('.')][0]
    answers, criteria = load_answers(correct_dir)

    log_path, err_path = init_log()

    journal = {}
    for file in test_files:
        filename = test_dir + r'\{}'.format(file)
        test_cnt = 0
        ok_tests = 0
        wrong_tests = 0
        title = f'initialisation {file}'
        log_write(log_path, title)
        for indat in answers.keys():
            answer = answers[indat]
            status, output, time = check(filename, indat, answer)
            indat = indat.replace('\n', '|')
            if status is None:
                raport = 'Testing failed: invalid file extension'
                log_write(log_path, raport)
                log_write(err_path, raport)
                break

            if status:
                status = 'OK'
                ok_tests += 1
                raport = f'\ttest {test_cnt}-----{status}, time spent: {time}\n'
            else:
                status = 'WRONG'

                if wrong_tests == 0:
                    log_write(err_path, title)

                wrong_tests += 1

                raport = f'\ttest {test_cnt}-----{status}, input: {indat}, output: {output}, expected output: {answer},' \
                         f' time spent: {time}\n'
                log_write(err_path, raport)

            log_write(log_path, raport)
            test_cnt += 1
        if status is not None:
            percent = ok_tests / test_cnt * 100
            mark = '2'
            for part in criteria.keys():
                if percent >= part:
                    mark = criteria[part]

        student_name = [i for i in file.split('-')][0]
        journal[student_name] = mark
        log_write(log_path, f'\nTesting of {file} finished\n\tOK tests: {str(ok_tests)}\n\tFaled tests: {str(wrong_tests)}\n\t'
                  f'Percent of correct answers: {str(percent)}%\n\tMark: {mark}\n=======================\n')
    write_marks(xlfile, journal, task_number, log_path, err_path)


def log_write(path, string):
    """
    Запись в лог с отчетом о проверке
    :param path: путь к log-файлу
    :param string: строка
    :return:
    """
    with open(path, 'a') as printlog:
        printlog.write(string)


def init_log():
    """
    Создание общего лог файла и файла с ошибками
    :return: имя общего файла, имя файла ошибок
    """
    date_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    name = f'test_log-{date_time}.txt'
    errors_name = f'errors_log-{date_time}.txt'
    with open(name, 'w') as printlog:
        printlog.write(f'{date_time}\nImporting packages...\nloading files...\n start checking...\n, ================')

    with open(errors_name, 'w') as printerr:
        printerr.write(f'{date_time}\nERRORS:\n')

    return name, errors_name


def load_files(path):
    """Импорт проверямых программ
    Функция загружает список файлов в папке"""
    fileslist = os.listdir(path)
    return fileslist


def write_marks(path, students_list, task_number, log_path, err_path):
    """

    :param path: Путь к таблице
    :param students_list: имена с оценками
    :param task_number: номер задания (task_number + 1 = номер столбца)
    :param log_path: файл лога
    :param err_path: файл лога ошибок
    :return: None
    """
    if path:
        log, errors = excelwriter.write(path, students_list, task_number)
        log_write(log_path, log)
        log_write(err_path, errors)
    else:
        date_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
        name = f'journal-{date_time}.txt'
        with open(name, 'w') as jrnlw:
            jrnlw.write('Name:\tMark:\n')
            for student_name in students_list.keys():
                mark = students_list[student_name]
                line = f'{student_name} - {mark}\n'
                jrnlw.write(line)

def check_readable(file):
    """
    Проверка расшиерния файла. Функция возвращает 0, если расширение файла .py и ошибку ExpansionError, если нет
    :param file: абсолютное имя файла
    :return:
    """
    if file [-3:] == '.py':
        return True
    else:
        expansion = [i for i in file.split('.')]
        expansion= expansion[-1]
        message = f'ExpansionError: incorrect file expansion {expansion=}, expected ".py"'
        return message


def check(file, inp, expect_output, timer=1):
    """
    Функция вызывает проверку файла, возвращает True, если выходные данные совпадают с эталонными
    и False если нет, выходные данные программы и затраченное время.
    :param file: абсолютное имя файла
    :param inp: входные данные
    :param expect_output: ожидаемые выходные данные
    :param timer: максимально разрешенное время ожидания
    :return: статус выполнения, вывод программы, затраченное время
    """
    possible = check_readable(file)
    if possible:
        status, output, time = process.check_py(file, inp, expect_output, timer)
        return status, output, time
    else:
        return None, 0, 0


if __name__ == "__main__":
    answer = input('Укажите полный путь к проверяемому файлу\n')
    correct_data = input('Укажите полный путь к проверяющему файлу\n')
    while True:
        table_path = input('Укажите путь к файлу .xls для записи оценок\n')
        if table_path[-4:] == '.xls':
            break
        else:
            print('Файл имеет недопустимое расширение, необходимо расширение .xls!\n')
