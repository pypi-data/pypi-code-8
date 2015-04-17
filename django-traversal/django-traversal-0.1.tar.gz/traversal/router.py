# coding: utf-8
# TODO добавить совместимость с python3
# TODO добавить совместимость с django 1.8
from django.conf import settings
from django.views.defaults import page_not_found
import sys
import traceback
import importlib
from exceptions import KeyError


class Router(object):
    """
    Альтернативный роутер, реализующий патерн MVRT

    1) Получает корень дерева, path из request'a контекст = корень
    3) Пытается получить дочерний элемент от контекста передавая следующий элемент из списка vpath_tuple в качестве ключа
    4) ... см в начале
    """

    separator = '/'

    def __init__(self, request):
        try:
            self.root = self.get_path(settings.ROOT)('', None, request)
            self.context = self.root
            self.request = request
        except Exception as e:
            raise Exception(e)


    @staticmethod
    def get_path(path):
        """
        Импортирует объект по имени
        :param path: Принимает строку, содержащую путь к динамически импортируемому объекту с точками
        :return: Возвращает импортируемый объект
        """
        parts = path.split('.')
        module = ".".join(parts[:-1])
        # m = __import__(module)
        #  вызываю в обёртке, потому-что так рекомендует документация у __import__ очень не простое поведение
        print module
        m = importlib.import_module(module)
        m = getattr(m, parts[-1])
        return m

    @staticmethod
    def split_path_info(path, separator='/'):
        """
        Разбиваем path на сегменты, формируя vpath_list
        :param path:
        :return: vroot_list
        """

        if path[0] == separator:
            path = path[1:]
        vpath_list = path.split(separator)
        # vpath_list.remove('')
        return vpath_list

    def get_view(self, view_name, view_params):
        """
        Функция ищет подходящий данному контексту VIEW с декоратором get_traverse_context
        :return: возвращает представление (view)
        """
        try:
            exc_info = sys.exc_info()
            for t_factory_path in settings.TRAVERSE_FACTORIES:
                TFactory = self.get_path(t_factory_path)
                t_factory = TFactory(self.context, view_name)
                view = t_factory.traverse_factory()
                # Если находим - возвращаем вместе с параметрами
                if view:
                    return view(self.request, self.context, *view_params)

            # Если не нашли - выдаём 404
            return page_not_found(self.request)
        finally:
            # Display the *original* exception in traceback  исключая наше штатное KeyError
            if exc_info[0]:
                if not isinstance(exc_info[1], KeyError):
                    traceback.print_exception(*exc_info)
            del exc_info

    def resource_tree_traverse(self):
        """
        Проход по дереву ресурсов
        Находим контекст, представление, которое отвечает за его обработку или 404, 403 в перспективе,параметры для него
        :return: возвращаем список context, view_name, view_params
        """
        vroot_tuple = iter(self.split_path_info(self.request.path))
        view_name = ''  # в том случае если мы прошли контекст до конца - берётся view по умолчанию
        params = []
        for key in vroot_tuple:
            if key.find('+') + 1:
                keys = self.split_path_info(key, '+')
            else:
                keys = [key, ]
            # Проверяем, есть ли у текущего контекста дочерний ресурс с текущим ключём
            try:
                # Если ключ составной, передаём управление ресурсу с первым ключём,
                # ожидается что поведение всех ресурсов в составе ключа идентично (они объекты одного класса)
                brothers = []
                for single_key in keys:
                    brothers.append(self.context[single_key])
                # Первый из братьев отвечает за всех
                self.context = brothers[0]
                if len(keys) > 1:
                    self.context.brothers = brothers
                    brothers_source = self.context.get_brothers_source()

                    # Для поддержания логики архитектурного решения передаём в каждый из братских рессурсов информацию о остальных и данные
                    for brother in brothers:
                        brother.brothers = brothers
                        brother.brothers_source = brothers_source

            # Если нет такого дочернего ресурса, значит контекст определён, ищем view в данном контексте
            # по списку, заданному в settings
            except KeyError:
                view_name = key
                break

        for param in vroot_tuple:
            params.append(param)
        return self.get_view(view_name, params)


def route_factory(request, *args):
    router = Router(request)
    return router.resource_tree_traverse()