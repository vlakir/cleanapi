from cleanapi.third_party_libs import importdir


def get_handlers(path_to_handlerd_dir: str) -> list:
    """
    Возвращает все хендлеры, лежащие в папке handlers
    :return: список хендлеров
    :rtype: list
    """

    path_to_handlerd_dir.strip('/')

    importdir.do(path_to_handlerd_dir.strip('/'), locals())
    list_handler_instances = []

    for key, value in locals().items():
        current_handler_instance = value
        if key.endswith('_handler'):
            list_handler_instances.append(current_handler_instance)

    return list_handler_instances
