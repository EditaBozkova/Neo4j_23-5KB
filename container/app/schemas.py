from sre_constants import SUCCESS
import graphene

from .models import get_id, Person, Group, GroupType, Membership, RoleType


#
# Uzivatel
#
class PersonSchema(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    surname = graphene.String()
    age = graphene.String()
    memberships = graphene.List(lambda: MembershipSchema)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.person = Person(id=self.id).fetch()

    def resolve_memberships(self, info):
        return [MembershipSchema(**membership) for membership in Person(id=self.id).fetch().fetch_memberships()]



class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        surname = graphene.String(required=True)
        age = graphene.Int(required=True)

    success = graphene.Boolean()
    person = graphene.Field(lambda: PersonSchema)

    def mutate(self, info, name, surname, age):
        person = Person(
            id=get_id(),
            name=name,
            surname=surname,
            age=age)
        person.save()

        return CreatePerson(person=person, success=True)


class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()
        surname = graphene.String()
        age = graphene.Int()

    success = graphene.Boolean()
    person = graphene.Field(lambda: PersonSchema)

    def mutate(self, info, id, name=None, surname=None, age=None):
        person = Person(id=id).fetch()
        if(type(name) == str): person.name = name
        if(type(surname) == str): person.surname = surname
        if(type(age) == str): person.age = age
        person.save()

        return UpdatePerson(person=person, success=True)


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.String(required = True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        person = Person(id=id).deleteNode()

        return DeletePerson(success=True)


#
# Skupina
#
class GroupSchema(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    groupType = graphene.List(lambda: GroupTypeSchema)
    members = graphene.List(lambda: PersonSchema)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group = Group(id=self.id).fetch()

    def resolve_groupTypes(self, info):
        return [GroupTypeSchema(**gType.as_dict) for gType in self.group.groupType]

    def resolve_members(self, info):
        return [PersonSchema(**person) for person in Group(id=self.id).fetch().fetch_members()]


class CreateGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        groupTypeID = graphene.String()

    success = graphene.Boolean()
    group = graphene.Field(lambda: GroupSchema)

    def mutate(self, info, name, groupTypeID):
        group = Group(
            id=get_id(),
            name=name,
            groupType=groupTypeID)
        group.save()

        return CreateGroup(group=group, success=True)


class UpdateGroup(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()

    success = graphene.Boolean()
    group = graphene.Field(lambda: GroupSchema)

    def mutate(self, info, id, name=None):
        group = Group(id=id).fetch()
        if(type(name) == str): group.name = name
        group.save()

        return UpdateGroup(group=group, success=True)


class DeleteGroup(graphene.Mutation):
    class Arguments:
        id = graphene.String(required = True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        group = Group(id=id).deleteNode()

        return DeleteGroup(success=True)



#
# Skupina typ
#
class GroupTypeSchema(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Type = GroupType(id=self.id).fetch()


class CreateGroupType(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    success = graphene.Boolean()
    groupType = graphene.Field(lambda: GroupSchema)

    def mutate(self, info, name):
        groupType = GroupType(
            id=get_id(),
            name=name)
        groupType.save()

        return CreateGroupType(groupType=groupType, success=True)


class UpdateGroupType(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()

    success = graphene.Boolean()
    groupType = graphene.Field(lambda: GroupTypeSchema)

    def mutate(self, info, id, name=None):
        groupType = GroupType(id=id).fetch()
        if(type(name) == str): groupType.name = name
        groupType.save()

        return UpdateGroupType(groupType=groupType, success=True)


class DeleteGroupType(graphene.Mutation):
    class Arguments:
        id = graphene.String(required = True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        groupType = GroupType(id=id).deleteNode()

        return DeleteGroupType(success=True)


#
# RoleType
#
class RoleTypeSchema(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.roleType = RoleType(id=self.id).fetch()


class CreateRoleType(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    success = graphene.Boolean()
    roleType = graphene.Field(lambda: RoleTypeSchema)

    def mutate(self, info, name):
        roleType = RoleType(
            id=get_id(),
            name=name)
        roleType.save()

        return CreateRoleType(roleType=roleType, success=True)


class UpdateRoleType(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()

    success = graphene.Boolean()
    roleType = graphene.Field(lambda: RoleTypeSchema)

    def mutate(self, info, id, name=None):
        roleType = RoleType(id=id).fetch()
        if(type(name) == str): roleType.name = name
        roleType.save()

        return UpdateRoleType(roleType=roleType, success=True)


class DeleteRoleType(graphene.Mutation):
    class Arguments:
        id = graphene.String(required = True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        roleType = RoleType(id=id).deleteNode()

        return DeleteRoleType(success=True)


#
# Memberships
#
class MembershipSchema(graphene.ObjectType):
    id = graphene.String()
    roleType = graphene.List(lambda: RoleTypeSchema)
    groups = graphene.List(lambda: GroupSchema)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.membership = Membership(id=self.id).fetch()

    def resolve_groups(self, info):
        return [GroupSchema(**group) for group in Membership().fetch(id=self.id).fetch_groups()]

    def resolve_roleTypes(self, info):
        return [RoleTypeSchema(**roletype) for roletype in RoleType().fetch(id=self.id).fetch_roles()]


#
# Queries
#
class Query(graphene.ObjectType):
    person = graphene.Field(lambda: PersonSchema, id = graphene.String())
    group = graphene.Field(lambda: GroupSchema, id = graphene.String())
    groupType = graphene.Field(lambda: GroupTypeSchema, id = graphene.String())
    roleType = graphene.Field(lambda: RoleTypeSchema, id = graphene.String())

    def resolve_person(self, info, id):
        person = Person(id=id).fetch()
        return PersonSchema(**person.as_dict())

    def resolve_group(self, info, id):
        group = Group(id=id).fetch()
        return GroupSchema(**group.as_dict())
        #return [GroupSchema(**group.as_dict()) for group in Group().all]

    def resolve_groupType(self, info, id):
        groupType = GroupType(id=id).fetch()
        return GroupTypeSchema(**groupType.as_dict())

    def resolve_roleType(self, info, id):
        roleType = RoleType(id=id).fetch()
        return RoleTypeSchema(**roleType.as_dict())

#
# Mutations
#
class AddUserToGroup(graphene.Mutation):
    class Arguments:
        idP = graphene.String(required=True)
        idG = graphene.String(required=True)

    success = graphene.Boolean()
    person = graphene.Field(lambda: PersonSchema)
    group = graphene.Field(lambda: GroupSchema)

    def mutate(self, info, idP, idG):
        person = Person(id=idP).fetch()
        group = Group(id=idG).fetch()
        person = Person().AddPersontoG(idP, idG)

        return AddUserToGroup(success=True)


class RemoveUserFromGroup(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        person = Person().RemovePersonFG(id)

        return RemoveUserFromGroup(success=True)


class Mutations(graphene.ObjectType):
    createPerson = CreatePerson.Field()
    updatePerson = UpdatePerson.Field()
    delPerson = DeletePerson.Field()

    createGroup = CreateGroup.Field()
    updateGroup = UpdateGroup.Field()
    delGroup = DeleteGroup.Field()

    createGroupType = CreateGroup.Field()
    updateGroupType = UpdateGroup.Field()
    delGroupType = DeleteGroup.Field()

    createRoleType = CreateRoleType.Field()
    updateRoleType = UpdateRoleType.Field()
    delRoleType = DeleteRoleType.Field()

    add_user_to_group = AddUserToGroup.Field()
    remove_user_from_group = RemoveUserFromGroup.Field()


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)