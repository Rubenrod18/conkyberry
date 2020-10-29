import graphene
from bson import ObjectId
from graphene_mongo import MongoengineObjectType

from .models import (Resource as ResourceModel,
                     ResourceData as ResourceDataModel,
                     ResourceGraph as ResourceGraphModel,
                     ResourceField as ResourceFieldModel)


class CustomNode(graphene.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return id


class ResourceGraph(MongoengineObjectType):
    class Meta:
        model = ResourceGraphModel
        interfaces = (CustomNode,)


class ResourceField(MongoengineObjectType):
    class Meta:
        model = ResourceFieldModel
        interfaces = (CustomNode,)


class ResourceData(MongoengineObjectType):
    class Meta:
        model = ResourceDataModel
        interfaces = (CustomNode,)


class Resource(MongoengineObjectType):
    class Meta:
        model = ResourceModel
        interfaces = (CustomNode,)


class Query(graphene.ObjectType):
    node = CustomNode.Field()
    all_resources = graphene.List(Resource)
    resource = graphene.Field(Resource, id=graphene.ID())

    def resolve_all_resources(self, info):
        return ResourceModel.objects.all()

    def resolve_resource(self, info, id: str):
        return ResourceModel.objects(id=ObjectId(id)).get()


schema = graphene.Schema(query=Query, types=[Resource, ResourceData,
                                             ResourceGraph, ResourceField])
