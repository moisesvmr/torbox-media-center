from library.http import api_http_client, search_api_http_client, general_http_client
import httpx
from enum import Enum
import PTN
from library.torbox import TORBOX_API_KEY
from functions.mediaFunctions import constructSeriesTitle, cleanTitle, cleanYear
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

# Ahora filtramos por extensiones populares de video
ACCEPTABLE_EXTENSIONS = ('.mp4', '.mkv', '.avi')

def getUserDownloads(type: DownloadType):

    offset = 0
    limit = 1000

    file_data = []
    
    while True:
        params = {
            "limit": limit,
            "offset": offset,
            "bypass_cache": True,
        }
        try:
            response = api_http_client.get(f"/{type.value}/mylist", params=params)
        except Exception as e:
            logging.error(f"Error fetching {type.value}: {e}")
            return None, False, f"Error fetching {type.value}: {e}"
        if response.status_code != 200:
            return None, False, f"Error fetching {type.value}. {response.status_code}"
        data = response.json().get("data", [])
        if not data:
            break
        file_data.extend(data)
        offset += limit
        if len(data) < limit:
            break

    if not file_data:
        return None, True, f"No {type.value} found."
    
    logging.debug(f"Fetched {len(file_data)} {type.value} items from API.")
    
    files = []
    
    for item in file_data:
        if not item.get("cached", False):
            continue
        for file in item.get("files", []):
            # Cambia esta línea: checa por extensión en lugar de mimetype
            if not file.get("short_name", "").lower().endswith(ACCEPTABLE_EXTENSIONS):
                logging.debug(f"Skipping file {file.get('short_name')} with extension {os.path.splitext(file.get('short_name'))[-1]}")
                continue
            data = {
                "item_id": item.get("id"),
                "type": type.value,
                "folder_name": item.get("name"),
                "folder_hash": item.get("hash"),
                "file_id": file.get("id"),
                "file_name": file.get("short_name"),
                "file_size": file.get("size"),
                "file_mimetype": file.get("mimetype"),  # Puedes dejarlo o quitarlo ya que no filtras por él
                "path": file.get("name"),
                "download_link": f"https://api.torbox.app/v1/api/{type.value}/requestdl?token={TORBOX_API_KEY}&{IDType[type.value].value}={item.get('id')}&file_id={file.get('id')}&redirect=true",
                "extension": os.path.splitext(file.get("short_name"))[-1],              
            }
            title_data = PTN.parse(file.get("short_name"))

            if item.get("name") == item.get("hash"):
                item["name"] = title_data.get("title", file.get("short_name"))

            metadata, _, _ = searchMetadata(title_data.get("title", file.get("short_name")), title_data, file.get("short_name"), f"{item.get('name')} {file.get('short_name')}")
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
    try:
        response = search_api_http_client.get(f"/meta/search/{full_title}", params={"type": "file"})
    except Exception as e:
        logging.error(f"Error searching metadata: {e}")
        return base_metadata, False, f"Error searching metadata: {e}"
    if response.status_code != 200:
        logging.error(f"Error searching metadata: {response.status_code}")
        return base_metadata, False, f"Error searching metadata. {response.status_code}"
    try:
        data = response.json().get("data", [])[0]

        title = cleanTitle(data.get("title"))
        base_metadata["metadata_title"] = title
        base_metadata["metadata_years"] = cleanYear(title_data.get("year", None) or data.get("releaseYears"))

        if data.get("type") == "anime" or data.get("type") == "series":
            series_season_episode = constructSeriesTitle(season=title_data.get("season", None), episode=title_data.get("episode", None))
            file_name = f"{title} {series_season_episode}{extension}"
            base_metadata["metadata_foldername"] = constructSeriesTitle(season=title_data.get("season", 1), folder=True)
            base_metadata["metadata_season"] = title_data.get("season", 1)
            base_metadata["metadata_episode"] = title_data.get("episode")
        elif data.get("type") == "movie":
            file_name = f"{title} ({base_metadata['metadata_years']}){extension}"
        else:
            return base_metadata, False, "No metadata found."
            
        base_metadata["metadata_filename"] = file_name
        base_metadata["metadata_mediatype"] = data.get("type")
        base_metadata["metadata_link"] = data.get("link")
        base_metadata["metadata_image"] = data.get("image")
        base_metadata["metadata_backdrop"] = data.get("backdrop")
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
