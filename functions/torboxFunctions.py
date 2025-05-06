from library.http import api_http_client, search_api_http_client, general_http_client
import httpx
from enum import Enum
import PTN
from library.torbox import TORBOX_API_KEY
from functions.mediaFunctions import constructSeriesTitle, cleanTitle
from functions.databaseFunctions import insertData
import os
import logging

class DownloadType(Enum):
    torrent = "torrents"
    usenet = "usenet"
    webdl = "webdl"

class IDType(Enum):
    torrents = "torrent_id"
    usenet = "usenet_id"
    webdl = "web_id"

ACCEPTABLE_MIME_TYPES = [
    "video/x-matroska",
    "video/mp4",
]

def getUserDownloads(type: DownloadType):
    params = {
        "limit": 10000,
        "bypass_cache": False,
    }
    response = api_http_client.get(f"/{type.value}/mylist", params=params)

    if response.status_code != 200:
        return None, False, f"Error fetching {type.value}. {response.status_code}"

    data = response.json().get("data", [])
    if not data:
        return None, True, f"No {type.value} found."
    
    files = []
    
    for item in data:
        if not item.get("cached", False):
            continue
        for file in item.get("files", []):
            if not file.get("mimetype").startswith("video/") or file.get("mimetype") not in ACCEPTABLE_MIME_TYPES:
                logging.debug(f"Skipping file {file.get('short_name')} with mimetype {file.get('mimetype')}")
                continue
            data = {
                "item_id": item.get("id"),
                "type": type.value,
                "folder_name": item.get("name"),
                "folder_hash": item.get("hash"),
                "file_id": file.get("id"),
                "file_name": file.get("short_name"),
                "file_size": file.get("size"),
                "file_mimetype": file.get("mimetype"),
                "path": file.get("name"),
                "download_link": f"https://api.torbox.app/v1/api/{type.value}/requestdl?token={TORBOX_API_KEY}&{IDType[type.value].value}={item.get('id')}&file_id={file.get('id')}&redirect=true",
                "extension": os.path.splitext(file.get("short_name"))[-1],              
            }
            title_data = PTN.parse(file.get("short_name"))
            metadata, _, _ = searchMetadata(title_data.get("title"), title_data, file.get("short_name"), f"{item.get('name')} {file.get('short_name')}")
            data.update(metadata)
            files.append(data)
            logging.debug(data)
            insertData(data, type.value)
            
    return files, True, f"{type.value.capitalize()} fetched successfully."

def searchMetadata(query: str, title_data: dict, file_name: str, full_title: str):
    base_metadata = {
        "metadata_title": cleanTitle(query),
        "metadata_link": None,
        "metadata_mediatype": "movie",
        "metadata_image": None,
        "metadata_backdrop": None,
        "metadata_years": None,
        "metadata_season": None,
        "metadata_episode": None,
        "metadata_filename": file_name,
        "metadata_rootfoldername": title_data.get("title", None),
    }
    extension = os.path.splitext(file_name)[-1]
    response = search_api_http_client.get(f"/meta/search/{full_title}", params={"type": "file"})
    if response.status_code != 200:
        return base_metadata, False, f"Error searching metadata. {response.status_code}"
    try:
        data = response.json().get("data", [])[0]
        title = cleanTitle(data.get("title"))
        base_metadata["metadata_title"] = title

        if data.get("type") == "anime" or data.get("type") == "series":
            series_season_episode = constructSeriesTitle(season=title_data.get("season", None), episode=title_data.get("episode", None))
            file_name = f"{title} {series_season_episode}{extension}"
            base_metadata["metadata_foldername"] = constructSeriesTitle(season=title_data.get("season"), folder=True)
            base_metadata["metadata_season"] = title_data.get("season")
            base_metadata["metadata_episode"] = title_data.get("episode")
        elif data.get("type") == "movie":
            file_name = f"{title} ({data.get('releaseYears')}){extension}"
        else:
            return base_metadata, False, "No metadata found."
            
        base_metadata["metadata_filename"] = file_name
        base_metadata["metadata_mediatype"] = data.get("type")
        base_metadata["metadata_link"] = data.get("link")
        base_metadata["metadata_image"] = data.get("image")
        base_metadata["metadata_backdrop"] = data.get("backdrop")
        base_metadata["metadata_years"] = title_data.get("year", None) or data.get("releaseYears")
        base_metadata["metadata_rootfoldername"] = f"{title} ({base_metadata['metadata_years']})"

        return base_metadata, True, "Metadata found."
    except IndexError:
        return base_metadata, False, "No metadata found."
    except Exception as e:
        logging.error(f"Error searching metadata: {e}")
        return base_metadata, False, f"Error searching metadata: {e}"

def getDownloadLink(url: str):
    response = general_http_client.get(url)
    if response.status_code == httpx.codes.TEMPORARY_REDIRECT or response.status_code == httpx.codes.PERMANENT_REDIRECT or response.status_code == httpx.codes.FOUND:
        return response.headers.get('Location')
    return url

def downloadFile(url: str, size: int, offset: int = 0):
    headers = {
        "Range": f"bytes={offset}-{offset + size - 1}",
        **general_http_client.headers,
    }
    response = general_http_client.get(url, headers=headers)
    if response.status_code == httpx.codes.OK:
        return response.content
    elif response.status_code == httpx.codes.PARTIAL_CONTENT:
        return response.content
    else:
        logging.error(f"Error downloading file: {response.status_code}")
        raise Exception(f"Error downloading file: {response.status_code}")
    
