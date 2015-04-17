# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse


class Resource(object):
    """
    Каждый ресурс знает:
    __slug__ - как его зовут
    __parent__ - своего родителя
    children - список всех возможных классов своих детей
    request - имеет доступ к HTTP запросу
    source - имеет основное содержание, формируемое ещё на этапе маршрутизации, посредством метода get_source
    т.к. зачастую путь формируется исходя из возможности сформировать путь.
    В большинстве случаев get_source содержит запрос к БД
    parents - сущнность, для взаимодействия с родителями рессурса
    brothers - рессурс может иметь братьев, т.е. список экземпляров того же класса, связанных с данным рессурсом
    математической операцией ИЛИ, обозначаются в URL как resource+resource


    Продуктом работы ресурса является контекст, который он добавляет к view

    В идеале у ресурсов есть права доступа (ALE) ?ACL
    Несомненно, работа с правами доступа требует повышенного контроля, а значит унификации,
    и в будующем этот вопрос нужно решать, но я ещё не решил, как это сделать лучше всего.
    Однако по сути права доступа - это контекст, а методов для работы с контекстом в классе более чем достаточно

    Алгоритм действия ресурсов:
    1) Роутер передаёт управление корневому ресурсу, он имеет информацию о всех классах cвоих прямых потомков через children
    2) Рессурс добавляет в контекст свою логику (из get_source)
    3) Роутер пытается вызвать дочерний элемент с новым контекстом если у него получается, то повторяются пунты 2,3, иначе
    4) Роутер ищет view с именем ключа
    5) если получается, передаёт управление в view с полученным контекстом, и оставшимися в vpath_list параметрами, иначе обрабатывает исключение 404

    URL всегда соответствует Resource + View + [view_params]

    mixin - добавляет атрибуты и методы в класс

    """

    source = None  # Основное содержимое ресурса

    def __init__(self, slug, parent=None, request=None, source=None):
        self.__slug__ = slug
        self.__parent__ = parent
        self.request = request
        self.source = source
        self.children = self.children_factory()
        self.parents = self.Parents(self)
        self.brothers = [self, ]
        self.brothers_source = source
        self.full_list = self.__get_full_list()
        self.list = self.full_list
        # self.debug("init %s" % self.__class__.__name__)

    """
    Абстрактный интерфейс для работы с контекстом
    для взаимодействия с интерфейсом объект должен содержать следующие атрибуты
    list - модифицируемый интерфейсом список рессурсов
    full_list - полный список рессурсов (без фильтрации) для заданного рессурса
    """

    @staticmethod
    def base_all(obj):
        obj.list = obj.full_list
        return obj

    @staticmethod
    def base_filter(obj, filtered_classes):
        obj.list = []
        for parent in obj.full_list:
            for filtered_class in filtered_classes:
                if isinstance(parent, filtered_class):
                    obj.list.append(parent)

        return obj

    @staticmethod
    def base_exclude(obj, excluded_classes):
        obj.list = obj.full_list[:]
        for index, parent in enumerate(obj.list):
            for excluded_class in excluded_classes:
                if isinstance(parent, excluded_class):
                    obj.list.pop(index)
        return obj

    @staticmethod
    def base_get_all(obj, attr_name):
        """Возвращает все реализации члена или метода среди ресурсов-родителей по заданному имени атрибута
           Например: get_all('get_title') - вернёт список методов get_title ресурсов родителей, начиная от прямого потомка
        """
        attr_list = []
        for parent in obj.list:
            if attr_name in dir(parent):
                attr_list.append(getattr(parent, attr_name))

        return attr_list

    @staticmethod
    def base_get_and_call_all(obj, attr_name):
        """
        Похож на предыдущий метод, только вызывает каждый из списка возвращаемых методов
        :param attr_name:  имя возвращаемого метода
        :return: список результатов возвращаемых каждым из методов
        """
        attr_list = []
        for parent in obj.list:
            if attr_name in dir(parent):
                attr_list.append(getattr(parent, attr_name)())

        return attr_list

    @staticmethod
    def base_get_first(obj, attr_name):
        """Возвращает первую реализацию метода или члена среди родителей
           Фактически это эквивалент запроса ребёнка: Родители, дайте мне машинку,
           при этом запрос выполнит первый, кто сможет это сделать
           в случае, если никто из родителей не имеет искомого атрибута, вернёт None
        """
        for parent in obj.list:
            if attr_name in dir(parent):
                return getattr(parent, attr_name)
        return None

    @staticmethod
    def base_get_last(obj, attr_name):
        """Возвращает последнюю реализацию метода или члена среди родителей"""
        for parent in reversed(obj.list):
            if attr_name in dir(parent):
                return getattr(parent, attr_name)
        return None

    """
    Интерфейс для работы с контекстом в контексте рессурса
    """

    def __get_full_list(self):
        list = [self, ]
        list += self.parents.get_parents_list(self)
        return list

    def all(self):
        return self.base_all(self)

    def filter(self, filtered_classes):
        return self.base_filter(self, filtered_classes)

    def exclude(self, excluded_classes):
        return self.base_exclude(self, excluded_classes)

    def get_all(self, attr_name):
        return self.base_get_all(self, attr_name)

    def get_and_call_all(self, attr_name):
        return self.base_get_and_call_all(self, attr_name)

    def get_first(self, attr_name):
        return self.base_get_first(self, attr_name)

    def get_last(self, attr_name):
        return self.base_get_last(self, attr_name)

    """
    Группа методов для работы с братскими рессурсами
    """

    def get_brothers_all(self, attr_name):
        """
        Метод возвращает список значений аттрибута для каждого из братьев-рессурсов,
        ВАЖНО, у каждого брата должен быть данный атрибут
        :param attr_name: имя вызываемого метода или члена класса брата-рессурса
        :return:
        """
        attr_list = []
        for brother in self.brothers:
            attr_list.append(getattr(brother,attr_name))
        return attr_list

    def get_and_call_brothers_all(self, attr_name):
        """
        Очень похож на предыдущий метод, с той лишь разницей, что вызывает каждый из полученных методов
        :param attr_name: имя вызываемого метода
        :return:
        """
        attr_list = self.get_brothers_all(attr_name)
        attr_called_list = []
        for attr in attr_list:
            attr_called_list.append(attr())
        return attr_called_list

    def get_brothers_title(self):
        """Примитивный метод, демонстрирует взаимодействие с братскими ресурсами,
        ну и выдаёт перечень title братьев через запятую"""
        return ', '.join(self.get_and_call_brothers_all('get_title'))

    def is_have_brothers(self):
        """Флаг, возвращает истину, если у рессурса есть братья, и ложь, если нет"""
        if len(self.brothers) > 1:
            return True
        else:
            return False

    def get_brothers_source(self):
        """Возвращает queryset совместных данных рессурсов одного уровня (братьев)
        ПЕРЕОПРЕДЕЛИ МЕНЯ если необходима поддержка операции ИЛИ (+) """
        return None

    def __get_partical_source(self):
        """Возвращает часть выражения source предназначенную для обработки методом get_brother's source
        Вызывается в методе get_source, для поддержки  операции ИЛИ в рессурсах (+)
        ПЕРЕОПРЕДЕЛИ МЕНЯ В СВОЁМ РЕСУРСЕ, если требуется функционал составных рессурсов (+)"""
        return None

    class Parents():
        def __init__(self, context):
            self.context = context
            self.full_list = self.get_parents_list(self.context)
            self.list = self.full_list

        @staticmethod
        def get_parents_list(context):
            parents_list = []
            while context.__parent__:
                # учитываем братьев рессурса
                for brother in context.__parent__.brothers:
                    parents_list.append(brother)
                context = context.__parent__
            return parents_list

        """
        Интерфейс для работы с контекстом в контексте родителей рессурса
        """

        def all(self):
            return self.context.base_all(self)

        def filter(self, filtered_classes):
            return self.context.base_filter(self, filtered_classes)

        def exclude(self, excluded_classes):
            return self.context.base_exclude(self, excluded_classes)

        def get_all(self, attr_name):
            return self.context.base_get_all(self, attr_name)

        def get_and_call_all(self, attr_name):
            return self.context.base_get_and_call_all(self, attr_name)

        def get_first(self, attr_name):
            return self.context.base_get_first(self, attr_name)

        def get_last(self, attr_name):
            return self.context.base_get_last(self, attr_name)

    def get_parent(self):
        """
        :return: Возвращает ресурс родитель (в основном для использования в шаблонах, где нельзя применять "__")
        """
        return self.__parent__

    def get_title(self):
        """
        :return: Возвращает заголовок ресурса для поиска, желательно переопределить в своих ресурсах, иначе выводится slug
        """
        return self.__slug__

    def get_source(self, parent, key):
        """Переопределите метод get_source в своём ресурсе

        :type self: object
        :param parent: класс родитель передаёт свой экземпляр для досутпа к своим source и __parent__
        :param key: имя будущего ресурса
        :return: возвращает source в случае если с данным контекстом, по данному ключу есть результат иначе исключение
        """

        return None

    def __get_traversal_url(self):
        """
        Метод для внутреннего использования
        :param self: принимает ресурс
        :return: возвращает часть URL, сгенерированную непосредственно django_traversal (без корня)
        """
        path_list = []
        while self:
            # учитываем братьев в URL
            if self.is_have_brothers():
                path_list.append('+'.join(self.get_brothers_all('__slug__')))
            else:
                path_list.append(self.__slug__)
            self = self.__parent__

        #удаляем пустой корень
        del path_list[-1]

        vpath_tuple = reversed(path_list)
        traversal_url = '/'.join(vpath_tuple)
        return traversal_url

    def __get_parenet_url(self, url):
        """Метод обрезает URL вплоть до ближайшего справа разделителя, если разделителей нет - вернёт пустую строку
        Нужен для оптимизации, чтобы десять раз не парсить один и тот-же стек рессурсов
        :param url: строка url
        :return: Возвращает
        """
        # удаляем правую часть текущего URL до разделителя
        if url.count('/') > 1:
            return url.rsplit('/', 1)[0]
        else:
            return '/'

    def __breadcrumbs_append(self, current_url, breadcrumbs_list):
        """
        Добавляет значение в список
        :return: Возвращает
        """
        # проверяем, есть ли у текущего рессурса братья
        if self.is_have_brothers():
            parent_url = self.__get_parenet_url(current_url)
            breadcrumbs_list.append((current_url, self.get_brothers_title(), parent_url, self.get_brothers_all('__slug__')))
        else:
            breadcrumbs_list.append((current_url, self.get_title()))

        return breadcrumbs_list

    def get_breadcrumbs(self):
        """
        :return: возвращает список ссылок на всех родителей данного ресурса в формате (url,заголовок, [url-родителя рессурса, [список рессурсов-братьев] ])
        """
        breadcrumbs_list = []
        context = self

        if self.list == self.full_list:
            current_url = self.get_absolute_url()
            while context:
                breadcrumbs_list = context.__breadcrumbs_append(current_url, breadcrumbs_list)
                current_url = self.__get_parenet_url(current_url)
                context = context.__parent__
        else:
            # если применяем фильтрацию по классам, то экономичный алгоритм создания крошек уже не актуален,
            # создаём их индивидуально для каждого члена списка list:
            while context:
                if context in self.list:
                    current_url = context.get_absolute_url()
                    breadcrumbs_list = context.__breadcrumbs_append(current_url, breadcrumbs_list)
                context = context.__parent__

        breadcrumbs_list = breadcrumbs_list[::-1]
        return breadcrumbs_list

    def get_absolute_url(self):
        """
        :return: возвращает путь к текущему ресурсу
        """
        traversal_url = self.__get_traversal_url()
        url_root = reverse('router_root')
        absolute_url = url_root + traversal_url
        return absolute_url

    def get_first_resource_for_class_name(self, resource_class_name):
        """Возвращает первый экземпляр класса из контекста, по имени класса
        если в контексте нет экземпляров данного класса - вернёт None"""
        for resource in self.full_list:
            if resource.__class__.__name__ == resource_class_name:
                return resource.__class__
        return None

    def children_factory(self):
        """
        ПЕРЕОПРЕДЕЛИ МЕНЯ В СВОЁМ РЕСУРСЕ
        Фабрика для объявления списка потомков текущего ресурса
        :return: возвращает список классов ресурсов-потомков для данного класса
        """
        children = []  # ресурсы-потомки данного класса
        return children

    # Внимательно проектируем дерево, помня о пустых кверисетах
    def __getitem__(self, key):
        """
        В нашей архитектуре потомки определяются в __getitem__ ресурса-родителя, посредством вспомогательного класса
        при этом потомку приходит результат запроса к БД в виде инстанса

        Если не найден потомок - приходит keyError
        Вьюшку уже определяет сам роутер
        а непосредственно работать с основными данными ресурса можно через source

        """
        for Child in self.children:
            try:
                child = Child(key, self, self.request)
                child.source = child.get_source(self, key)
                child.brothers_source = child.source
                return child
            except (ObjectDoesNotExist, ValueError, KeyError):
                pass
            except Exception as e:
                raise Exception(e)
        raise KeyError
