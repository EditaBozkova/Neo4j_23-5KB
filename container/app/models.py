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


g_id=0

def get_id():
    global g_id
    g_id=g_id+1
    return str(g_id)


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
    __primarykey__ = 'id'

    id = Property()
    name = Property()
    surname = Property()
    age = Property()
    memberships = RelatedTo('Membership', 'PATRI')

    def fetch(self):
        person = self.match(graph, self.id).first()
        if person is None:
            raise GraphQLError(f'"{self.id}" has not been found in person list.')

        return person

    def deleteNode(self):
        person = self.match(graph, self.id).first()
        Person.delete(person)

    def AddPersontoG(self, idP, idG):
        graph.run("""
            MATCH (a:Person) WHERE a.id="{}"
            MATCH (b:Group) WHERE b.id="{}"
            CREATE r=(b)-[:CLEN]->(a)
        """.format(idP, idG))

    def RemovePersonFG(self, id):
        graph.run("""
            MATCH  (n {id: "{}"})-[r:KNOWS]->()
            DELETE r
        """.format(id))

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
    __primarykey__ = 'id'

    id = Property()
    name = Property()
    groupType = RelatedTo('GroupType', 'CLENEM')
    members = RelatedTo('Person', 'CLEN')

    def fetch(self):
        group = self.match(graph, self.id).first()
        if group is None:
            raise GraphQLError(f'"{self.id}" has not been found in group list.')

        return group

    def deleteNode(self):
        group = self.match(graph, self.id).first()
        Group.delete(group)

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
    __primarykey__ = 'id'

    id = Property()
    name = Property()

    def fetch(self):
        membership = self.match(graph, self.id).first()
        if membership is None:
            raise GraphQLError(f'"{self.id}" has not been found in group Type list.')

        return membership

    def deleteNode(self):
        groupType = self.match(graph, self.id).first()
        GroupType.delete(groupType)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class RoleType(BaseModel):
    __primarykey__ = 'id'

    id = Property()
    name = Property()

    def fetch(self):
        roleType = self.match(graph, self.id).first()
        if roleType is None:
            raise GraphQLError(f'"{self.id}" has not been found in role Type list.')

        return roleType

    def deleteNode(self):
        roleType = self.match(graph, self.id).first()
        RoleType.delete(roleType)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Membership(BaseModel):
    __primarykey__ = 'id'

    id = Property()

    roleType = RelatedTo('RoleType', 'ROLE')
    groups = RelatedTo('Group', 'OBSAHUJE')

    def fetch(self):
        roleType = self.match(graph, self.id).first()
        if roleType is None:
            raise GraphQLError(f'"{self.id}" has not been found in role Type list.')

        return roleType
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

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
        }