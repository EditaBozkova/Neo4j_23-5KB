from typing_extensions import Required
from urllib import request
import graphene

from .models import Person, Group, GroupType, RoleType, Membership


#
# Uzivatel
#
class PersonSchema(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()
    age = graphene.String()
    memberships = graphene.List(lambda: MembershipSchema)

    # name = graphene.String()
    # surname = graphene.String()
    # age = graphene.Int()
    # email = graphene.String()

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.person = Person(email=self.email).fetch()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.person = Person(id=self.id).fetch()

    def resolve_membreships(self, info):
        return [MembershipSchema(**membreship) for membreship in Membership().fetch(self._id).fetch_memberships()]    
    

class PersonInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        surname = graphene.String(required=True)
        age = graphene.Int(required=True)

    success = graphene.Boolean()
    person = graphene.Field(lambda: PersonSchema)

    def mutate(self, info, **kwargs):
        person = Person(**kwargs)
        person.save()

        return CreatePerson(person=person, success=True)


class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        surname = graphene.String()
        age = graphene.Int()

    success = graphene.Boolean()
    person = graphene.Field(lambda: PersonSchema)

    def mutate(self, info, name, surname, age):
        person = Person()
        person = Person(id=self.id).fetch()
        person.update(id=self.id, name=name, surname=surname, age=age)

        return UpdatePerson(person=person, success=True)


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)

    success = graphene.Boolean()

    def mutate(self, info, **kwargs):
        person = Person(**kwargs)
        person = Person(id=self.id).fetch()
        person.delete(id=self.id)

        return DeletePerson(success=True)


#
# Skupina
#
class GroupSchema(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    groupType = graphene.List(lambda: GroupTypeSchema)
    members = graphene.List(lambda: PersonSchema)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group = Group(id=self.id).fetch()

    def resolve_groupTypes(self, info):
        return [GroupTypeSchema(**grouptype) for grouptype in Group().fetch(id=self.id).fetch_groupTypes()]

    def resolve_persons(self, info):
        return [PersonSchema(**person) for person in Group().fetch(id=self.id).fetch_persons()]


class GroupInput(graphene.InputObjectType):
    name = graphene.String(required=True)


#
# Skupina typ
#
class GroupTypeSchema(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.groupType = GroupType(id=self.id).fetch()


class GroupTypeInput(graphene.InputObjectType):
    name = graphene.String(required=True)


#
# RoleType
#
class RoleTypeSchema(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.roleType = RoleType(id=self.id).fetch()


#
# Membership
#
class MembershipSchema(graphene.ObjectType):
    roleType = graphene.List(lambda: RoleType)
    groups = graphene.List(lambda: GroupSchema)

    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id')
        super().__init__(**kwargs)

    def resolve_groups(self, info):
        return [GroupSchema(**group) for group in Membership().fetch(id=self.id).fetch_groups()]

    def resolve_roleTypes(self, info):
        return [RoleTypeSchema(**roletype) for roletype in RoleType().fetch(id=self.id).fetch_roles()]


#
# Queries
#
class Query(graphene.ObjectType):
    # getPerson = graphene.Field(lambda: PersonSchema, id=graphene.String())
    person = graphene.List(lambda: PersonSchema)
    group = graphene.List(lambda: GroupSchema)
    groupType = graphene.List(lambda: GroupTypeSchema)
    roleType = graphene.List(lambda: RoleTypeSchema)

    # def resolve_person(self, info, id):
    #     getPerson = Person(id=id).fetch()
    #     return PersonSchema(**getPerson.as_dict())

    def resolve_persons(self, info):
        return [PersonSchema(**person.as_dict()) for person in Person().all]

    def resolve_group(self, info):
        return [GroupSchema(**group.as_dict()) for group in Group().all]

    def resolve_groupType(self, info):
        return [GroupTypeSchema(**groupType.as_dict()) for groupType in GroupType().all]

    def resolve_roleType(self, info):
        return [RoleTypeSchema(**roleType.as_dict()) for roleType in RoleType().all]


class Mutations(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    remove_person = DeletePerson.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)