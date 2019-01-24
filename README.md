# Python實作玩運彩


```
📁 input：本次所有使用到的資料集。
📁 nbastat：用來抓取、整理本次所有資料的套件。
📁 model：放訓練完的模型。
```
## 套件介紹
### NBA STAT資料
```python
from nbastat import nbastatapi

# 呼叫class,並輸入球隊數及一季比賽數目（預設30隊，83場比賽）
nbastat = nbastatapi.NbaStatApi(numOfTeam=30, numOfGames=83)

# 抓取球隊或球員傳統LOG資料
nbastat.leaguegamefinder(start, end, playerOrTeam, location, save_pickle_file_dir, SeasonType)
# start & end 時間 e.g.: 2012
# playerOrTeam 抓取球員還是球隊資訊 T/P
# location 主客場 A/H
# SeasonType 賽事類型 Regular Season（預設）/Playoffs
# save_pickle_file_dir 產出資料路徑


# By球隊抓取LOG資訊
nbastat.teamgamelog(start, end, save_pickle_file_dir, SeasonType)
# start & end 時間 ex: 2012
# SeasonType 賽事類型 Regular Season（預設）/Playoffs
# save_pickle_file_dir 產出資料路徑


# 進階boxscore數據
nbastat.boxscoreadvanced(start_year, end_year, start_gameid, end_gameid, save_team_pickle_file_dir, save_player_pickle_file_dir)
# start_year & end_year 時間 ex: 2012
# start_gameid & end_gameid 起始 gameid，結束 gameid
# save_team_pickle_file_dir 球隊資料產出路徑
# save_player_pickle_file_dir 球員資料產出路徑
          
```

### 玩運彩頁面
```
使用 lottery_crawer.ipynb 進行
```

### FEATURE ENGINERING
```
1. 使用 api_data_collect.ipynb 來抓取raw data
2. 使用 feature_engineering_aggregate.ipynb/feature_engineering_rawdata.ipynb 進行資料整理
```
### MODELING ＆ STRATEGY
```
1. 使用 modeling.ipynb 進行建模
2. 使用 stratage_verify.ipynb 進行策略驗證
```
### 模型更新 ＆ 使用策略
```
1. 模型更新使用 model_update.ipynb
2. 策略使用 game_table.ipynb
```