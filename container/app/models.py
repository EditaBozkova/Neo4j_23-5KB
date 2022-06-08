from graphql import GraphQLError
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from app import settings

graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)


class BaseModel(GraphObject):
    """
    Implements some basic functions to guarantee some standard functionality
    across all models. The main purpose here is also to compensate for some
    missing basic features that we expected from GraphObjects, and improve the
    way we interact with them.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def all(self):
        return self.match(graph)

    def save(self):
        graph.push(self)


class User(BaseModel):
    __primarykey__ = 'email'

    name = Property()
    surname = Property()
    age = Property()
    email = Property()

    def fetch(self):
        user = self.match(graph, self.email).first()
        if user is None:
            raise GraphQLError(f'"{self.email}" has not been found in our customers list.')

        return user

    def as_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'age': self.age,
            'email': self.email
        }


class Group(BaseModel):
    name = Property()
    fullName = Property()

    users = RelatedTo('User', 'CLEN')
    groupType = RelatedTo('GroupType', "PATRI")

    def fetch(self, _id):
        return Group.match(graph, _id).first()

    def fetch_users(self):
        return [{
            **user[0].as_dict(),
            **user[1]
        } for user in self.users._related_objects]

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'fullName': self.fullName
        }


class GroupType(BaseModel):
    name = Property()

    groups = RelatedTo('Group', 'OBSAHUJE')

    def fetch(self, _id):
        return Group.match(graph, _id).first()

    def fetch_groups(self):
        return [{
            **group[0].as_dict(),
            **group[1]
        } for group in self.groups._related_objects]

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name
        }


class Temp(BaseModel):
    name = Property()
    fullName = Property()

    def fetch(self, _id):
        return Temp.match(graph, _id).first()


    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'fullName': self.fullName
        }