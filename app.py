import os
from utils import query_constructor
from flask import Flask, request, Response
from flask_restx import abort


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/")
def starter_page() -> str:
    return f"Привет! Это стартовая страница, попробуйте запрос: /perform_query/?cmd1=filter&value1=POST"


@app.route("/perform_query/", methods=['GET', 'POST'])
def perform_query() -> Response:
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    try:
        cmd_1 = request.args.get('cmd_1')
        value_1 = request.args.get('value_1')
        cmd_2 = request.args.get('cmd_2')
        value_2 = request.args.get('value_2')
        file_name = request.args.get('file_name')

        if not (cmd_1 and value_1 and file_name):
            abort(400, 'Error 400 - Bad Request. Какой-то из параметров или файл отсутсвует')

    except:
        abort(400, 'Error 400 - Bad Request. Отсутствуеют необходимые параметры')

    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    file_path = os.path.join(DATA_DIR, str(file_name))
    if not os.path.exists(file_path):
        abort(400, 'Error 400 - Bad Request. Файл не найден')

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            result = query_constructor(str(cmd_1), str(value_1), file)
            if cmd_2 and value_2:
                result = query_constructor(str(cmd_2), str(value_2), iter(result))

    except:
        abort(404, 'Error - Не удалось прочитать файл')

    # вернуть пользователю сформированный результат
    return app.response_class("\n".join(result), content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)
