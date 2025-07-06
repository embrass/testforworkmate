import argparse
import csv
from tabulate import tabulate


def load_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))


def apply_filter(data, condition):
    if not condition:
        return data

    operators = ['>=', '<=', '>', '<', '=']
    op = None
    for operator in operators:
        if operator in condition:
            op = operator
            column, value = condition.split(operator, 1)
            break

    if not op:
        raise ValueError(f"Недопустимый формат: {condition}. Используйте операторы {operators}")

    filtered = []

    for row in data:
        if column not in row:
            continue

        cell_value = row[column]

        try:
            cell_num = float(cell_value)
            value_num = float(value)

            if op == '=' and cell_num == value_num:
                filtered.append(row)
            elif op == '>' and cell_num > value_num:
                filtered.append(row)
            elif op == '<' and cell_num < value_num:
                filtered.append(row)
            elif op == '>=' and cell_num >= value_num:
                filtered.append(row)
            elif op == '<=' and cell_num <= value_num:
                filtered.append(row)

        except ValueError:
            if op == '=' and str(cell_value).strip().lower() == str(value).strip().lower():
                filtered.append(row)

    return filtered


def apply_aggregate(data, operation):
    if not operation:
        return None

    column, op = operation.split('=', 1)
    values = []

    for row in data:
        try:
            values.append(float(row[column]))
        except (ValueError, KeyError):
            continue

    if not values:
        return None

    if op == 'avg':
        return sum(values) / len(values)
    elif op == 'min':
        return min(values)
    elif op == 'max':
        return max(values)
    else:
        raise ValueError(f"Введен неверный параметр {op}")


def apply_sort(data, sort_condition):
    if not sort_condition:
        return data

    column, order = sort_condition.split('=', 1)
    reverse = (order.lower() == 'desc')

    try:
        return sorted(data, key=lambda x: float(x[column]), reverse=reverse)
    except ValueError:
        return sorted(data, key=lambda x: str(x[column]).lower(), reverse=reverse)


def main():
    parser = argparse.ArgumentParser(description='Обработка CSV файла')
    parser.add_argument('filename', help='Имя CSV файла')
    parser.add_argument('--where', help='Фильтрация в формате "column>value" или "column=value"')
    parser.add_argument('--aggregate', help='Агрегация в формате "column=operation" (avg/min/max)')
    parser.add_argument('--order-by', help='Сортировка в формате "column=order" (asc/desc)')
    args = parser.parse_args()

    try:
        data = load_csv(args.filename)

        if args.where:
            data = apply_filter(data, args.where)

        if args.order_by:
            data = apply_sort(data, args.order_by)

        if args.aggregate:
            result = apply_aggregate(data, args.aggregate)
            if result is not None:
                print(f"Результат: {(result)}$")
            else:
                print("Нет данных для агрегации")
            return


        if data:
            print(tabulate(data, headers="keys", tablefmt="grid"))
        else:
            print("Нет данных, соответствующих условиям фильтрации")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        parser.print_help()


if __name__ == "__main__":
    main()


# python main.py products.csv --where "brand=apple" --aggregate "price=max"
# python main.py products.csv --where --aggregate "price=max"
# python main.py products.csv --where "brand=apple" --order-by "price=asc"
# python main.py products.csv  --where "rating>4.0"