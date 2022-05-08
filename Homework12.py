money = input("Введите сумму, руб:")
money = int(money)
per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
deposit = list(per_cent.values())
for i, num in enumerate(deposit): deposit[i] = deposit[i] * (money)/100
for i, num in enumerate(deposit): deposit[i] = round(deposit[i])
print('deposit', '=', deposit)
deposit.sort()
print('Максимальная сумма, которую вы можете заработать ', '- ', deposit[-1], ' руб.')
