import graphene

import gql.geodata.schema
import gql.metadata.schema
import gql.indicator.schema
import gql.metadata.mutation
import gql.indicator.mutation


class Query(gql.geodata.schema.Query,
            gql.metadata.schema.Query,
            gql.indicator.schema.Query,
            graphene.ObjectType):
    pass


class Mutation(gql.metadata.mutation.Mutation,
               gql.indicator.mutation.Mutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)