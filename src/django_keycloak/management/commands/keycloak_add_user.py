from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from django_keycloak.models import Realm

import django_keycloak.services.users

logger = logging.getLogger(__name__)


def realm(name):
    try:
        return Realm.objects.get(name=name)
    except Realm.DoesNotExist:
        raise TypeError("Realm does not exist")


def get_username_field() -> str:
    UserModel = get_user_model()
    if hasattr(UserModel, "USERNAME_FIELDS"):
        return UserModel.USERNAME_FIELDS
    return "username"


def user(username):
    UserModel = get_user_model()
    filter_qs = {get_username_field(): username}
    try:
        return UserModel.objects.get(**filter_qs)
    except UserModel.DoesNotExist:
        raise TypeError("User does not exist")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--realm", type=realm, required=True)
        parser.add_argument("--user", type=user, required=True)

    def handle(self, *args, **options):
        user = options["user"]
        realm = options["realm"]

        django_keycloak.services.users.add_user(client=realm.client, user=user)
