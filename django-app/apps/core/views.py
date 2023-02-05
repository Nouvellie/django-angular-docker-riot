import json
import queue

from .utils.riot import Riot
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
from threading import Thread as td

riot = Riot()


class HomePage(TemplateView):

	template_name = 'core/base.html'


class Regions(APIView):

	permission_classes = (AllowAny,)

	def get(self, request, format=None, *args, **kwargs):
		response = riot.regions
		return Response(response, status=HTTP_200_OK)

class CompleteSummonerInfo(APIView):

	permission_classes = (AllowAny,)

	def post(self, request, format=None, *args, **kwargs):

		region = "la2" #request.data.get("region")
		# summoner_name = "ŠzékeŁÿ" #request.data.get("summonerName")
		summoner_name = "beTTERTHANTHAT"
		count = 20

		# # 1.0-1.1
		# summoner_info_queue = queue.Queue()
		# summoner_info_t = td(target=lambda q, arg1, arg2: q.put(riot.summoner_info_by_name(arg1, arg2)), args=(summoner_info_queue, region, summoner_name))
		# summoner_info_t.start()
		# summoner_info_result = summoner_info_queue.get()

		# # 1.0-1.3
		# summoner_extra_info_queue = queue.Queue()
		# summoner_extra_info_t = td(target=lambda q, arg1: q.put(riot.summoner_extra_info(arg1)), args=(summoner_extra_info_queue, summoner_info_result['puuid']))
		# summoner_extra_info_t.start()
		
		# # 1.0-1.2
		# summoner_soloq_info_queue = queue.Queue()
		# summoner_soloq_info_t = td(target=lambda q, arg1, arg2: q.put(riot.summoner_soloq_info(arg1, arg2)), args=(summoner_soloq_info_queue, region, summoner_info_result['id']))
		# summoner_soloq_info_t.start()

		# 2.1-2.3
		# summoner_last_soloq_info_queue = queue.Queue()
		# summoner_last_soloq_info_t = td(target=lambda q, arg1, arg2: q.put(riot.summoner_last_soloq_info(arg1, arg2)), args=(summoner_last_soloq_info_queue, summoner_info_result['puuid'], count))
		# summoner_last_soloq_info_t.start()
		# z = summoner_last_soloq_info_queue.get()

		# summoner_extra_info_result = summoner_extra_info_queue.get()
		# summoner_info_result.update(summoner_extra_info_result)		
		# summoner_soloq_info_result = summoner_soloq_info_queue.get()
		# summoner_info_result.update(summoner_soloq_info_result)
		
		# 1.1-1.2
		soloq_match_detail_queue = queue.Queue()
		soloq_match_detail_t = td(target=lambda q, arg1: q.put(riot.soloq_match_detail(arg1)), args=(soloq_match_detail_queue, "LA2_1265958182"))
		soloq_match_detail_t.start()
		soloq_match_detail_result = soloq_match_detail_queue.get()

		# print(match_detail_result['metadata']['participants'])
		# match_card_queue = queue.Queue()
		# match_card_t = td(target=lambda q, arg1: q.put(riot.match_card(arg1)), args=(soloq_match_detail_queue, match_detail_result))
		# match_card_t.start()

		# x = match_card_queue.get()

		a = riot.match_card(region, soloq_match_detail_result)

		return Response(a, status=HTTP_200_OK)
	

# class Matches(APIView):

# 	permission_classes = (AllowAny,)

# 	def get(self, request, format=None, *args, **kwargs):

