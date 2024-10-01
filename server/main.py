from fastapi import FastAPI
from starlette.responses import FileResponse
import requests
import collections
from models import Content, Influencer, Place
from typing import List
import Constants
import os
root = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    init()


def init():
    return


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/contents")
async def contents():
    contents: List[Content] = []

    headers = {
        # Notion Api Setting
        # dotenv 처리 필요
        'Authorization': 'secret_cusmrLss0KCCYGtfPUue3bUqCApPk26GLQ5NGcZj2Fq',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    # Load Contents
    responses = get_notion_data("https://api.notion.com/v1/databases/ed379cac2f7f44ef904692a34f9efe39/query", headers)

    for response in responses:    
        for content in response['results']:
            if not content['properties']['influencer']['relation']:
                continue

            copy: Content = Content.Content(
                id=content['properties']['id']['formula']['string'],
                name=content['properties']['name']['title'][0]['text']['content'],
                sourceUrl=content['properties']['source_url']['url'],
                place=content['properties']['place']['relation'][0]['id'],
                influencer=content['properties']['influencer']['relation'][0]['id']
            )
            contents.append(copy)

    return contents


@app.get("/influencers")
async def influencers():
    influencers: List[Influencer] = []

    headers = {
        # Notion Api Setting
        # dotenv 처리 필요
        'Authorization': 'secret_cusmrLss0KCCYGtfPUue3bUqCApPk26GLQ5NGcZj2Fq',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    # Load Influencers
    responses = get_notion_data("https://api.notion.com/v1/databases/21a956c47d594ab8ae31758bf32740a3/query", headers)

    for response in responses:
        for influencer in response['results']:
            copy: Influencer = Influencer.Influencer(
                id=influencer['properties']['id']['formula']['string'],
                name=influencer['properties']['name']['title'][0]['text']['content'],
                platform=Constants.Platform[
                    influencer['properties']['platform']['select']['name'].upper()
                ],
                profileImage=influencer['properties']['profile_image']['url']
            )
            influencers.append(copy)
            
    return influencers


@app.get("/places")
async def places():
    places: List[Place] = []

    headers = {
        # Notion Api Setting
        # dotenv 처리 필요
        'Authorization': 'secret_cusmrLss0KCCYGtfPUue3bUqCApPk26GLQ5NGcZj2Fq',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    # Load Places
    responses = get_notion_data("https://api.notion.com/v1/databases/cab597b093ca47f38d53eb589c193ce8/query", headers)

    for response in responses:
        for place in response['results']:
            if not place['properties']['google_rating']['number']:
                continue

            categories = set()
            for category in place['properties']['categories']['multi_select']:
                categories.add(category['name'])

            copy: Place = Place.Place(
                id=place['properties']['id']['formula']['string'],
                name=place['properties']['name']['title'][0]['text']['content'],
                googleRating=place['properties']['google_rating']['number'],
                googleUserRatingsTotal=place['properties']['google_user_ratings_total']['number'],
                categories=categories,
                address=place['properties']['address']['rich_text'][0]['plain_text'],
                centerLat=place['properties']['centerLat']['number'],
                centerLon=place['properties']['centerLon']['number'],
                phone=place['properties']['phone']['phone_number']
            )

            places.append(copy)

    return places


@app.get("/min-version/aos")
def min_version():
    return Constants.aosMinVersion


@app.get("/min-version/ios")
def min_version():
    return Constants.iosMinVersion


@app.get("/privacy-policy")
def privacy_policy():
    return FileResponse('privacy-policy.html')


def get_notion_data(url, headers, data = None):
    responses = []

    response = requests.post(
        url=url,
        headers=headers,
        json=data
    ).json()

    responses.append(response)


    if response["has_more"] == True:
        next_cursor = response["next_cursor"]
        body = {"start_cursor": next_cursor}
        responses.append(get_notion_data(url, headers, body))

    return list(flatten(responses))


def flatten(l):
    for el in l:
        # if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
        if type(el) is list:
            yield from flatten(el)
        else:
            yield el