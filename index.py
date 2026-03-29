"""
YouTube Downloader
Downloads the highest quality audio+video from YouTube videos
"""

import yt_dlp
import os
import sys

def download_youtube_video(url, output_path, format_choice="bestvideo+bestaudio[ext=m4a]/best"):
    """
        Download the highest quality video+audio from YouTube as MP4

        Args:
            url: YouTube video URL
            output_path: Where to save the file (uses video title automatically)
        """
    ydl_opts = {
        'format': format_choice,
        'merge_output_format': 'mp4',  # yt-dlp handles FFmpeg merging automatically
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'no_warnings': True,
        'extract_flat': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'Unknown')
            print(f"\n✅ Successfully downloaded: {video_title}")
            print(f"📁 Saved to: {output_path}")

            return True

    except Exception as e:
        print(f"❌ Error downloading file: {str(e)}")
        return False


def download_youtube_audio(url, output_path=".", codec="mp3"):
    """
    Download audio from YouTube video in highest quality

    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the audio file
        format_choice (str): Audio format preference
    """

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best audio available
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extract audio
            'preferredcodec': codec,  # Convert to MP3 (change to 'm4a', 'opus', etc.)
            'preferredquality': '0',  # 0 = best quality
        }],
        'outtmpl': os.path.join(output_path, './downloads/%(title)s.%(ext)s'),  # Save as video title
        'quiet': False,  # Show download progress
        'no_warnings': True,  # Show warnings
        'extract_flat': False,  # Extract full metadata
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from: {url}")

            # Get video info
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'Unknown')

            print(f"\n✅ Successfully downloaded: {video_title}")
            print(f"📁 Saved to: {output_path}")

            return True

    except Exception as e:
        print(f"❌ Error downloading audio: {str(e)}")
        return False


def download_with_custom_format(url, output_path=".", format_code="bestaudio"):
    """
    Download audio with custom format options

    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the file
        format_code (str): yt-dlp format code
    """

    ydl_opts = {
        'format': format_code,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"\n✅ Successfully downloaded: {info.get('title', 'Unknown')}")
            return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def list_available_formats(url):
    """
    List all available formats for a video
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            print(f"\nAvailable formats for: {info.get('title', 'Unknown')}\n")
            print("Format Code | Extension | Resolution/Quality | File Size")
            print("-" * 60)

            for f in formats:
                format_id = f.get('format_id', 'N/A')
                ext = f.get('ext', 'N/A')
                quality = f.get('format_note', 'N/A')
                filesize = f.get('filesize', 0)
                filesize_mb = filesize / (1024 * 1024) if filesize else 0

                if filesize:
                    print(f"{format_id:11} | {ext:9} | {quality:18} | {filesize_mb:.2f} MB")
                else:
                    print(f"{format_id:11} | {ext:9} | {quality:18} | N/A")

            return True
    except Exception as e:
        print(f"❌ Error listing formats: {str(e)}")
        return False


def main():
    """Main function with user interface"""
    print("=" * 50)
    print("YouTube Audio Downloader")
    print("=" * 50)

    # Get URL from user
    url = input("\nEnter YouTube URL: ").strip()

    if not url:
        print("❌ No URL provided")
        return

    # Ask for download location
    output_dir = input("Enter output directory (press Enter for current directory): ").strip()
    if not output_dir:
        output_dir = "."

    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ask for format preference
    print("\nAudio format options:")
    print("1. Best quality MP3 (default)")
    print("2. Best quality M4A")
    print("3. Best quality OPUS")
    print("4. Best quality MP4 (Audio+Video)")
    print("5. Original format (no conversion)")
    print("6. List all available formats")

    choice = input("Choose option (1-5, default 1): ").strip()

    if choice == "5":
        list_available_formats(url)
        return

    # Configure postprocessor based on choice
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
    }

    if choice in ["1", "2", "3", ""]:
        # Set preferred codec
        codec_map = {
            "1": "mp3",
            "2": "m4a",
            "3": "opus",
            "": "mp3"
        }

        codec = codec_map.get(choice, "mp3")

        download_youtube_audio(url, output_dir, codec)

        print(f"\nDownloading best audio as {codec.upper()}...")

    elif choice == "4":
        download_youtube_video(url, output_dir)
        print("\nDownloading original audio+video format...")

    elif choice == "5":
        ydl_opts['format'] = 'bestaudio'
        print("\nDownloading original audio format...")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                print(f"\n✅ Success! Saved: {info.get('title', 'Unknown')}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    elif choice == "6":
        list_available_formats(url)


if __name__ == "__main__":
    # Simple single URL usage
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        download_youtube_audio(url, output_dir)
    else:
        # Interactive mode
        main()
