a = str(input('введите числа через пробел'))
element = int(input('введите число'))
array = a.split()
print(array)

for i, item in enumerate(array):
    array[i] = int(item)

array.append(element)

def sorting(array):
    for i in range(len(array)):
        for j in range(len(array) - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array

sorting(array)
print(array)

def binary_search(array, element, left, right):
    if left > right:  # если левая граница превысила правую,
        return False  # значит элемент отсутствует

    middle = (right + left) // 2  # находим середину
    if array[middle] == element:  # если элемент в середине,
        return middle  # возвращаем этот индекс
    elif element < array[middle]:  # если элемент меньше элемента в середине
        # рекурсивно ищем в левой половине
        return binary_search(array, element, left, middle - 1)
    else:  # иначе в правой
        return binary_search(array, element, middle + 1, right)

if element == min(array):
    print('введенное число находится в начале списка')
elif element == max(array) and array.count(element) == 1:
    print('введенное число находится в конце списка')
else:
    print(f"Предшествующий числу {element} индекс = ", (binary_search(array, element, 0, len(array) - 1)))
