import re
from typing import Iterator, List, Any


# с помощью функционального программирования (функций filter, map),
# итераторов/генераторов сконструировать запрос
def query_constructor(cmd: str, value: Any, data: Iterator) -> List[Any]:
    """ Конструктор запроса с использованием ФП """
    if cmd == 'filter':
        result = list(filter(lambda x: value in x, data))
        return result

    if cmd == 'map':
        value = int(value)
        result = list(map(lambda x: x.split(" ")[value], data))
        return result

    if cmd == 'unique':
        result = list(set(data))
        return result

    if cmd == 'sort':
        reverse = bool(value)
        result = list(sorted(data, reverse=reverse))
        return result

    if cmd == 'limit':
        value = int(value)
        result = list(data)[:value]
        return result

    if cmd == 'regex':
        regex = re.compile(value)
        result = list(filter(lambda x: regex.search(x), data))
        return result

    return []
