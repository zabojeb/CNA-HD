import plotly.express as px
import pandas as pd
import osmnx as ox
import geopandas as gpd
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt


def make_href_for_hotel(hotel):
    pt = f"{hotel[1]},{hotel[0]}"
    href = f'https://yandex.ru/maps/?ll={hotel[1]},{hotel[0]}&text=кафе&pt={pt}&z=16&l=map'
    return href


def lat_and_lon(cords, distance=500):
    # Инициализируем геоколлектор
    geolocator = Nominatim(user_agent="i2d")
    try:
        print(cords,4)
        latitude, longitude = list(map(float,cords.split(', ')))
    

    
        # Находим заведения поблизости
    
    
        print((latitude, longitude))
        tags = {'amenity': True}
        nearby_places = ox.features.features_from_point((latitude, longitude), dist=distance, tags=tags)
        #print(nearby_places)
        if nearby_places.empty:
            return None
        
        return (latitude, longitude)
    except Exception as e:
        print(e)
        return None
        
    
#plot_nearby_places("Россия, Москва, Отель Эден")
#59.148141, 37.942938