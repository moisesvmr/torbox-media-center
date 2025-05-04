from library.http import api_http_client, search_api_http_client
from enum import Enum
import PTN
from library.torbox import TORBOX_API_KEY

class DownloadType(Enum):
    torrent = "torrents"
    usenet = "usenet"
    webdl = "webdl"

class IDType(Enum):
    torrents = "torrent_id"
    usenet = "usenet_id"
    webdl = "web_id"

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
            if not file.get("mimetype").startswith("video/"):
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
            }
            title_data = PTN.parse(file.get("short_name"))
            metadata, _, _ = searchMetadata(title_data.get("title"))
            data.update(metadata)
            files.append(data)
            
    return files, True, f"{type.value.capitalize()} fetched successfully."

def searchMetadata(query: str):
    base_metadata = {
        "metadata_title": "",
        "metadata_link": "",
        "metadata_mediatype": "",
        "metadata_image": "",
        "metadata_backdrop": "",
        "metadata_years": ""
    }
    response = search_api_http_client.get(f"/meta/search/{query}")
    if response.status_code != 200:
        return base_metadata, False, f"Error searching metadata. {response.status_code}"
    try:
        data = response.json().get("data", [])[0]
        base_metadata["metadata_title"] = data.get("title")
        base_metadata["metadata_link"] = data.get("link")
        base_metadata["metadata_mediatype"] = data.get("type")
        base_metadata["metadata_image"] = data.get("image")
        base_metadata["metadata_backdrop"] = data.get("backdrop")
        base_metadata["metadata_years"] = data.get("releaseYears")
        return base_metadata, True, "Metadata found."
    except IndexError:
        return base_metadata, False, "No metadata found."
