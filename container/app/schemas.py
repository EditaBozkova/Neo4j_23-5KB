from typing_extensions import Required
import graphene

from .models import User, Group, GroupType


#
# Uzivatel
#
class UserSchema(graphene.ObjectType):
    name = graphene.String()
    surname = graphene.String()
    age = graphene.Int()
    email = graphene.String()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = User(email=self.email).fetch()


class UserInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        surname = graphene.String(required=True)
        age = graphene.Int(required=True)
        email = graphene.String(required=True)

    success = graphene.Boolean()
    user = graphene.Field(lambda: UserSchema)

    def mutate(self, info, **kwargs):
        user = User(**kwargs)
        user.save()

        return CreateUser(user=user, success=True)


#
# Skupina
#
class GroupSchema(graphene.ObjectType):
    name = graphene.String()
    fullName = graphene.String()
    users = graphene.List(UserSchema)
    groupType = graphene.Field(lambda: GroupTypeSchema)


    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id')
        super().__init__(**kwargs)

    def resolve_users(self, info):
        return [UserSchema(**user) for user in Group().fetch(self._id).fetch_users()]


class GroupInput(graphene.InputObjectType):
    name = graphene.String(required=True)


#
# Skupina typ
#
class GroupTypeSchema(graphene.ObjectType):
    name = graphene.String()
    groups = graphene.List(lambda: GroupSchema)

    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id')
        super().__init__(**kwargs)

    def resolve_groups(self, info):
        return [GroupSchema(**group) for group in GroupType().fetch(self._id).fetch_groups()]


class GroupTypeInput(graphene.InputObjectType):
    name = graphene.String(required=True)


#
# Queries
#
class Query(graphene.ObjectType):
    getUser = graphene.Field(lambda: UserSchema, email=graphene.String())
    user = graphene.List(lambda: UserSchema)
    group = graphene.List(lambda: GroupSchema)
    groupType = graphene.List(lambda: GroupTypeSchema)

    def resolve_user(self, info, email):
        getUser = User(email=email).fetch()
        return UserSchema(**getUser.as_dict())

    def resolve_user(self, info):
        return [UserSchema(**user.as_dict()) for user in User().all]

    def resolve_group(self, info):
        return [GroupSchema(**group.as_dict()) for group in Group().all]

    def resolve_groupType(self, info):
        return [GroupTypeSchema(**groupType.as_dict()) for groupType in GroupType().all]


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)