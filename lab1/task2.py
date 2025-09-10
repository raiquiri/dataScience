import re
from typing import List

import pandas as pd
from pandas import DataFrame

# Установить максимальное количество отображаемых столбцов
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', None)        # Убрать ограничение по ширине
pd.set_option('display.max_colwidth', None) # Показать полное содержимое ячеек

# Подготовка данных
def preparing_data(tables: List[DataFrame]):
    date = tables[0].iloc[2][0]
    seats = tables[0].iloc[10][0]
    head = tables[0].iloc[4:7][0]
    df = tables[0].iloc[12:]
    column_names = df.iloc[0]
    df.columns = column_names
    df = df.iloc[1:]

    # Удаление лишних данных
    df = df.drop(columns=['№',
                          'Уникальный код',
                          'Представление приказа',
                          'Учебная группа',
                          'Идентификационный номер заказчика целевого обучения (для целевого приема)',
                          'Номер предложения (для целевого приема)'])
    df = df.dropna(axis=1, how='all')
    df = df.astype(int)

    return df, date, seats, head

def subject_stat(df: DataFrame):
    column_name = 'Сумма баллов'

    mean_value = df[column_name].mean()
    max_value = df[column_name].max()
    min_value = df[column_name].min()

    return mean_value, max_value, min_value

def subject_mean(df: DataFrame):
    subject1 = df.columns[1]
    subject2 = df.columns[2]
    subject3 = df.columns[3]

    mean_subject1 = df[subject1].mean()
    mean_subject2 = df[subject2].mean()
    mean_subject3 = df[subject3].mean()

    mean_values = {
        subject1: mean_subject1,
        subject2: mean_subject2,
        subject3: mean_subject3
    }

    # Находим максимальное значение и соответствующий предмет
    max_subject = max(mean_values, key=mean_values.get)

    return max_subject

def students_condition(df: DataFrame, main_condition, other_condition) -> DataFrame:
    subject1 = df.columns[1]
    subject2 = df.columns[2]
    subject3 = df.columns[3]

    mean_subject1 = df[subject1].mean()
    mean_subject2 = df[subject2].mean()
    mean_subject3 = df[subject3].mean()

    condition1 = main_condition(df[subject1], mean_subject1)
    condition2 = other_condition(df[subject2], mean_subject2)
    condition3 = other_condition(df[subject3], mean_subject3)

    final_condition = condition1 & condition2 & condition3
    filtered_students = df[final_condition]

    return len(filtered_students)

def result_data(tables: List[DataFrame]):
    df, date, seats, head = preparing_data(tables)
    mean_value, max_value, min_value = subject_stat(df)
    subject = subject_mean(df)
    count_students1 = students_condition(df,
                                         lambda x, mean: x > mean,
                                         lambda x, mean: x < mean)
    count_students2 = students_condition(df,
                                         lambda x, mean: x < mean,
                                         lambda x, mean: x > mean)
    head = head.str.split(' - ', n=1, expand=True)
    year = re.search(r'\.(\d{4})\.', date).group(1)
    count_seats = seats.split(': ')[1].split('.')[0]

    df_result = pd.DataFrame({
        head.iloc[0, 0]: [head.iloc[0, 1]],
        head.iloc[1, 0]: [head.iloc[1, 1]],
        head.iloc[2, 0]: [head.iloc[2, 1]],
        'Год': [year],
        'Количество мест': [count_seats],
        'Предметы ЕГЭ': [df.columns[1] + " ; " + df.columns[2] + " ; " + df.columns[3]],
        'Средняя сумма баллов': [mean_value],
        'Min сумма баллов': [min_value],
        'Max сумма баллов': [max_value],
        'Предмет с высшим средним': [subject],
        'Кол-во студентов тип_1': [count_students1],
        'Кол-во студентов тип_2': [count_students2]
    })

    return df_result

def main():
    tables = pd.read_html('data.html')
    result = result_data(tables)
    print(result)
if __name__ == '__main__':
    main()