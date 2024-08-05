import os
import time
import configparser
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

# Constants
MAX_WORKERS = 10

# Utility functions
def is_valid_api_key(api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    try:
        youtube.search().list(part="id", maxResults=1, q="test").execute()
        return True
    except HttpError:
        return False

def get_api_key():
    while True:
        api_key = input("YouTube Data API key: ")
        if api_key.strip() and is_valid_api_key(api_key):
            return api_key
        else:
            print("Invalid API key. Please enter a valid API key.")

def get_channel_id():
    while True:
        channel_id = input("Channel_ID to search: ")
        if channel_id.strip():
            return channel_id
        else:
            print("Invalid Channel ID. Please enter a valid Channel ID.")

def get_max_results():
    while True:
        try:
            max_results = int(input("Number of videos to search (starts from newest video): "))
            if max_results > 0:
                return max_results
            else:
                print("Invalid input. Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_language_code():
    while True:
        language_code = input("Caption language code (default: en): ")
        if not language_code.strip():
            return "en"
        elif len(language_code) == 2:
            return language_code
        else:
            print("Invalid input. Please enter a valid two-letter language code.")

def get_authenticated_service(api_key):
    return build("youtube", "v3", developerKey=api_key)

def has_captions(video_id, language_code):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([language_code])
        transcript.fetch()
        return True
    except Exception:
        return False

def get_video_details(youtube, video_id):
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id,
    ).execute()

    video_info = response["items"][0]["snippet"]
    video_statistics = response["items"][0]["statistics"]
    title = video_info["title"]
    channel_title = video_info["channelTitle"]
    channel_id = video_info["channelId"]
    date_uploaded = video_info["publishedAt"]
    views = int(video_statistics["viewCount"])

    return title, channel_title, channel_id, date_uploaded, views

def format_views(views):
    return "{:,}".format(views)

def save_preferences(api_key):
    config = configparser.ConfigParser()
    config['Preferences'] = {'API_KEY': api_key}
    with open('preferences.ini', 'w') as configfile:
        config.write(configfile)

def load_preferences():
    config = configparser.ConfigParser()
    config.read('preferences.ini')
    return config.get('Preferences', 'API_KEY', fallback='')

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def get_video_ids_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            video_ids = [line.strip() for line in file.readlines()]
        return video_ids
    except FileNotFoundError:
        print("File not found. Please enter a valid file path.")
        return None

def get_video_ids_input():
    while True:
        video_ids_input = input("Enter video ID(s) separated by commas or path to a file with video ID(s): ")
        if ',' in video_ids_input:
            return [vid.strip() for vid in video_ids_input.split(',')]
        elif os.path.isfile(video_ids_input):
            return get_video_ids_from_file(video_ids_input)
        else:
            return [video_ids_input.strip()]

def get_channel_videos(youtube, channel_id, language_code="en", max_results=10):
    video_ids = []
    nextPageToken = None

    with Progress(
        TextColumn("[steel_blue]Fetching video IDs...", table_column=Column(ratio=1)),
        BarColumn(bar_width=30, table_column=Column(ratio=2)),
        "[yellow4][progress.percentage]{task.percentage:>3.0f}%[/yellow4] [white]•[/white]",
        "Fetched IDs: [dodger_blue2]{task.completed}/{task.total}[/dodger_blue2] •",
        "[bright_red]ETA: [progress.time_remaining]{task.time_remaining}s",
        expand=False,
    ) as progress:
        task = progress.add_task("Fetching IDs", total=max_results)

        while len(video_ids) < max_results:
            try:
                response = youtube.search().list(
                    part="id",
                    channelId=channel_id,
                    maxResults=50,
                    order="date",
                    pageToken=nextPageToken,
                ).execute()

                for item in response["items"]:
                    if "videoId" in item["id"]:
                        video_id = item["id"]["videoId"]
                        if video_id not in video_ids and has_captions(video_id, language_code):
                            video_ids.append(video_id)
                            progress.update(task, advance=1)
                        if len(video_ids) >= max_results:
                            break
                nextPageToken = response.get("nextPageToken")
                if not nextPageToken:
                    break
            except HttpError as e:
                print(f"An HTTP error {e.resp.status} occurred: {e.content}")
                break

    if not video_ids:
        print(f"No videos found with captions in the selected language ({language_code}).")
        exit()

    return video_ids

def prompt_search_type():
    while True:
        search_type = input("Search mode: Channel ID/Video ID(s)? Enter 'channel' or 'video': ").lower()
        if search_type in ['channel', 'video']:
            return search_type
        else:
            print("Invalid input. Please enter 'channel' or 'video'.")

def fetch_transcript(video_id, language_code, target_word):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        transcript_items = [item for item in transcript if target_word.lower() in item["text"].lower()]
        return transcript_items
    except (NoTranscriptFound, TranscriptsDisabled):
        return []

def main():
    API_KEY = load_preferences()
    if not API_KEY or input("Do you want to change the API key? (y/n): ").lower() == 'y':
        API_KEY = get_api_key()
        save_preferences(API_KEY)

    youtube = get_authenticated_service(API_KEY)
    search_type = prompt_search_type()

    if search_type == 'channel':
        channel_id = get_channel_id()
        max_results = get_max_results()
        language_code = get_language_code()
        video_ids = get_channel_videos(youtube, channel_id, language_code, max_results)
    else:
        video_ids = get_video_ids_input()
        language_code = get_language_code()

    target_word = input("Enter the word (or phrase) to search in the captions: ")
    output_dir = "transcripts"
    os.makedirs(output_dir, exist_ok=True)

    all_video_details = []
    match_count = 0

    start_time = time.time()

    with Progress(
        TextColumn("[yellow]Searching...", justify="left"),
        BarColumn(bar_width=30),
        TextColumn("[yellow4][progress.percentage]{task.percentage:>3.0f}%[/yellow4]", justify="right"),
        TextColumn("| [bright_red]ETA: {task.time_remaining}s[/bright_red] |", justify="right"),
        TextColumn("Found [green]{task.fields[match_count]}[/green] matches!"),
    ) as progress:
        task = progress.add_task("", total=len(video_ids), match_count=match_count)

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(fetch_transcript, video_id, language_code, target_word): video_id for video_id in video_ids}
            for future in as_completed(futures):
                video_id = futures[future]
                try:
                    transcript_items = future.result()
                    if transcript_items:
                        match_count += len(transcript_items)
                        title, channel_title, channel_id, date_uploaded, views = get_video_details(youtube, video_id)
                        video_details = f"Video Title: {title}\n"
                        video_details += f"Video ID: {video_id}\n"
                        video_details += f"Channel Name: {channel_title}\n"
                        video_details += f"Channel ID: {channel_id}\n"
                        video_details += f"Date Uploaded: {date_uploaded}\n"
                        video_details += f"Views: {format_views(views)}\n"
                        video_details += "Timestamps:\n"
                        for item in transcript_items:
                            time_str = format_time(item['start'])
                            video_details += f"╳ {time_str} - {item['text']}\n"
                        video_details += "\n══════════════════════════════════════════════\n\n"
                        all_video_details.append(video_details)
                    elapsed_time = time.time() - start_time
                    progress.update(task, advance=1, match_count=match_count)
                except Exception as e:
                    print(f"Error processing video ID {video_id}: {e}")

    print(f"\n\nSearch finished!")
    print(f"Found a total of {match_count} match{'es' if match_count != 1 else ''} in the captions.")

    output_file_name = f"{target_word}.txt"
    output_file_path = os.path.join(output_dir, output_file_name)
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.writelines(all_video_details)

    print(f"Generated .txt file at: {output_file_path}")

if __name__ == "__main__":
    main()
