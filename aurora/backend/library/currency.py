from django.contrib.humanize.templatetags.humanize import intcomma

def toCurrency(digits):
    return intcomma(int(digits))
