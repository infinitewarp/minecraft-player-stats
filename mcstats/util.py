from collections import defaultdict
import locale


# borrowed from https://gist.github.com/hrldcpr/2012250
def tree():
    return defaultdict(tree)


def pretty_time(minutes, units_count=4):
    units = [
        ('year', minutes / 525600),
        ('day', minutes % 525600 / 1440),
        ('hour', minutes % 3600 / 60),
        ('minute', minutes % 60),
    ]

    included = []
    for unit, amount in units:
        if amount > 0:
            formatted = '{0} {1}'.format(amount, unit) if unit == 1 else '{0} {1}s'.format(amount, unit)
            included.append(formatted)
            units_count -= 1
        if units_count == 0:
            break

    return ', '.join(included)


def pretty_count(number):
    # TODO improve locale support based on the request
    locale.setlocale(locale.LC_ALL, 'en_US')
    return locale.format("%d", number, grouping=True)


def pretty_count_truncate(number):
    if number > 1000000:
        return '{.1d}M'.format(number % 1000000)
    if number > 1000:
        return '{}k'.format(number % 1000)
    return '{}'.format(number)
