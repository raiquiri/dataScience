from selectors import SelectSelector

import pandas as pd
import numpy as np

# Установить максимальное количество отображаемых столбцов
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', None)        # Убрать ограничение по ширине
pd.set_option('display.max_colwidth', None) # Показать полное содержимое ячеек

df = pd.read_csv('BikeData.csv')
#print(df)

# 1. Создайте новую переменную Total_count, в которую записать общее количество арендованных велосипедов за каждый час.
df['Total count'] = df['Partner 1'] + df['Partner 2']
#print(df)

# 2. Удалите ряды Partner 1 и Partner 2
df = df.drop(columns=['Partner 1','Partner 2'])
#print(df)

# 3. Преобразуйте переменную Date к стандартной форме (to_datetime).
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
#print(df)

# 4. Определите сколько велосипедов было выдано в день, месяц и число которого совпадает с днем выполнения этого задания. Определите, какой это был день недели.
result = df[df['Date'].dt.month.eq(9) & df['Date'].dt.day.eq(23)]
bike_count = result['Total count'].sum()
day_of_week = result['Date'].iloc[0].day_name()
#print(f'Количество велосипедов за день: {bike_count})
#print(f'День недели: {day_of_week}')

# 5. Перекодируйте категориальную переменную переменную Functioning Day(рабочий или нерабочий день) в переменную типа boolean, т.е. "Yes"=True и "No" = False. Выведите количество нерабочих дней ( не часов ). День считается нерабочим, если пункт выдачи велосипедов работал менее 12 часов.
df['Functioning Day'] = df['Functioning Day'].map({'Yes': True, 'No': False})
#print(df['Functioning Day'].dtype)

weekend_count = 0
for mouth in range(1, 13):
    for day in range(1, 32):
        day_result = df[df['Date'].dt.month.eq(mouth) & df['Date'].dt.day.eq(day)]

        if day_result.empty:
            continue

        counts = day_result['Functioning Day'].value_counts()
        true_count = counts.get(True, 0)
        if true_count < 12:
            weekend_count += 1

#print(weekend_count)

# 6. Перекодируйте переменную Holiday (являлся ли день праздничным) в 0, если No Holiday, и 1, если Holiday. (используйте анонимную функцию lambda).
df['Holiday'] = df['Holiday'].apply(lambda x: 1 if x == 'Holiday' else 0)
#print(df)

# 7. Введите новую категориальную переменную Temperature category, которая будет равна
df['Temperature category'] = df['Temperature'].apply(lambda x: 'Freezing' if x < 0 else
                                                'Chilly' if 0 <= x < 15 else
                                                'Nice' if 15 <= x < 26 else
                                                'Hot')
#print(df)

# 8. Создайте новую переменную Good weather, которая будет равна 1 (т.е. хорошая погода), если
df['Good weather'] = np.where(
    (df['Temperature category'] == 'Nice') &
    (df['Humidity'] >= 40) & (df['Humidity'] <= 60) &
    (df['Wind speed'] < 5.4) &
    (df['Rainfall'] == 0) &
    (df['Snowfall'] == 0),
    1, 0)

good_weather_count = df['Good weather'].sum()
good_weather_percent = (good_weather_count / len(df)) * 100
#print(f'Наблюдений с хорошей погодой: {good_weather_count}')
#print(f'Процент наблюдений с хорошей погодой: {good_weather_percent:.2f}%')

# 9. Сгруппируйте данные по сезонам (Seasons), внутри сезона по категории погоды (Temperature category)
groups = df.groupby(['Seasons','Temperature category'])
groups_stat = groups[['Total count']].sum()
pivot_table = groups_stat.unstack(fill_value=0)
#print(groups_stat)
#print(pivot_table)

# 10. Определите сезон и температуру, при которых выдается наибольшее и наименьшее количество велосипедов.
max_rentals = groups_stat['Total count'].max()
min_rentals = groups_stat['Total count'].min()

max_group = groups_stat['Total count'].idxmax()
min_group = groups_stat['Total count'].idxmin()

print('Максимум')
print(f'Сезон: {max_group[0]};\tПогода: {max_group[1]};\tКоличество: {max_rentals}')
print('Минимум')
print(f'Сезон: {min_group[0]};\tПогода: {min_group[1]};\tКоличество: {min_rentals}')