def constructSeriesTitle(season = None, episode = None, folder: bool = False):
    title_season = None
    title_episode = None

    if isinstance(season, list):
        # get first and last season
        title_season = f"S{season[0]:02}-S{season[-1]:02}"
    elif isinstance(season, int) or season is not None:
        if folder:
            title_season = f"Season {season}"
        else:
            title_season = f"S{season:02}"
    
    if isinstance(episode, list):
        # get first and last episode
        title_episode = f"E{episode[0]:02}-E{episode[-1]:02}"
    elif isinstance(episode, int) or episode is not None:
        title_episode = f"E{episode:02}"

    if title_season and title_episode:
        return f"{title_season} {title_episode}"
    elif title_season:
        return title_season
    elif title_episode:
        return title_episode
    else:
        return None