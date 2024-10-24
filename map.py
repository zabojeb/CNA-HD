import plotly.express as px
import pandas as pd
import osmnx as ox
import geopandas as gpd
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt


def map(df):
    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        hover_name="name",
        color_discrete_sequence=["blue"],
        zoom=15,
    )
    fig.update_layout(map_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def plot_nearby_places(address, distance=500):
    # Инициализируем геоколлектор
    geolocator = Nominatim(user_agent="i2d")

    # Получаем координаты по адресу
    location = geolocator.geocode(address)
    if location is None:
        print("Не удалось найти адрес.")
        return

    # Получаем координаты
    latitude = location.latitude
    longitude = location.longitude

    # Создаем точку на карте
    point = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy([longitude], [latitude]), crs="EPSG:4326"
    )

    # Находим заведения поблизости
    tags = {"amenity": True}
    nearby_places = ox.features.features_from_point(
        (latitude, longitude), dist=distance, tags=tags
    )
    data_lon = []
    data_lat = []
    nearby_places = nearby_places[["name", "geometry"]]
    n_p = nearby_places.copy(deep=True)
    indexes_to_del = []
    for i, r in nearby_places.iterrows():
        # print((r['geometry']))
        if str(r["geometry"]).startswith("POINT"):
            x, y = r["geometry"].x, r["geometry"].y
            data_lon.append(x)
            data_lat.append(y)
        else:
            indexes_to_del.append(i)

    n_p = nearby_places.drop(indexes_to_del)
    n_p["lon"] = data_lon
    n_p["lat"] = data_lat
    n_p = n_p.dropna()
    # print(n_p)
    map(n_p)


# plot_nearby_places("Россия, Москва, Отель Эден")
