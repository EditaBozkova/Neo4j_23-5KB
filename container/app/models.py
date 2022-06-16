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

    def update(self):
        graph.update(self)

    def delete(self):
        graph.delete(self)


class Person(BaseModel):
    id = Property()
    name = Property()
    surname = Property()
    age = Property()
    memberships = RelatedTo('Membership', 'PATRI')

    def fetch(self):
        return Person.match(graph, self.id).first()

    def fetch_memberships(self):
        return [{
            **membership[0].as_dict(),
            **membership[1]
        } for membership in self.memberships._related_objects]

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'age': self.age
        }


class Group(BaseModel):
    id = Property()
    name = Property()
    groupType = RelatedTo('GroupType', "PATRI")
    members = RelatedTo('Person', 'CLEN')

    def fetch(self):
        return Group.match(graph, self.id).first()

    def fetch_members(self):
        return [{
            **member[0].as_dict(),
            **member[1]
        } for member in self.members._related_objects]

    def fetch_groupTypes(self):
        return [{
            **groupTyp[0].as_dict(),
            **groupTyp[1]
        } for groupTyp in self.groupType._related_objects] 

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class GroupType(BaseModel):
    id = Property()
    name = Property()

    def fetch(self):
        return GroupType.match(graph, self.id).first()

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class RoleType(BaseModel):
    id = Property()
    name = Property()

    def fetch(self):
        return RoleType.match(graph, self.id).first()

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Membership(BaseModel):
    roleType = RelatedTo('RoleType', 'ROLE')
    groups = RelatedTo('Group', 'OBSAHUJE')

    def fetch(self, _id):
        return Membership.match(graph, _id).first()

    def fetch_roles(self):
        return [{
            **role[0].as_dict(),
            **role[1]
        } for role in self.roleType._related_objects]
        
    def fetch_groups(self):
        return [{
            **group[0].as_dict(),
            **group[1]
        } for group in self.groups._related_objects]