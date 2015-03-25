# -*- coding: utf-8 -*-

dictionary = \
{
    'lang':                             u'ru',
#admin fields
    'admin':                            u'Администратор',
    'catalogs':                         u'Справочники',
    'journals':                         u'Журналы',
    'tables':                           u'Таблицы',
    'reports':                          u'Отчеты',
    'details':                          u'Подч.таблицы',
    'id':                               u'ID записи',
    'deleted_flag':                     u'Приз.удаления',
    'caption':                          u'Наимен.',
    'name':                             u'Имя',
    'table_name':                       u'Таблица',
    'template':                         u'Шаблон отчета',
    'report_module':                    u'Модуль отчета',
    'params_template':                  u'UI парам.',
    'view_template':                    u'UI просм.',
    'edit_template':                    u'UI редакт.',
    'filter_template':                  u'UI фильт.',
    'visible':                          u'Вид.',
    'client_module':                    u'Модуль клиента',
    'web_client_module':                u'Модуль web-клиента',
    'server_module':                    u'Модуль сервера',
    'report_module':                    u'Модуль отчета',
    'project':                          u'Проект',
    'users':                            u'Пользователи',
    'roles':                            u'Роли',
    'privileges':                       u'Права',
    'tasks':                            u'Задача',
    'safe_mode':                        u'Безопасный режим',
    'language':                         u'Язык',
    'author':                           u'Автор',
    'interface':                        u'Интерфейс',
    'db_type':                          u'Тип базы',
    'db_name':                          u'Имя файла',
    'alias':                            u'База данных',
    'data_type':                        u'Тип',
    'filter_type':                      u'Тип фильтра',
    'size':                             u'Длина',
    'object':                           u'Объект',
    'object_field':                     u'Поле объекта',
    'master_field':                     u'Связать с',
    'required':                         u'Обязат.',
    'calculated':                       u'Вычисл.',
    'default':                          u'По умолч.',
    'read_only':                        u'Неизмен.',
    'alignment':                        u'Выравн.',
    'active':                           u'Активный',
    'date':                             u'Дата',
    'role':                             u'Роль',
    'info':                             u'Информация',
    'item':                             u'Таблица',
    'can_view':                         u'Просмотр',
    'can_create':                       u'Создание',
    'can_edit':                         u'Изменение',
    'can_delete':                       u'Удаление',
    'fields':                           u'Поля',
    'field':                            u'Поле',
    'filter':                           u'Фильтр',
    'apply':                            u'Применить',
    'filters':                          u'Фильтры',
    'index':                            u'Индекс',
    'index_name':                       u'Имя индекса',
    'report_params':                    u'Параметры отчета',
    'error':                            u'Ошибка',
#admin interface
    'db':                               u'База',
    'export':                           u'Экспорт',
    'import':                           u'Импорт',
    'viewing':                          u'Просмотр',
    'editing':                          u'Редактирование',
    'filters':                          u'Фильтры',
    'order':                            u'Порядок',
    'indices':                          u'Индексы',
    'select_all':                       u'Выбрать все',
    'unselect_all':                     u'Отменить все',
    'project_params':                   u'Параметры проекта',
    'project_locale':                   u'Локализация',
#editor
    'case_sensitive':                   u'С учетом регистра',
    'whole_words':                      u'Совпадение всего слова',
    'in_task':                          u'В задаче',
    'text_not_found':                   u'Текст не найден.\nПерейти в начало и возобновить поиск',
    'text_changed':                     u'Текст был изменен. Сохранить?',
    'go_to_line':                       u'Перейти на строку',
    'go_to':                            u'Перейти',
    'line':                             u'Строка',
#admin editors
    'caption_name':                     u'Имя',
    'caption_word_wrap':                u'Перен.',
    'caption_expand':                   u'Расш.',
    'caption_edit':                     u'Ред.',
    'caption_descening':                u'По убыв.',
#admin messages
    'fill_task_attrubutes':             u'Введите имя, наименование и тип базы данных.',
    'can_not_connect':                  u'Не возможно подключиться к базе данных задачи. %s',
    'field_used_in_filters':            u'Нельзя удалить поле %s.\n Используется в определении фильтров:\n%s',
    'field_used_in_fields':             u'Нельзя удалить поле %s.\n Используется в определении полей:\n%s',
    'field_used_in_indices':            u'Нельзя удалить поле %s.\n Используется в определении индексов:\n%s',
    'field_is_system':                  u'Нельзя удалить системное поле.',
    'detail_mess':                      u'%s - подчиненная таблица %s',
    'item_used_in_items':               u'Нельзя удалить таблицу %s.\n Используется в определении таблиц:\n%s',
    'field_mess':                       u'%s - поле %s',
    'item_used_in_fields':              u'Нельзя удалить таблицу %s.\n Используется в определении полей:\n%s',
    'param_mess':                       u'%s - параметр %s',
    'item_used_in_params':              u'Нельзя удалить таблицу %s.\n Используется в определении параметров:\n%s',
    'invalid_name':                     u'Не верно задано имя.',
    'invalid_field_name':               u'Не верно задано имя поля.',
    'type_is_required':                 u'Не задан тип поля.',
    'index_name_required':              u'Не задано имя индекса.',
    'index_fields_required':            u'Не заданы поля индекса.',
    'cant_delete_group':                u'Удаление груп запрещено.',
    'object_field_required':            u'Не задано поле просмотра',
    'no_tasks_ptoject':                 u'В проекте отсутствуют задачи.',
    'stop_server':                      u'Остановить сервер',
#interface buttons and labels
    'yes':                              u'Да',
    'no':                               u'Нет',
    'ok':                               u'Сохранить',
    'cancel':                           u'Отменить',
    'delete':                           u'Удалить',
    'new':                              u'Добавить',
    'edit':                             u'Изменить',
    'copy':                             u'Копировать',
    'print':                            u'Печатать',
    'save':                             u'Сохранить',
    'open':                             u'Открыть',
    'close':                            u'Закрыть',
    'select':                           u'Отобрать',
    'filter':                           u'Фильтр',
    'find':                             u'Найти',
    'replace':                          u'Заменить',
    'view':                             u'Просмотреть',
    'log_in':                           u'Войти',
    'login':                            u'Логин',
    'password':                         u'Пароль',
    'log_out':                           u'Выйти',
#runtime messages
    'invalid_int':                      u'%s неверное значение - должно быть целое число',
    'invalid_float':                    u'%s неверное значение - должно быть число',
    'invalid_cur':                      u'%s неверное значение - должна быть сумма',
    'invalid_date':                     u'%s неверное значение - должна быть дата',
    'invalid_bool':                     u'%s неверное значение - должно быть логическое значение',
    'invalid_value':                    u'%s неверное значение',
    'value_required':                   u'Требуемое значение не задано',
    'invalid_length':                   u'Длина первышает мах. допустимую - %d',
    'save_changes':                     u'Данные были изменены. Сохранить?',
    'apply_changes':                    u'Данные не были сохранены на сервере. Сохранить?',
    'delete_record':                    u'Удалить выбранную запись?',
    'server_request_error':             u'Ошибка при выполнении запроса на сервер.',
    'cant_delete_used_record':          u'Удаление запрещено. Запись используется.',
    'website_maintenance':              u"На вебсайте проводятся технические работы.",
    'items_selected':                   u"выбрано: %d",
#rights messages
    'cant_view':                        u'%s: у Вас нет прав для просмотра',
    'cant_create':                      u'%s: у Вас нет прав для операции добавления',
    'cant_edit':                        u'%s: у Вас нет прав для операции изменения',
    'cant_delete':                      u'%s: у Вас нет прав для операции удаления',
#calendar
    'week_start':                        1,
    'days_min':                         [u'Вс', u'Пн', u'Вт', u'Ср', u'Чт', u'Пт', u'Сб', u'Вс'],
    'months':                           [u'Январь', u'Февраль', u'Март', u'Апрель', u'Май', u'Июнь', u'Июль', u'Август', u'Сентябрь', u'Октябрь', u'Ноябрь', u'Декабрь'],
    'months_short':                     [u'Янв', u'Фев', u'Мар', u'Апр', u'Май', u'Июн', u'Июл', u'Авг', u'Сен', u'Окт', u'Ноя', u'Дек'],
#grid
    'page':                             u'Стр.',
    'of':                               u'из'
}
