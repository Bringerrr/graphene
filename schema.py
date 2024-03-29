import graphene
import json
import uuid
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resolve_users(self, info, limit=None):
        return[
            User(id="1", username="Fred", created_at=datetime.now()),
            User(id="2", username="Tyler", created_at=datetime.now()),
        ][:limit]


class CreateUser(graphene.Mutation):

    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)


class Mutation (graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
 mutation{
    createUser(username: "Jeff"){
        user{
            id
            username
            createdAt
        }
    }
 }
'''
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))
