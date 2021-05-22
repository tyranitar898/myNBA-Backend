# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayoffseries
from nba_api.stats.endpoints import leaguestandingsv3
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.static import players
from pandas import DataFrame 
import pandas as pd
import numpy as np
import os
import time
from sklearn.mixture import GaussianMixture as GMM
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler



# %%
# GETS a given players SEASONAL STAT
# PARAM
# NAME: str
# SEASON : str
# returns   SeasonStatsdf of that SEASON for the PLAYER
def getSeasonTotalForPlayer(name, season):
    Id = players.find_players_by_full_name(name)[0]["id"]
    career = playercareerstats.PlayerCareerStats(player_id=Id)
    seasonTotalsDf = career.season_totals_regular_season.get_data_frame()
    seasonStatsDf = seasonTotalsDf.loc[seasonTotalsDf["SEASON_ID"] == season]
    #add name for convience
    seasonStatsDf.insert(0, 'Name', name)
    return seasonStatsDf

NAME = 'Dikembe Mutombo'
SEASON = "2000-01"
dm_df = getSeasonTotalForPlayer(NAME, SEASON)
dm_df


# %%
# GETS a list of NBA player names that played in given a SEASON that has played
# more than FIVE minutes in any one game within the series
# PARAM
# SEASON : str
# returns   list of names : str
def getFinalsPlayers(season_yr):
    playoffs = commonplayoffseries.CommonPlayoffSeries(season=season_yr)
    poffDf = playoffs.playoff_series.get_data_frame()
    seriesCol = poffDf["SERIES_ID"]
    #get the last series id of that years playoff (nba finals)
    finalsSeriesID = seriesCol.max()
    finalsDf = poffDf.loc[poffDf["SERIES_ID"]==finalsSeriesID]
    finalsGameIds = finalsDf["GAME_ID"].values

    #gets all players who played more than 5 minutes in NBA FINALS
    FinalsPlayerNames = set()
    for g in finalsGameIds:
        #current final games boxscore
        bs = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=g)
        bsDf = bs.player_stats.get_data_frame()
        #get the two finals teams abrevations 
        final_abrev = bsDf["TEAM_ABBREVIATION"].unique()
        #drops dataframe rows that contain NAN
        bsDf.dropna(subset = ["MIN"], inplace=True)
        #regex for more than 5 minutes
        regex = "^\d\d\:|[5-9]\:"
        bsFilterByMinutesDf = bsDf[bsDf["MIN"].str.contains(regex)]
        #get the names of the playesr who >= 5 minutes
        curgPlayerNames = bsFilterByMinutesDf["PLAYER_NAME"].values
        FinalsPlayerNames.update(curgPlayerNames)
    return list(FinalsPlayerNames), final_abrev

SEASON = "2018"
getFinalsPlayers(SEASON)


# %%
#takes all the nba players that played in these finals and gets their career stat and saves it to csvs
YEARS = ["2000-01", "2001-02", "2002-03", "2003-04", "2004-05","2005-06","2006-07","2007-08","2008-09","2009-10", "2010-11", "2011-12", "2012-13", "2013-14","2014-15","2015-16","2016-17","2017-18","2018-19","2019-20"]
for y in YEARS:
    yr = y[:4]
    seasonStr = y
    #need finals abrevations cuz someplayers switch midseason to win RINGS
    finalsPlayersForYr, final_abrev = getFinalsPlayers(yr)

    playerStatDf_Arr = []
    for p in finalsPlayersForYr:
        #for api calls
        time.sleep(0.5)
        p_seasonStat_df = getSeasonTotalForPlayer(p, seasonStr)
        #makes sure to get the season stat of that player when they were on the finals team
        p_seasonStat_df = p_seasonStat_df[p_seasonStat_df["TEAM_ABBREVIATION"].isin(final_abrev)]
        playerStatDf_Arr.append(p_seasonStat_df)

    finalsPLayersSeasonStat_df = pd.concat(playerStatDf_Arr, ignore_index=True)
    finalsPLayersSeasonStat_df.to_csv("./finalsPlayersSeasonStat/"+seasonStr+"_finals_player_stats"+".csv")
        


# %%
def getPerGameFeature(df, var):
  return df.apply(
      lambda row:
          row[var]/ row.GP,
      axis=1
  )

# Get and filter data from directory
directory = os.path.join("./","finalsPlayersSeasonStat")
allYrsAllPlayersStatDf_Arr = []
FEATURES = ["FG_PCT", "FT_PCT"]
perGame_Features = ["STLPG","ASTPG","BLKPG","REBPG","PTSPG","FG3MPG"]

for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
        f_path = os.path.join(directory, filename)
        f=open(f_path, 'r')
        curYr_df = pd.read_csv(f_path)
        allYrsAllPlayersStatDf_Arr.append(curYr_df)
        f.close()
# Create dataframe with data
X = pd.concat(allYrsAllPlayersStatDf_Arr, ignore_index=True)

# Augment certian features (computes per game features)
for f in perGame_Features:
    featureName = f[:-2]
    X[f] = getPerGameFeature(X, featureName)
allFeatures = FEATURES+perGame_Features
featureFilterd_X_df = X[allFeatures]

# NORMALIZE for better result
# create a scaler object
scaler = RobustScaler()
# fit and transform the data
df_robust = pd.DataFrame(scaler.fit_transform(featureFilterd_X_df), columns=featureFilterd_X_df.columns)

# GMM Clustering
N_CLUSTERS = 16
gmm = GMM(n_components=N_CLUSTERS, covariance_type="full", random_state=2).fit(df_robust)
labels = gmm.predict(df_robust)

# add labels to data df
X.insert(loc=1, column='GMM_CLASS', value=pd.Series(labels))


# %%
leag = leaguestandingsv3.LeagueStandingsV3(season='2005')
leag.get_data_frames()[0]


# %%
n_components = np.arange(1, 41)
models = [GMM(n, covariance_type='full', random_state=0).fit(df_robust)
          for n in n_components]

plt.plot(n_components, [m.bic(df_robust) for m in models], label='BIC')
plt.plot(n_components, [m.aic(df_robust) for m in models], label='AIC')
plt.legend(loc='best')
plt.xlabel('n_components');


# %%
result = leaguegamefinder.LeagueGameFinder()
all_games = result.get_data_frames()[0]
# Find the game_id we want
full_game = all_games[all_games.GAME_ID == '0040800405']
full_game


# %%
bs = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id='0040800117')
bs.get_data_frames()[0]


# %%
playoffs = commonplayoffseries.CommonPlayoffSeries(season="2018-19")
poffDf = playoffs.playoff_series.get_data_frame()
bs = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id="0041800101")
bsDf = bs.player_stats.get_data_frame()
bsDf["TEAM_ABBREVIATION"].unique()


# %%
# d = {'col1': [100, 200, 300], 'col2': [0.3, 0.4, 0.8]}
d = {'col1': [1,2,3,4,5,6,7,8,9,10,11,12], 'col2': [1,2,3,4,5,6,7,8,9,10,11,12], 'col3': [100,200,300,400,500,600,700,800,900,1000,1100,1200]}
df = pd.DataFrame(data=d)
# create a scaler object
scaler = RobustScaler()
# fit and transform the data

df_robust = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
gmm = GaussianMixture(n_components=3, covariance_type="diag", random_state=0).fit(df)
labels = gmm.predict(df)
df.insert(loc=1, column='GMM_CLASS', value=pd.Series(labels))
df


# %%



