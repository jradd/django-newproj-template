from django import template
from django.db.models import get_model


register = template.Library()


def do_latest_content(parser, token):
	"""
	Returns a specific number of entries for a particular model. (If the model is sorted by date published they will be sorted that way hence the name get_latest_content.)
	
	Example usage:
	
	{% load fetch_content %}
	{% get_latest_content application_name.model_name 5 as foo %}
	{% for bar in foo %}
		{{ bar.attribute }}
	{% endfor %}
	"""
	bits = token.split_contents()
	if len(bits) != 5:
		raise template.TemplateSyntaxError("'get_latest_content' takes exactly four arguments")
	model_args = bits[1].split('.')
	if len(model_args) != 2:
		raise template.TemplateSyntaxError("First argument to 'get_latest_content' must be an 'application name'.'model name' string")
	model = get_model(*model_args)
	if model is None:
		raise template.TemplateSyntaxError("'get_latest_content' tag got an invalid model: %s" % bits[1])
	return LatestContentNode(model, bits[2], bits[4]) # model to retrieve content from, number of items to retrieve, var name to store results in


class LatestContentNode(template.Node):
	def __init__(self, model, num, varname):
		self.model = model
		self.num = int(num)
		self.varname = varname
	def render(self, context):
		context[self.varname] = self.model._default_manager.all()[:self.num]
		return ''

register.tag('get_latest_content', do_latest_content)


def do_all_content(parser, token):
	"""
	Returns all entries for a particular model.

	Example usage:
	
	{% load fetch_content %}
	{% get_all_content application_name.model_name as foo %}
	{% for bar in foo %}
		{{ bar.attribute }}
	{% endfor %}
	"""
	bits = token.split_contents()
	if len(bits) != 4:
		raise template.TemplateSyntaxError("'get_all_content' takes exactly three arguments")
	model_args = bits[1].split('.')
	if len(model_args) != 2:
		raise template.TemplateSyntaxError("First argument to 'get_all_content' must be an 'application name'.'model name' string")
	model = get_model(*model_args)
	if model is None:
		raise template.TemplateSyntaxError("'get_all_content' tag got an invalid model: %s" % bits[1])
	return AllContentNode(model, bits[3]) # model to retrieve content from, var name to store results in


class AllContentNode(template.Node):
	def __init__(self, model, varname):
		self.model = model
		self.varname = varname
	def render(self, context):
		context[self.varname] = self.model._default_manager.all()
		return ''

register.tag('get_all_content', do_all_content)