# -*- coding: utf-8 -*-

# импорт
from pymymailru import PyMyMailRu, ApiError, MyMailUtil

# инициализация - передаем id приложения, секретный ключ и задаем формат выдачи
py_my_mail_ru = PyMyMailRu(691349, 'f3df6b05b28b283602071542c967c0b2', 'xml')
try:
    # получаем информацию о пользователях 1234567, 1234568 от лица пользователя 7654321
    #result = py_my_mail_ru.users_get_info('14517893456985249033', '4b52ba754ddf479b123704190f97555e')
    print (MyMailUtil()).link_to_uid('http://my.mail.ru/mail/grishin')
    result = py_my_mail_ru.achievements_list(1, 10, 'f331def1f5166338676926e030e11825')
    print result
# обработка ошибок
except ApiError, e:
    print e.code
    print e.message
