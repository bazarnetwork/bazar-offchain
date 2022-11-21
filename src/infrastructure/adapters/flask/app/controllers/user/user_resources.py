# -*- coding: utf-8 -*-
#
# This source code is the confidential, proprietary information of
# Bazar Network S.A.S., you may not disclose such Information,
# and may only use it in accordance with the terms of the license
# agreement you entered into with Bazar Network S.A.S.
#
# 2022: Bazar Network S.A.S.
# All Rights Reserved.
#

import json

import inject
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request

from src.application.user.user_uc import GetUser, GetAllUsers, CreateUser
from src.domain.entities.common_entity import InputPaginationEntity, JwtEntity
from src.domain.entities.user_entity import UserNewEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth

#
# This file contains the user endpoints Api-rest
# @author David Córdoba
#

api = Namespace(name='users', description="User controller", path='/api/v1/users')


@api.route("/")
class UsersResource(Resource):

    # Swagger params pagination
    schema = InputPaginationEntity.schema()
    model = api.schema_model("InputPaginationEntity", schema)

    @inject.autoparams('get_all_users', 'create_user')
    def __init__(self, api: None, get_all_users: GetAllUsers, create_user: CreateUser):
        self.api = api
        self.get_all_users = get_all_users
        self.create_user = create_user

    @api.doc(params=schema['properties'], security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        jwt = dict(request.headers).get('Authorization', None)
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        result = self.get_all_users.execute(limit, offset, jwt)
        return json.loads(result.json()), 200

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        entity = UserNewEntity.parse_obj(request.json)
        result = self.create_user.execute(entity)
        return json.loads(result.json()), 201


@api.route("/<string:user_uuid>")
class UserResource(Resource):

    @inject.autoparams('get_user')
    def __init__(self, api: None, get_user: GetUser):
        self.api = api
        self.get_user = get_user

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, user_uuid, *args, **kwargs):
        result = self.get_user.execute(user_uuid)
        return json.loads(result.json()), 200
