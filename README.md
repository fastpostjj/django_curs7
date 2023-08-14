## Курсовой проект "Трекер полезных привычек"

Бэкенд-часть SPA веб-приложения.

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек.
В книге хороший пример привычки описывается как конкретное действие, которое можно уложить в одно предложение:

я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

За каждую полезную привычку необходимо себя вознаграждать или сразу после делать приятную привычку. Но при этом привычка не должна расходовать на выполнение больше 2 минут.

Привычка:

Пользователь — создатель привычки.

Место — место, в котором необходимо выполнять привычку.

Время — время, когда необходимо выполнять привычку.

Действие — действие, которое представляет из себя привычка.

Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.

Связанная привычка — привычка, которая связана с другой привычкой (только для полезных привычек).

Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.

Вознаграждение — чем пользователь должен себя вознаградить после выполнения.

Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.

Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.

Каждый пользователь имеет доступ только к своим привычкам по механизму CRUD.



## Начало работы
Для начала работы необходимо создать пользователей командой python manage.py csu.

Логин пользователя- id в телеграме.

Новому пользователю генерируется пароль и высылается в телеграм.
Для того, чтобы привычки рассылались пользователю, у него должен быть установлен признак "подписан" (is_subscripted=True).

Настроены периодические задачи по проверке сообщений бота и создании новых пользователей, если они отправили сообщение боту, а также по рассылке привычек по расписанию (также запускаются по ручкам /habits/check_message_bot/ и /habits/send_message_bot/).
Периодические задачи проверки новых пользователей и задание расписания рассылки привычек устанавливаются командой python manage.py set_task.

Команда python manage.py bot устанавливает задачи по рассылке привычек по расписанию.


Команды для запуска celery и beat:

celery -A config worker -l INFO -P eventlet

celery -A config beat -l INFO
