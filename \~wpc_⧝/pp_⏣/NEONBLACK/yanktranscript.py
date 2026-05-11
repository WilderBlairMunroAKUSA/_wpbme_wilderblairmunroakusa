#!/usr/bin/env python3
"""
transcriptdiddy.py - pull youtube transcripts from the command line
usage: python transcriptdiddy.py <url_or_video_id> [--timestamps] [--json] [--out file.txt]
"""
import sys
import re
import json
import argparse
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Missing dep. Run: pip install youtube-transcript-api")
    sys.exit(1)
try:
    import yt_dlp
except ImportError:
    print("Missing dep. Run: pip install yt-dlp")
    sys.exit(1)

def extract_video_id(input_str):
    input_str = input_str.strip()
    if re.match(r'^[a-zA-Z0-9_-]{11}$', input_str):
        return input_str
    patterns = [
        r'[?&]v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'embed/([a-zA-Z0-9_-]{11})',
        r'shorts/([a-zA-Z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, input_str)
        if m:
            return m.group(1)
    return None

def get_video_metadata(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    opts = {'quiet': True, 'skip_download': True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            raw_date = info.get('upload_date', '')  # YYYYMMDD
            if raw_date and len(raw_date) == 8:
                formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
            else:
                formatted_date = 'unknown-date'
            return {
                'title': info.get('title', 'Unknown Title'),
                'upload_date': formatted_date,
                'description': info.get('description', ''),
            }
    except Exception as e:
        print(f"Warning: couldn't fetch video metadata: {e}")
        return {'title': 'Unknown Title', 'upload_date': 'unknown-date', 'description': ''}

def fmt_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"

def normalize(transcript):
    """Handle both old (list of dicts) and new (list of objects) API responses."""
    entries = []
    for e in transcript:
        if isinstance(e, dict):
            entries.append(e)
        else:
            entries.append({'start': e.start, 'text': e.text})
    return entries

def main():
    parser = argparse.ArgumentParser(description='Pull YouTube transcripts')
    parser.add_argument('url', help='YouTube URL or video ID')
    parser.add_argument('--timestamps', action='store_true', help='Include timestamps')
    parser.add_argument('--json', action='store_true', dest='as_json', help='Output raw JSON')
    parser.add_argument('--out', action='store_true', help='Write output to file instead of stdout')
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        print(f"Couldn't parse a video ID from: {args.url}")
        sys.exit(1)

    meta = get_video_metadata(video_id)
    title = meta['title']
    upload_date = meta['upload_date']
    description = meta['description']

    try:
        ytt = YouTubeTranscriptApi()
        raw = ytt.fetch(video_id)
        entries = normalize(raw)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        sys.exit(1)

    header = f"Title: {title}\nDate:  {upload_date}\nDescription: {description}\n\n"

    if args.as_json:
        output = json.dumps({
            'title': title,
            'upload_date': upload_date,
            'description': description,
            'transcript': entries,
        }, indent=2)
    elif args.timestamps:
        body = '\n'.join(f"[{fmt_time(e['start'])}] {e['text']}" for e in entries)
        output = header + body
    else:
        output = header + ' '.join(e['text'] for e in entries)

    if args.out:
        filename = f"{upload_date}_smol_{video_id}.txt"
        with open(filename, 'w') as f:
            f.write(output)
        print(f"Saved → {filename}")
    else:
        print(output)

if __name__ == '__main__':
    main()
