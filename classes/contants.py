from collections import namedtuple

Month = namedtuple('Month', ['main', 'alt'])

MONTHS = (
    '',
    Month('Январь', 'января'),
    Month('Февраль', 'февраля'),
    Month('Март', 'марта'),
    Month('Апрель', 'апреля'),
    Month('Май', 'мая'),
    Month('Июнь', 'июня'),
    Month('Июль', 'июля'),
    Month('Август', 'августа'),
    Month('Сентябрь', 'сентября'),
    Month('Октябрь', 'октября'),
    Month('Ноябрь', 'ноября'),
    Month('Декабрь', 'декабря'),
)
