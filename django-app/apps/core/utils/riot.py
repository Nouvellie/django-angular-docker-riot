import json
import queue
import requests

from abc import (
    ABC,
    abstractclassmethod,
)
from main.settings import MEDIA_ROOT, RIOT
from threading import Thread as td
from typing import (
    Generic,
    TypeVar,
)
SELFCLASS = TypeVar('SELFCLASS')

class Riot(ABC):

    def __new__(cls, *args, **kwargs,) -> Generic[SELFCLASS]:
        return super(Riot, cls).__new__(cls, *args, **kwargs)

    def __init__(self,) -> None:
        self.regions = self.read_regions()
        self.match_5vs5 = self.read_match_5vs5()
        self.player = self.read_player()
        self.api_key = RIOT

    def read_regions(self,) -> json:
        file_path = f"{MEDIA_ROOT}/regions.json"
        with open(str(file_path), "r", encoding="utf8") as regions_template:
            regions_data = json.load(regions_template)
        return regions_data.get("regions")

    def read_match_5vs5(self,) -> json:
        file_path = f"{MEDIA_ROOT}/match_5vs5.json"
        with open(str(file_path), "r", encoding="utf8") as match_template:
            match_5vs5_data = json.load(match_template)
        return match_5vs5_data.get("match_5vs5")
    
    def read_player(self,) -> json:
        file_path = f"{MEDIA_ROOT}/player.json"
        with open(str(file_path), "r", encoding="utf8") as player_template:
            player_data = json.load(player_template)
        return player_data.get("player")
    
    def summoner_info_by_name(self, region, summoner_name) -> json:
        summoner_info_by_name_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={self.api_key}"
        # print("1", type(requests.get(summoner_info_by_name_url).json()))
        return requests.get(summoner_info_by_name_url).json()
    
    def summoner_info_by_puuid(self, region, match_detail, position, side) -> json:
        puuid = match_detail['metadata']['participants'][position]
        summoner_info_by_puuid_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.api_key}"
        summoner_info_by_puuid_result = requests.get(summoner_info_by_puuid_url).json()
        
        summoner_soloq_info_result = self.summoner_soloq_info(region, summoner_info_by_puuid_result['id'])
        
        try:
            mmr = f"{summoner_soloq_info_result['tier'].capitalize()} {summoner_soloq_info_result['rank']} {summoner_soloq_info_result['leaguePoints']}"
        except:
            import re, traceback
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())
            print(full_traceback)
            mmr = "Unranked"
        print("$$$$$$$$$$$$$$$$$$$$", position, match_detail['info']['participants'][position])
        player_card = {}
        player_card.update({
            "name": summoner_info_by_puuid_result['name'].strip(),
            "mmr": mmr,
            "side": side,
            "pinkPlaced": match_detail['info']['participants'][position]['challenges']['controlWardsPlaced'],
            "soloKills": match_detail['info']['participants'][position]['challenges']['soloKills'],
            "kills": match_detail['info']['participants'][position]['kills'],
            "deaths": match_detail['info']['participants'][position]['challenges']['deathsByEnemyChamps'],
            "assists": match_detail['info']['participants'][position]['assists'],
            "kda": match_detail['info']['participants'][position]['challenges']['kda'],
            "cs10": match_detail['info']['participants'][position]['challenges']['laneMinionsFirst10Minutes'],
            "cs": match_detail['info']['participants'][position]['neutralMinionsKilled'] + match_detail['info']['participants'][position]['totalMinionsKilled'],
            "kp": int(round(match_detail['info']['participants'][position]['challenges']['killParticipation']*100, 0)),
            "perfectGame": match_detail['info']['participants'][position]['challenges']['perfectGame'],
            "champLevel": match_detail['info']['participants'][position]['champLevel'],
            "championName": match_detail['info']['participants'][position]['championName'],
            "championId": match_detail['info']['participants'][position]['championId'],
            "fbAssist": match_detail['info']['participants'][position]['firstBloodAssist'],
            "fbKill": match_detail['info']['participants'][position]['firstBloodKill'],
            "item0": match_detail['info']['participants'][position]['item0'],
            "item1": match_detail['info']['participants'][position]['item1'],
            "item2": match_detail['info']['participants'][position]['item2'],
            "item3": match_detail['info']['participants'][position]['item3'],
            "item4": match_detail['info']['participants'][position]['item4'],
            "item5": match_detail['info']['participants'][position]['item5'],
            "item6": match_detail['info']['participants'][position]['item6'],
            "damageToChampion": match_detail['info']['participants'][position]['totalDamageDealtToChampions'],
            "damageTaken": match_detail['info']['participants'][position]['totalDamageTaken'],
            "visionScore": match_detail['info']['participants'][position]['visionScore'],
            "wardsKilled": match_detail['info']['participants'][position]['wardsKilled'],
            "wardsPlaced": match_detail['info']['participants'][position]['wardsPlaced'],
            "win": match_detail['info']['participants'][position]['win'],
            "spells1": match_detail['info']['participants'][position]['spell1Casts'],
            "spells2": match_detail['info']['participants'][position]['spell2Casts'],
            "spells3": match_detail['info']['participants'][position]['spell3Casts'],
            "spells4": match_detail['info']['participants'][position]['spell4Casts'],
            "s1c": match_detail['info']['participants'][position]['summoner1Id'],
            "s2c": match_detail['info']['participants'][position]['summoner2Id'],
        })
        # print(player_card)
        return player_card
    
    def summoner_extra_info(self, puuid,) -> json:
        summoner_extra_info_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={self.api_key}"
        return requests.get(summoner_extra_info_url).json()

    def summoner_soloq_info(self, region, id) -> json:
        summoner_soloq_info_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={self.api_key}"
        summoner_soloq_info_result =  requests.get(summoner_soloq_info_url).json()
    
        if len(summoner_soloq_info_result) == 0:
            return {'placement': True}
        else:
            summoner_soloq_info_result[0].update({
                'placement': False, 
                'winRate': f"{int(round(summoner_soloq_info_result[0]['wins']*100/(summoner_soloq_info_result[0]['wins']+summoner_soloq_info_result[0]['losses']),0))}%"
            })
            return summoner_soloq_info_result[0]
        
    def summoner_last_soloq_info(self, puuid, count,) -> json:
        last_soloq_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={count}&api_key={self.api_key}"
        return requests.get(last_soloq_url).json()
    
    def soloq_match_detail(self, match_id,) -> json:
        soloq_match_detail_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.api_key}"
        return requests.get(soloq_match_detail_url).json()
    
    def match_card(self, region, match_detail_result,) -> json:
        # print(match_detail_result['metadata']['participants'])
        summoner_one_queue = queue.Queue()
        summoner_one_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_one_queue, region, match_detail_result, 0,"blue"))
        summoner_one_t.start()
        
        summoner_two_queue = queue.Queue()
        summoner_two_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_two_queue, region, match_detail_result, 1, "blue"))
        summoner_two_t.start()

        summoner_three_queue = queue.Queue()
        summoner_three_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_three_queue, region, match_detail_result, 2, "blue"))
        summoner_three_t.start()

        summoner_four_queue = queue.Queue()
        summoner_four_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_four_queue, region, match_detail_result, 3, "blue"))
        summoner_four_t.start()

        summoner_five_queue = queue.Queue()
        summoner_five_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_five_queue, region, match_detail_result, 4, "blue"))
        summoner_five_t.start()

        summoner_six_queue = queue.Queue()
        summoner_six_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_six_queue, region, match_detail_result, 5, "red"))
        summoner_six_t.start()

        summoner_seven_queue = queue.Queue()
        summoner_seven_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_seven_queue, region, match_detail_result, 6,  "red"))
        summoner_seven_t.start()

        summoner_eight_queue = queue.Queue()
        summoner_eight_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_eight_queue, region, match_detail_result, 7, "red"))
        summoner_eight_t.start()

        summoner_nine_queue = queue.Queue()
        summoner_nine_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_nine_queue, region, match_detail_result, 8, "red"))
        summoner_nine_t.start()

        summoner_ten_queue = queue.Queue()
        summoner_ten_t = td(target=lambda q, arg1, arg2, arg3, arg4: q.put(self.summoner_info_by_puuid(arg1, arg2, arg3, arg4)), args=(summoner_ten_queue, region, match_detail_result, 9, "red"))
        summoner_ten_t.start()
            
        self.match_5vs5['one'] = summoner_one_queue.get()
        self.match_5vs5['two'] = summoner_two_queue.get()
        self.match_5vs5['three'] = summoner_three_queue.get()
        self.match_5vs5['four'] = summoner_four_queue.get()
        self.match_5vs5['five'] = summoner_five_queue.get()
        self.match_5vs5['six'] = summoner_six_queue.get()
        self.match_5vs5['seven'] = summoner_seven_queue.get()
        self.match_5vs5['eight'] = summoner_eight_queue.get()
        self.match_5vs5['nine'] = summoner_nine_queue.get()
        self.match_5vs5['ten'] = summoner_ten_queue.get()
        self.match_5vs5['gameDuration'] = f"{match_detail_result['info']['gameDuration']//60}m {match_detail_result['info']['gameDuration']%60}s"
        self.match_5vs5['gameCreation'] = match_detail_result['info']['gameCreation'] #1675540127921 change to date
        try:
            self.match_5vs5['bans'] = [
                match_detail_result['info']['teams'][0]['bans'][0]['championId'], 
                match_detail_result['info']['teams'][0]['bans'][1]['championId'],
                match_detail_result['info']['teams'][0]['bans'][2]['championId'],
                match_detail_result['info']['teams'][0]['bans'][3]['championId'],
                match_detail_result['info']['teams'][0]['bans'][4]['championId'],
                match_detail_result['info']['teams'][1]['bans'][0]['championId'], 
                match_detail_result['info']['teams'][1]['bans'][1]['championId'],
                match_detail_result['info']['teams'][1]['bans'][2]['championId'],
                match_detail_result['info']['teams'][1]['bans'][3]['championId'],
                match_detail_result['info']['teams'][1]['bans'][4]['championId'],
            ]
        except:
            self.match_5vs5['bans'] = []
        return self.match_5vs5
