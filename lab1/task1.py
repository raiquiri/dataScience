import re

import pandas as pd

# Установить максимальное количество отображаемых столбцов
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', None)        # Убрать ограничение по ширине
pd.set_option('display.max_colwidth', None) # Показать полное содержимое ячеек

tables = pd.read_html('data.html')

# Подготовка данных
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

# Определение типов данных
df = df.astype(int)
# print(df.dtypes)

# 4. Определить средний, минимальный и максимальный суммарные баллы
print(f'4. Определить средний, минимальный и максимальный суммарные баллы')
column_name = 'Сумма баллов'

mean_value = df[column_name].mean()
max_value = df[column_name].max()
min_value = df[column_name].min()

print(f"Среднее значение: {mean_value}")
print(f"Максимальное значение: {max_value}")
print(f"Минимальное значение: {min_value}")

# 5. Средние значения по экзаменам
print(f'\n5. Средние значения по экзаменам')
subject1 = 'ХиХТ / Химия'
subject2 = 'АиНМА / Биология / Информатика и ИКТ / Математика / Физика'
subject3 = 'Русский язык'

mean_subject1 = df[subject1].mean()
mean_subject2 = df[subject2].mean()
mean_subject3 = df[subject3].mean()

df_mean = pd.DataFrame({
    subject1: [mean_subject1],
    subject2: [mean_subject2],
    subject3: [mean_subject3]
})

max_subject = df_mean.idxmax(axis=1)[0]
max_subject_value = df_mean.max(axis=1)[0]

print (f'\nТаблица средних:\n{df_mean}')
print(f'\nПредмет, по которому набирают больше всего баллов: {max_subject}')
print(f'Средний балл по этому предмету: {max_subject_value}')

# 6. Определить количество абитуриентов, у которых балла ЕГЭ по русскому ниже
# среднего балла по русскому языку, а по остальным предметам выше средних
print(f'\n6. Определить количество абитуриентов, у которых балла ЕГЭ по русскому ниже среднего балла по русскому языку, а по остальным предметам выше средних')

condition_subject1 = df[subject1] < mean_subject1
condition_subject2 = df[subject2] > mean_subject2
condition_subject3 = df[subject3] > mean_subject3

final_condition1 = condition_subject1 & condition_subject2 & condition_subject3

filtered_students1 = df[final_condition1]
count_filtered_students1 = len(filtered_students1)

print(f'Количество студентов: {count_filtered_students1}')

# 7. Определить количество абитуриентов, у которых балла ЕГЭ по русскому выше
# среднего балла по русскому языку, а по остальным предметам ниже средних
print(f'\n7. Определить количество абитуриентов, у которых балла ЕГЭ по русскому выше среднего балла по русскому языку, а по остальным предметам ниже средних')

condition_subject1 = df[subject1] > mean_subject1
condition_subject2 = df[subject2] < mean_subject2
condition_subject3 = df[subject3] < mean_subject3

final_condition2 = condition_subject1 & condition_subject2 & condition_subject3

filtered_students2 = df[final_condition2]
count_filtered_students2 = len(filtered_students2)
print(f'Количество студентов: {count_filtered_students2}')

# 8. Формирование итоговой таблицы
head = head.str.split(' - ', n=1, expand=True )
year = re.search(r'\.(\d{4})\.', date).group(1)
count_seats = seats.split(': ')[1].split('.')[0]

df_result = pd.DataFrame({
    head.iloc[0,0]: [head.iloc[0,1]],
    head.iloc[1,0]: [head.iloc[1,1]],
    head.iloc[2,0]: [head.iloc[2,1]],
    'Год': [year],
    'Количество мест': [count_seats],
    'Предметы ЕГЭ': [subject1 + " ; " +  subject2 + " ; " + subject3],
    'Средняя сумма баллов': [mean_value],
    'Min сумма баллов': [min_value],
    'Max сумма баллов': [max_value],
    'Предмет с высшим средним': [max_subject],
    'Кол-во студентов тип_1': [count_filtered_students1],
    'Кол-во студентов тип_2': [count_filtered_students2]
})
print(df_result)


print(df.columns[2])