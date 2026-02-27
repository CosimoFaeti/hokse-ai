from neomodel import config, AsyncStructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo


class Template(AsyncStructuredNode):
	""" """

	uid = UniqueIdProperty()
	description = StringProperty(required=True)
