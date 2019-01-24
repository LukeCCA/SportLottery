import requests
import numpy as np
import pandas as pd
import json
from datetime import datetime
import time

__version__ = '1.1'


class NbaStatApi(object):

    def __init__(self, numOfTeam=30, numOfGames=83):
        self.HEADERS = {
            'user-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),
            'Dnt': ('1'),
            'Accept-Encoding': ('gzip, deflate'),
            'Accept-Language': ('en'),
            'origin': ('http://stats.nba.com')
            }
        self.numOfTeam = numOfTeam
        self.numOfGames = numOfGames
        self.totalGames = (numOfTeam * numOfGames)//2


    def leaguegamefinder(self, start, end, playerOrTeam, location, save_pickle_file_dir,SeasonType='Regular Season'):
        # query by season

        nbaStat = []
        seasons = [i for i in range(start, end+1)]
        url = "http://stats.nba.com/stats/leaguegamefinder"
        for year in seasons:
            season = str(year-1)+"-"+str(year)[2:]
            querystring = {"playerOrTeam":playerOrTeam, # T / P
            "season":season,
            "leagueId":'00',
            'SeasonType':SeasonType, # Playoffs / Regular Season
            "location":location} # A / H
            response = requests.request("GET", url, params=querystring,headers=self.HEADERS)
            data = json.loads(response.content)['resultSets'][0]['rowSet']
            nbaStat += data
            print('Finish ' + season + ' season!!')
            print('Number of data: ' + str(len(data)))
        
        df = pd.DataFrame(nbaStat,columns=json.loads(response.content)['resultSets'][0]['headers']).sort_values(['GAME_ID']).reset_index(drop=True)
        df.to_pickle(save_pickle_file_dir)

        return df

    def teamgamelog(self, start, end, save_pickle_file_dir, SeasonType='Regular Season'):
        # query by season

        url = "http://stats.nba.com/stats/teamgamelog"
        seasons = [i for i in range(start, end+1)]
        teams = json.loads(open('/Users/chienan/Pycon/github/SportLottery/nbastat/teamId_mpt').read())
        output = {}
        for teamname, team in zip(teams.values(),teams.keys()):
            teamStat = []
            for year in seasons:
                season = str(year-1)+"-"+str(year)[2:]
                print(season)
                querystring = {"teamId":team,
                            "season":season,
                            'SeasonType':SeasonType,
                            "leagueId":'00'
                            }
                try:
                    response = requests.request("GET", url, params=querystring,headers=self.HEADERS)

                except:
                    print("timeout, wait for 20 seconds..."%())
                    time.sleep(20)
                    response = requests.request("GET", url, params=querystring,headers=self.HEADERS)

                try:
                    teamStat += json.loads(response.content)['resultSets'][0]['rowSet']
                except:
                    print(response.content)
            output[str(team)] = pd.DataFrame(teamStat,columns=json.loads(response.content)['resultSets'][0]['headers']).sort_values(['Game_ID']).reset_index(drop=True)
            print(teamname + " parse finish...")

        df = pd.DataFrame()
        for key in list(output.keys()):
            df = pd.concat([df,output[key]],axis=0).reset_index(drop=True)
        df.to_pickle(save_pickle_file_dir)

        return df


    '''''''''
    BoxScoreAdvance
        Var:
            "GAME_ID","TEAM_ID","TEAM_ABBREVIATION","TEAM_CITY","PLAYER_ID","PLAYER_NAME",
            "START_POSITION","COMMENT","MIN","OFF_RATING","DEF_RATING","NET_RATING","AST_PCT",
            "AST_TOV","AST_RATIO","OREB_PCT","DREB_PCT","REB_PCT",
            "TM_TOV_PCT","EFG_PCT","TS_PCT","USG_PCT","PACE","PIE"
    
    '''''''''


    def boxscoreadvanced(self, start_year, end_year, start_gameid, end_gameid, save_team_pickle_file_dir, save_player_pickle_file_dir):
        # query by game id

        url = "http://stats.nba.com/stats/boxscoreadvancedv2/"
        # years = [str(i) for i in range(start_year, end_year+1)]
        seasons = [int('2' + str(i)[2:] + '00000') for i in range(start_year-1, end_year)]
        
        playerData = []
        teamData = []
        for season in seasons:
            gameIds = np.array([i for i in range(season + 1, season+self.totalGames+1)])
            gameIds = gameIds[(gameIds>start_gameid)&(gameIds<=end_gameid)]

            for gameId in gameIds:
                querystring = {"gameId": '00'+str(gameId),"startPeriod":"0","endPeriod":"14",
                "startRange":"0","endRange":"2147483647","rangeType":"0"}
                response = requests.request("GET", url, params=querystring,headers=self.HEADERS)
                times = 0

                while response.status_code != 200:
                    response = requests.request("GET", url, params=querystring,headers=self.HEADERS)
                    times += 1
                    if times > 3:
                        print("error in gameid: " + str(gameId))
                        break
                    print("time:",times)
                try:
                    response = json.loads(response.content)               
                    playerData += response['resultSets'][0]['rowSet']
                    teamData += response['resultSets'][1]['rowSet']
                    
                    playerCol = response['resultSets'][0]['headers']
                    teamCol = response['resultSets'][1]['headers']
                    print('finish '+str(gameId))
                except:
                    print(response)
                    break
        team_df = pd.DataFrame(teamData,columns=teamCol)
        player_df = pd.DataFrame(playerData,columns=playerCol)

        team_df.to_pickle(save_team_pickle_file_dir)
        player_df.to_pickle(save_player_pickle_file_dir)

        return player_df, team_df

    '''''''''
    Game Track
        Var:
            "DIST","ORBC","DRBC","RBC","TCHS","SAST","FTAST","PASS",
            "AST","CFGM","CFGA","CFG_PCT","UFGM","UFGA","UFG_PCT","FG_PCT",
            "DFGM","DFGA","DFG_PCT"
    '''''''''


    # def boxscoreplayertrack(self, start, end, save_team_pickle_file_dir, save_player_pickle_file_dir):
    #     # query by game id

    #     url = "http://stats.nba.com/stats/boxscoreplayertrackv2/"
    #     # years = [str(i) for i in range(start, end+1)]
    #     seasons =  [int('2' + str(i)[2:] + '00000') for i in range(start-1, end)]
    #     playerData = []
    #     teamData = []
    #     for season in seasons:

    #         for gameId in [i for i in range(season + 1, season+self.totalGames+1)]:
    #             querystring = {"gameId": '00'+str(gameId) }
    #             response = requests.request("GET", url, params=querystring,headers=self.HEADERS)
    #             times = 0

    #             while response.status_code != 200:
    #                 response = requests.request("GET", url, params=querystring,headers=self.HEADERS)
    #                 times += 1
    #                 if times > 5:
    #                     print("error in gameid: " + str(gameId))
    #                     response = requests.request("GET", url, 
    #                     params={"gameId": '00'+str(gameId-1),"startPeriod":"0","endPeriod":"14",
    #                     "startRange":"0","endRange":"2147483647","rangeType":"0"},
    #                     headers=self.HEADERS)
    #                     break

    #             response = json.loads(response.content)               
    #             playerData += response['resultSets'][0]['rowSet']
    #             teamData += response['resultSets'][1]['rowSet']
    #             print('finish '+str(gameId))

    #     team_df = pd.DataFrame(teamData,columns=response['resultSets'][1]['headers'])
    #     player_df = pd.DataFrame(playerData,columns=response['resultSets'][0]['headers'])

    #     team_df.to_pickle(save_team_pickle_file_dir)
    #     player_df.to_pickle(save_player_pickle_file_dir)

    #     return player_df, team_df     

        


