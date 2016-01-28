from django import template
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
	if re.search(pattern, request.path):
		return 'active'
	return ''

@register.filter
def get_dict_item(dictionary, key):
	# Вернет None, если ключа нет
	return dictionary.get(key)
