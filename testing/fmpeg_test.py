import subprocess
FFMPEG_PATH = (
    r"C:\Users\Akshay\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
)

subprocess.run([FFMPEG_PATH, "-version"], check=True)
print("FFmpeg is working ✅")
