# Real-Time Face Detection Video Streaming System

A production-ready, containerized backend API that ingests video feeds, processes frames in real-time to detect faces, draws bounding boxes, stores Region of Interest (ROI) data into PostgreSQL, and streams the processed video back to clients via MJPEG.

## 🏗 Architecture & Flow

The system is strictly organized with modular separation of concerns.

```mermaid
graph TD
    Client[Client Browser] -->|POST /ingest| Router[FastAPI Router]
    Client -->|GET /stream| Router
    Client -->|GET /roi| Router
    
    Router -->|Save File| VideoSvc[Video Service]
    Router -->|Generate MJPEG| StreamSvc[Streaming Service]
    Router -->|Fetch Data| ROISvc[ROI Service]
    
    StreamSvc -->|Iterate Frames| Processor[Video Processor]
    
    Processor -->|Extract| ImageIO[ImageIO/FFmpeg]
    Processor -->|Detect Face| MediaPipe[MediaPipe Tasks API]
    Processor -->|Draw Box| Pillow[Pillow / PIL]
    Processor -->|Save Box| ROISvc
    
    ROISvc -->|Persist| DB[(PostgreSQL)]
```

### 🧠 Design Decisions
1. **MediaPipe over OpenCV:** Dropped OpenCV entirely for face detection to use Google's highly efficient `mediapipe.tasks.vision` API (blaze_face_short_range). It is significantly faster and natively extracts absolute coordinates.
2. **Video Frame Extraction:** Used `imageio` with the `ffmpeg` plugin to extract frames purely as numpy arrays. This prevents loading full videos into memory and maintains OpenCV-free boundaries.
3. **Pillow for Drawing:** Kept OpenCV completely out of the codebase by utilizing `PIL.ImageDraw` to render bounding boxes natively.
4. **Threadpool MJPEG Streaming:** Video processing uses a synchronous generator. FastAPI's `StreamingResponse` smartly maps synchronous generators to a background Starlette threadpool so CPU-bound Face Detection doesn't block the async event loop.
5. **Real-time DB Syncing:** SQLAlchemy instantly syncs parsed bounding box coordinates (x, y, width, height) to Postgres during the streaming generator iteration.

## 🚀 Setup Instructions (Docker - Recommended)

The quickest way to run the entire backend + database is using Docker Compose.

1. Ensure Docker Desktop is running.
2. Build and start the containers from the project root:
   ```bash
   docker-compose up --build
   ```
3. Open your browser to test the full pipeline using the minimal frontend:
   [http://localhost:8000/](http://localhost:8000/)

## 💻 Setup Instructions (Local Development)

If you wish to run without Docker, ensure you have a running PostgreSQL database.

1. Update your `.env` or `app/core/config.py` `DATABASE_URL` to match your Postgres setup.
   ```text
   DATABASE_URL="postgresql://postgres:password@localhost:5432/facedb"
   ```
2. Navigate to the backend directory and set up a Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI development server:
   ```bash
   python app/main.py
   ```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves a minimal HTML frontend that tests the entire pipeline. |
| `GET` | `/api/v1/health` | Service health check. |
| `POST` | `/api/v1/ingest` | Upload a video file (`.mp4`, `.avi`) as `multipart/form-data`. Returns the filename to use for streaming. |
| `GET` | `/api/v1/stream?filename=video.mp4` | Retrieves and streams the requested video in real-time using MJPEG (`multipart/x-mixed-replace`). |
| `GET` | `/api/v1/roi?limit=10` | Returns the latest bounding box coordinates (`x, y, width, height`) tracked in PostgreSQL. |
