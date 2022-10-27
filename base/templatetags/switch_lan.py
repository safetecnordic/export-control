from django import template

register = template.Library()

@register.filter
def switch_lan(str, lan):
    ind = -1
    if lan == "no":
        if '/en/' in str:
            ind = str.index('/en/')
            return  str[:ind]+"/no/"+str[ind+4:]
        elif '/no/' in str:
            return str
        else:
            return "/no" + str
    if lan == "en":
        if '/no/' in str:
            ind = str.index('/no/')
            return  str[:ind]+"/en/"+str[ind+4:]
        elif '/en/' in str:
            return str
        else:
            return "/en" + str
    return  str