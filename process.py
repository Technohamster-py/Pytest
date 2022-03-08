"""
--------------------------------------------------
Programm by: Technohamster

Python version:        Year:
        3.8            2020

Thank you for using my programm! Good luck)
---------------------------------------------------
"""

from subprocess import run, PIPE, CalledProcessError, TimeoutExpired, STDOUT
import datetime


def check_py(file, indata, outdata, timer=1):
    """
    Функция обеспечивает разовый запуск программы с определенными фходными данными и возвращает ее вывод
    :param file: абсолютный путь к файлу,  должен быть защищен (r'folder\folder\file')
    :param indata: входные данные
    :param timer: время ожидания отклика прцесса, по истечении которого он будет принудительно остановлен
    :return: статус (True or False), выходные данные процесса или название ошибки, затраченное время
    """
    start_time = datetime.datetime.now()
    try:
        process = run([r'C:\Program Files\Python37\python.exe', file], stdout=PIPE,
                    input=indata, stderr=STDOUT, encoding='utf-8', timeout=timer)

        end_time = datetime.datetime.now()
        implemintation_time = end_time - start_time
        output = process.stdout.replace('\n', '|')

        if output == outdata:
            return True, output, implemintation_time
        else:
            return False, output, implemintation_time

    except CalledProcessError:
        return False, 'CalledProcessError', '0'

    except TimeoutExpired:
        return False, 'TimeoutExpired', f'more than {timer} seconds'
    except UnicodeDecodeError:
        return False, f'UnicodeError can not decode name of file {file}', '0'

if __name__ == '__main__':
    path = input('insert path to file\n')
    indata = input('insert input\n')
    outdata = input('insert expected output\n')
    timer = int(input('insert timer\n'))
    status, output, time = check_py(path, indata, outdata, timer)
    log = f'file: {path}\n input: {indata}\n output: {output}\n implemintation time: {time}'

    print(log)
