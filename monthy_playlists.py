import pandas as pd
from findplaylist import Playlist, Song

df = pd.read_csv("monthly_playlists.csv")
print(df["ID"])
