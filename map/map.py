import plotly.express as px
import pandas as pd
import osmnx as ox
import geopandas as gpd
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt

from requests import get
import os

YANDEX_MAPS_API_KEY = os.getenv("YANDEX_MAPS_API_KEY")

def make_href_for_hotel(hotel):
    pt = f"{hotel[1]},{hotel[0]}"
    href = f"https://yandex.ru/maps/?ll={hotel[1]},{hotel[0]}&text=достопримечательности&pt={pt}&z=16&l=map"
    return href


def make_href_for_cords(cords: list[str]):
    try:
        print(cords)
        hotel = list(map(float, cords))

        pt = f"{hotel[0]},{hotel[1]}"
    except Exception as e:
        return "Error"
    href = f"https://yandex.ru/maps/?ll={hotel[0]},{hotel[1]}&text=достопримечательность&pt={pt}&z=16&l=map"
    return href


def find_cords(address):
    resp = get(
        f"https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_MAPS_API_KEY}&geocode={'+'.join(address.split())}&format=json"
    )
    try:
        return resp.json()["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"
        ]["Point"]["pos"].split()
    except Exception as e:
        return resp


def lat_and_lon(cords, distance=500):
    # Инициализируем геоколлектор
    geolocator = Nominatim(user_agent="i2d")
    try:
        print(cords, 4)
        latitude, longitude = list(map(float, cords.split(", ")))

        # Находим заведения поблизости
        print((latitude, longitude))
        tags = {"amenity": True}
        nearby_places = ox.features.features_from_point(
            (latitude, longitude), dist=distance, tags=tags
        )

        if nearby_places.empty:
            return None

        return (latitude, longitude)
    except Exception as e:
        print(e)
        return None
