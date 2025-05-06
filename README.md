![Logo](https://raw.githubusercontent.com/TorBox-App/torbox-media-center/main/assets/header.png)

## About
The TorBox Media Center allows you to easily mount your TorBox media in a no-frills way. This moutns your playable media files to your filesystem for use with Jellyfin, Emby, Plex, Infuse, VLC, or any other media player. With TorBox's custom built solution you can mount files as virtual files (which take up zero storage space), or as .strm files (which take up less than 1GB for libraries of any size).

> [!IMPORTANT]
> *TorBox does not allow piracy or condone it in any way. This is meant to be used with media you own and have the rights to.*

### Features
- Organizing your media automatically, using the TorBox Metadata Search API
- Mounting your media simply and safely
- Making sure your media is easily discoverable by media players
- Fast and effecient.
- Proxy for files *(if your connection is slow)*
- Compatible with all systems and OS *(when using the `strm` mount method)*
- No limit on library size

### Comparison to Zurg
- Usability with TorBox
- Latest features for free
- Faster setup *(no config necessary)*
- No reliance on RClone
- Optimized for TorBox
- More video server/player support
- Works with torrents, usenet and web downloads.

### What this application does not do
- Folder customization *(limited to 'movies' and 'series')*
- Provides WebDAV server *(use TorBox's WebDAV)*
- Works with all types of files *(limited to video files)*
- Gets you banned from TorBox *(developed by TorBox team)*
- 'Repairing' or 'renewing' your library *(this is against TorBox ToS)*
- Adding new downloads
- Customizing downloads *(update/rename)*
- Manage downloads *(delete)*

## Compatibility

### Compatbility with OS
Compatibility is limited to Linux/Unix/BSD based systems when using the `fuse` option due to requiring FUSE.

The `strm` option is compatible with all systems.

If the `fuse` option is selected and your system is incompatible, the application will give an error and will not run.

> [!NOTE]
> If you are unsure, choose the `strm` option.

### Compatbility with players / media servers
The `strm` option is geared towards media servers which support '.strm' files such as Jellyfin and Emby. If using either of these options, we recommend using the `strm` mounting method.

The `fuse` option is meant to be a fallback for everything else, Plex, VLC, Infuse, etc. This is due to the fuse method mounting the virtual files right to your filesystem as if they were local. This means that any video player will be able to stream from them and the TorBox Media Center will handle the rest.

> [!TIP]
> TL;DR: 
> 
> Emby / Jellyfin => `strm`
> 
> Plex / VLC / Anything else => `fuse`


## Choosing a mounting method
Above we explained compatibility, which should be the main driving factor for making a decision, but there are few other things we should mention.

1. The virtual filesystem created by the `fuse` mounting method can be slower (playing files, reading files, listing files and directories) and take up more resources as it emulates an entire filesystem. It also may not play well with your Docker installation (if going that route).
2. The `strm` mounting method takes up more storage space, and disk reads and writes as they are physical text files. Over longer periods of time it can wear down your disk (not by much, but it is something we should mention). If you have a slow filesystem (hard drive vs SSD), this can be slower if you have a lot of files.

## Why not use RClone?
We wanted to reduce the number of moving parts required to use this application. RClone would only be used for FUSE mounting, but every single Linux system ships with some type of FUSE already, so RClone would be redundant. RClone also introduces more challenges, such as configuration, making sure versions are up to date, and you would still need FUSE anyways. This application doesn't provide a WebDAV API, so realistically, RClone isn't necessary here.

## Requirements
1. A TorBox account. Must be on a paid plan. Sign up here.
2. A server or computer running Linux/Unix/BSD/MacOS. Must be able to run Python or has administrator access *(only necessary for Docker installation)*
3. A player in mind you want to use *(for choosing a mounting method)*

## Environment Variables
To run this project you will need to add the following environment variables to your `.env` file or to your Docker run command.

`TORBOX_API_KEY` Your TorBox API key used to authenticate with TorBox. You can find this here. This is required.

`MOUNT_METHOD` The mounting method you want to use. Must be either `strm` or `fuse`. Read here for choosing a method. The default is `strm` and is optional.

`MOUNT_PATH` The mounting path where all of your files will be accessible. If inside of Docker, this path needs to be accessible to other applications. If running locally without Docker, this path must be owned.
