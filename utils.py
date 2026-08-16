# ============================================================================
# UTILITY FUNCTIONS FOR YOUTUBE VIDEO PROCESSING
# ============================================================================

import re


# ============================================================================
# FUNCTION 1: Extract Video ID from YouTube URL
# ============================================================================
def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)

    if match:
        return match.group(1)

    raise ValueError("Invalid YouTube URL. Please use format: https://www.youtube.com/watch?v=VIDEO_ID")


# ============================================================================
# FUNCTION 2: Get Video Title from YouTube
# ============================================================================
def get_video_title(video_id):
    """
    Gets the title of a YouTube video by scraping the page.
    No API key required.
    """
    try:
        import requests
        url = f"https://www.youtube.com/watch?v={video_id}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        match = re.search(r'"title":"(.*?)"', r.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error getting title: {e}")

    return f"Video {video_id}"


# ============================================================================
# FUNCTION 3: Get Transcript from YouTube Video
# ============================================================================
def get_transcript(video_id, languages=('en', 'en-US', 'en-GB')):
    """
    Downloads transcript for a YouTube video.
    Compatible with youtube-transcript-api v1.2.4+.

    Args:
        video_id: YouTube video ID
        languages: Tuple of language codes to try, in order of preference

    Returns:
        Transcript as a single string
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        api = YouTubeTranscriptApi()

        # Try to find a transcript in the preferred languages
        try:
            transcript_list = api.list(video_id)
            print(transcript_list)
            transcript = transcript_list.find_transcript(list(languages))
            print(transcript)
            fetched = transcript.fetch()
            text = " ".join([snippet.text for snippet in fetched])
            print(text)
            print(f"Transcript fetched successfully (language: {transcript.language_code})")
            return text

        # If preferred languages not found, fetch default (whatever is available)
        except Exception:
            print(f"Preferred languages {languages} not found, falling back to default...")
            fetched = api.fetch(video_id)
            text = " ".join([snippet.text for snippet in fetched])
            print("Transcript fetched successfully (default language)")
            return text

    except Exception as e:
        raise Exception(
            f"Could not retrieve transcript for video {video_id}\n"
            f"Reason: {e}\n\n"
            "Possible causes:\n"
            "1. Video has no captions/subtitles enabled\n"
            "2. Video is private or age-restricted\n"
            "3. YouTube is rate-limiting requests\n\n"
            "Suggested fix:\n"
            "- Ensure youtube-transcript-api is up to date: pip install --upgrade youtube-transcript-api"
        )