# yt-dlp rest server
A simple rest wrapper for yt-dlp, with which it is possible to get the media file directly in the http response.

## available routes and parameters

### download
- **route**: `/download`
- **method**: `GET`
- **parameters**:
  - `token` The token required for request authentication. If no token is provided on startup (env variable), a token will be generated automatically
  - `url`: URL of the video to download (Required)
  - `output_template` (Optional): The output template for the downloaded file's name. By default, it's `%(id)s.%(ext)s`
- **responses**:
  - `200`: If successful, the server will respond with the requested video file.
  - `400`: If the required url parameter is missing or not provided. 
  - `401`: If the provided token is invalid or missing for authentication.
  - `500`: If there is an issue with downloading or sending the file.

#### Example Request:
```plaintext
http://localhost:8080/download?url=VIDEO_URL&output_template=OUTPUT_TEMPLATE&token=TOKEN
```

## available configuration parameters
- **TOKEN**
  - (Optional) The token required for request authentication. If no token is provided on startup (env variable), a token will be generated automatically

## quick Start

### docker

```bash
docker run --rm \
    --publish 8080:5000 \
    --env TOKEN=CHANGE-ME \
    ghcr.io/eric-hess/yt-dlp-rest-server:latest
```
Now you can access the webpage via the following link: `http://localhost:8080`

### docker Compose
```yml
services:
    yt-dlp-rest-server:
        image: ghcr.io/eric-hess/yt-dlp-rest-server:latest
        restart: unless-stopped
        environment:
          - TOKEN=CHANGE-ME
        ports:
            - 8080:5000
```