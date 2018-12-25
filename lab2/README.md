## Лабораторна робота № 2.

1. Переробити програму з ЛР№1, переписавши запити доступу до баз даних у вигляді ORM. Рекомендована бібліотека: Python/SQLAlchemy (https://www.sqlalchemy.org/) або будь-яка подібна для інших мов програмування.

2. Реалізувати тригер та серверну процедуру, що автоматизує деяку задачу над базою даних з ЛР№1. Обидві процедури мають включати цикл та умовний оператор.

3. Проаналізувати у вигляді наочних прикладів з БД ЛР№1 реалізацію рівнів ізоляції транзакцій (READ COMMITTED, REPEATABLE READ, SERIALIZABLE) шляхом створення необхідних запитів у двох окремих транзакціях, слідкуючи за обсягом інформації, що повертається, та блокуванням транзакцій. Забезпечити можливість виявлення відповідних феноменів.