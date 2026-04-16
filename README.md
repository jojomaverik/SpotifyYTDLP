# 🎧 Spotify → YouTube Downloader (SpotifyYTDLP)

A Python-based tool that allows you to:

1. Import songs from a Spotify playlist
2. Store them in a local database
3. Automatically find matching YouTube audio
4. Download songs as MP3 or FLAC

## ⚠️ Disclaimer

This project is intended **for educational and personal use only**.

* Downloading content from YouTube may violate YouTube’s Terms of Service.
* You are responsible for how you use this tool.
* Do **not** distribute copyrighted material downloaded using this tool.
* Always support artists by purchasing or streaming music through official platforms.

---

## 📦 Requirements

* Python 3.9+
* FFmpeg (required for audio conversion)
* Spotify Developer credentials

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/jojomaverik/SpotifyYTDLP.git
cd SpotifyYTDLP
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

Download and install FFmpeg:
👉 https://ffmpeg.org/download.html

Make sure it is added to your system PATH.

---

## 🔑 Setup Spotify API

1. Go to: https://developer.spotify.com/dashboard
2. Create an app
3. Copy your credentials

Create a `.env` file in the project root:

```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🖥️ CLI Usage

After running, you will see:

```
s - search songs
g - print all songs in the database
c - clear database
p - import songs from a Spotify playlist URL
y - find YouTube URLs for songs in database
m - show songs still missing YouTube URLs
d - download songs that already have YouTube URLs
r - show songs waiting to be downloaded
q - quit
```

---

## 🔄 Typical Workflow

### 1. Import playlist

```
p
```

Paste a Spotify playlist URL.

---

### 2. Match YouTube URLs

```
y
```

---

### 3. Download songs

```
d
```

Choose format: `mp3` or `flac`

---

### 4. Check results

```
g
```

---

## 📁 Output

Downloaded files are saved in:

```
/downloads
```

Example:

```
downloads/
  Artist - Song.mp3
```

---

## 🗄️ Database

* Uses SQLite (`songs.db`)
* Tracks:

  * title
  * artist
  * album
  * spotify_id
  * youtube_url
  * downloaded status
  * file path

---

## 🧠 Future Improvements

* Duplicate protection
* One-command full sync
* Better YouTube matching
* Web interface (FastAPI + frontend)

---

## 🙌 Contributions

This project is currently for learning purposes, but improvements are welcome.

---

## ⭐ Support Artists

If you like the music you download, please:

* Buy the tracks
* Stream from official platforms
* Support the creators

---
