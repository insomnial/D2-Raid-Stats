import dateutil.parser
import pandas as pd
from datetime import datetime
import plotly.express as px
from app.reports.ReportBase import Report
from app.data.raidhash import RAID_HASH


class RaidsReport(Report):

    def save(self):
        super().save()

    def getName(self) -> str:
        return "[ALL] chart_area - raids by date"

    def __init__(self, membershipType, membershipId, displayName, manifest) -> None:
        super().__init__(membershipType, membershipId, displayName, manifest)

    def generate(self, data) -> Report:
        df = self.generateDataframe(data)
        fig = px.area(
            df, x='Date', y="playtime",
            title="Playtime per raid, in hours",
            color_discrete_sequence=px.colors.qualitative.Dark24,
            template="plotly_dark",
            color="raid", line_group="character",
            color_discrete_map={
                "Crota's End": "#56bff7",
                "Crown of Sorrows": "#2b7224",
                "Deep Stone Crypt": "#13af68",
                "Eater of Worlds": "#d13fe1",
                "Garden of Salvation": "#7966a6",
                "King's Fall": "#2540f6",
                "Last Wish": "#10369c",
                "Leviathan": "#8f4a0b",
                "The Pantheon": "#12a817",
                "Root of Nightmares": "#24e9f4",
                "Salvation's Edge": "#b3bf66",
                "Scourge of the Past": "#2f0224",
                "Spire of Stars": "#539a2c",
                "Vault of Glass": "#d64f9e",
                "Vow of the Disciple": "#28cd77"
            }
        )
        fig.update_traces(hovertemplate="%{y:.2f}h")
        fig.update_yaxes(matches=None)
        fig.update_yaxes(showticklabels=True)
        fig.update_xaxes(matches='x')
        self.fig = fig
        return self

    def generateRawDataframe(self, data):
        from tqdm import tqdm

        raidArr = []
        starttime_str = []
        starttime = []
        playtime = []
        clazz = []
        character = []

        # parse data in entry
        for datapoint in tqdm(data, desc=self.getName()):
            if "entries" not in datapoint: continue
            timestamp = dateutil.parser.parse(datapoint["period"]).timestamp()
            referenceId = datapoint['activityDetails']['referenceId']
            directorActivityHash = datapoint['activityDetails']['directorActivityHash']
            instanceId = datapoint['activityDetails']['instanceId']
            # get specifics of activity
            for entry in datapoint["entries"]:
                if entry["player"]["destinyUserInfo"]["membershipId"] != str(self.membershipId): continue
                if entry["player"]["classHash"] == 0: continue

                for raid in RAID_HASH:
                    if directorActivityHash in RAID_HASH[raid]:
                        raidArr.append(raid)

                starts = entry["values"]["startSeconds"]["basic"]["value"] # start time
                ends = starts + entry["values"]["timePlayedSeconds"]["basic"]["value"] # end time

                strtime = datetime.fromtimestamp(timestamp + starts).strftime("%Y-%m-%d %H:00") # total time
                starttime.append(pd.Timestamp(strtime))
                starttime_str.append(strtime)
                playtime.append(entry["values"]["timePlayedSeconds"]["basic"]["value"] / 60)
                
                if entry["player"]["classHash"] == 3655393761:
                    clazz.append("Titan")
                elif entry["player"]["classHash"] == 671679327:
                    clazz.append("Hunter")
                elif entry["player"]["classHash"] == 2271682572:
                    clazz.append("Warlock")

                character.append(entry["characterId"])

        df = pd.DataFrame({
            "start": starttime,
            "starttime_str": starttime_str,
            "playtime": playtime,
            "class": clazz,
            "character": character,
            "raid": raidArr
        })


        return df

    def generateDataframe(self, data):
        df = self.generateRawDataframe(data)
        df2 = df
        df2["Date"] = pd.to_datetime(df2['starttime_str']) - pd.to_timedelta(7, unit='d')
        df2 = df2.groupby(["raid", "class", "character", pd.Grouper(key='Date', freq='d')])["playtime"] \
            .sum().reset_index().sort_values('Date')

        lastDate = df2["Date"].tail(1).values[0]
        characterIds = df2["character"].unique()

        lastForChar = {k: 0 for k in characterIds}

        raidArr = []
        starttime_str = []
        starttime = []
        playtime = []
        clazz = []
        character = []

        for charId in characterIds:
            datax = df2[df2["character"] == charId]
            charClazz = datax.head(1)["class"].values[0]
            raidClazz = datax.head(1)["raid"].values[0]
            firstDate = datax.head(1)["Date"].values[0] + 0
            Dates = datax["Date"].unique()
            while firstDate < lastDate:
                if firstDate in Dates:
                    lastForChar[charId] += datax[datax["Date"] == firstDate]["playtime"].values[0]

                strtime = datetime.fromtimestamp(pd.Timestamp(firstDate).timestamp()).strftime("%Y-%m-%d %H:00")
                starttime.append(pd.Timestamp(strtime))
                starttime_str.append(strtime)
                playtime.append(lastForChar[charId])
                clazz.append(charClazz)
                character.append(charId)
                raidArr.append(raidClazz)

                firstDate += 24 * 60 * 60 * 1000000000

        df2 = pd.DataFrame({
            "start": starttime,
            "starttime_str": starttime_str,
            "playtime": playtime,
            "class": clazz,
            "character": character,
            "raid": raidArr
        })

        df2["Date"] = pd.to_datetime(df2['starttime_str']) - pd.to_timedelta(7, unit='d')
        df2 = df2.groupby(["raid", "class", "character", pd.Grouper(key='Date', freq='d')])["playtime"] \
            .sum().reset_index().sort_values(["raid", 'Date', "character", "playtime"])

        df2["playtime"] /= 60

        return df2
