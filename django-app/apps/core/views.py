from datetime import datetime, timezone
from django.shortcuts import render
from django.views.generic import TemplateView
from extra.info import info
from main.settings import DEBUG, MEDIA_ROOT
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
	HTTP_200_OK,
	HTTP_204_NO_CONTENT,
	HTTP_400_BAD_REQUEST,
	HTTP_401_UNAUTHORIZED,
	HTTP_404_NOT_FOUND,
	HTTP_426_UPGRADE_REQUIRED,
)
from rest_framework.views import APIView


class HomePage(TemplateView):

	template_name = 'core/base.html'