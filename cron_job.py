import os
import datetime
from googleapiclient.discovery import build
from yt_dlp import YoutubeDL
from moviepy.video.io.VideoFileClip import VideoFileClip

# CONFIGURATION
API_KEY = os.environ.get("YOUTUBE_API_KEY")
DOWNLOAD_DIR = "./docs"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_top_trending_stream():
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)
        request = youtube.search().list(
            part="snippet",
            eventType="live",
            type="video",
            order="viewCount",
            maxResults=1,
            regionCode="US"
        )
        response = request.execute()
        if response.get("items"):
            video_id = response["items"][0]["id"]["videoId"]
            title = response["items"][0]["snippet"]["title"]
            print(f"🔥 Top Stream Found: {title} (ID: {video_id})")
            return f"https://youtube.com{video_id}", title
    except Exception as e:
        print(f"❌ API Error: {e}")
    return None, None

def generate_dashboard(video_title):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Clean HTML Dashboard with horizontal card elements and a slide-up animation
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hourly YouTube Shorts Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f1f;
            color: #ffffff;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            color: #ff0055;
            margin-bottom: 5px;
            font-size: 2.5rem;
        }}
        .subtitle {{
            color: #8888a0;
            margin-bottom: 40px;
            font-size: 1rem;
        }}
        /* Horizontal Row Grid Layout */
        .dashboard-row {{
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: center;
            gap: 25px;
            max-width: 1200px;
            width: 100%;
        }}
        /* Sliding Entry Animation */
        .video-card {{
            background: #1a1a2e;
            border-radius: 12px;
            padding: 20px;
            flex: 1;
            min-width: 280px;
            max-width: 350px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            border: 1px solid #252547;
            text-align: left;
            opacity: 0;
            transform: translateY(40px);
            animation: slideUp 0.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }}
        /* Staggered animation delay for cards */
        .video-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .video-card:nth-child(2) {{ animation-delay: 0.3s; }}
        .video-card:nth-child(3) {{ animation-delay: 0.5s; }}

        @keyframes slideUp {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        .card-tag {{
            background: #ff0055;
            color: white;
            font-size: 0.75rem;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 12px;
        }}
        .video-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0 0 10px 0;
            line-height: 1.4;
            color: #e2e2e9;
        }}
        .video-meta {{
            font-size: 0.85rem;
            color: #7c7c93;
            margin-bottom: 20px;
        }}
        .download-btn {{
            display: block;
            text-align: center;
            background: linear-gradient(135deg, #ff0055 0%, #cc0044 100%);
            color: white;
            text-decoration: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
            transition: transform 0.2s, filter 0.2s;
        }}
        .download-btn:hover {{
            transform: scale(1.03);
            filter: brightness(1.1);
        }}
    </style>
</head>
<body>

    <h1>🎬 Stream Cutter Dashboard</h1>
    <div class="subtitle">Last Automated Processing: <strong>{current_time}</strong></div>

    <div class="dashboard-row">
        <!-- Part 1 -->
        <div class="video-card">
            <span class="card-tag">CLIP #1 (INTRO)</span>
            <div class="video-title">{video_title}</div>
            <div class="video-meta">Segment: 20% Timeline Depth</div>
            <a class="download-btn" href="best_part_1.mp4" download>📥 Download Clip</a>
        </div>

        <!-- Part 2 -->
        <div class="video-card">
            <span class="card-tag">CLIP #2 (MIDSTREAM)</span>
            <div class="video-title">{video_title}</div>
            <div class="video-meta">Segment: 50% Timeline Depth</div>
            <a class="download-btn" href="best_part_2.mp4" download>📥 Download Clip</a>
        </div>

        <!-- Part 3 -->
        <div class="video-card">
            <span class="card-tag">CLIP #3 (PEAK CLIMAX)</span>
            <div class="video-title">{video_title}</div>
            <div class="video-meta">Segment: 80% Timeline Depth</div>
            <a class="download-btn" href="best_part_3.mp4" download>📥 Download Clip</a>
        </div>
    </div>

</body>
</html>
"""
    with open(os.path.join(DOWNLOAD_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ Web Dashboard updated successfully!")

def download_and_cut_video(video_url, video_title):
    if not video_url: return
    
    # Clean old items
    for f in os.listdir(DOWNLOAD_DIR):
        if f.endswith('.mp4') or f == 'index.html':
            try: os.remove(os.path.join(DOWNLOAD_DIR, f))
            except: pass

    raw_output = os.path.join(DOWNLOAD_DIR, "raw_video.mp4")
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': raw_output,
        'max_filesize': 30 * 1024 * 1024,
    }
    
    print("⏳ Downloading video...")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        
    if not os.path.exists(raw_output): return

    print("✂️ Slicing video into 3 parts...")
    try:
        with VideoFileClip(raw_output) as video:
            duration = video.duration
            clip_length = 15
            intervals = [duration * 0.2, duration * 0.5, duration * 0.8]
            
            for i, start_time in enumerate(intervals):
                if start_time + clip_length < duration:
                    end_time = start_time + clip_length
                    sub_clip = video.subclipped(start_time, end_time)
                    sub_clip.write_videofile(
                        os.path.join(DOWNLOAD_DIR, f"best_part_{i+1}.mp4"), 
                        codec="libx264", 
                        audio_codec="aac"
                    )
        os.remove(raw_output)
        print("✅ Finished cutting clips successfully!")
        # Fire off the automated layout creation passing the true title
        generate_dashboard(video_title)
    except Exception as e:
        print(f"❌ Video cutting error: {e}")

if __name__ == '__main__':
    url, title = get_top_trending_stream()
    if url:
        download_and_cut_video(url, title)
