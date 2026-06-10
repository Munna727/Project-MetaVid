[README.md](https://github.com/user-attachments/files/28780142/README.md)
<div align="center">

# 🎬 MetaVid
### Intelligent Video Analysis Platform

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)](https://cloudinary.com)

*Transform raw video content into structured, actionable intelligence using AI and cloud technologies.*

</div>

---

## 📌 Overview

**MetaVid** is an AI-powered video analysis platform that automatically extracts meaningful insights from uploaded videos. The system combines computer vision techniques with cloud-based video intelligence services to identify important visual elements and events within a video.

The platform helps users analyze video content efficiently by detecting scene transitions, faces, logos, and objects — transforming raw video data into structured, actionable information.

---

## ✨ Features

### 🎞️ Shot Change Detection
Detects scene transitions and shot boundaries within a video, helping users understand video structure and navigate content efficiently.

### 👤 Face Detection
Identifies human faces appearing in the video and provides information about their occurrence throughout the footage.

### 🏷️ Logo Detection
Recognizes brand logos present in video frames — useful for marketing analysis, sponsorship tracking, and brand monitoring.

### 📦 Object Detection
Detects and classifies various objects appearing in the video, enabling deeper content understanding and categorization.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Core backend language |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) | Web framework |
| ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white) | Video frame processing |
| ![Google Cloud](https://img.shields.io/badge/Google_Video_Intelligence-4285F4?style=flat&logo=google-cloud&logoColor=white) | AI video analysis |
| ![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=flat&logo=cloudinary&logoColor=white) | Cloud video storage & management |
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | Frontend interface |

---

## ⚙️ System Workflow

```
User Uploads Video
       │
       ▼
┌─────────────────┐
│   Cloudinary    │  ← Secure video upload & management
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Google Video Intelligence   │  ← AI-powered content analysis
└────────────┬────────────────┘
             │
             ▼
┌─────────────────┐
│    OpenCV       │  ← Frame-level processing
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│         Detection & Extraction               │
│  Shot Changes │ Faces │ Logos │ Objects      │
└────────────────────────┬─────────────────────┘
                         │
                         ▼
             Interactive Results Dashboard
```

1. **Upload** — User uploads a video through the web interface.
2. **Store** — The video is processed and securely managed using Cloudinary.
3. **Analyze** — Google Video Intelligence API analyzes the video content.
4. **Process** — OpenCV performs additional video frame processing.
5. **Extract** — Detection results are extracted and organized.
6. **Interpret** — The platform generates meaningful insights from the analyzed video.
7. **Display** — Results are shown to the user through an interactive dashboard.

---

## 💡 Applications

| Domain | Use Case |
|---|---|
| 📺 Media & Broadcasting | Video content analysis & monitoring |
| 📣 Marketing | Brand visibility tracking & sponsorship analytics |
| 📚 Education | Educational video analysis & indexing |
| 🗂️ Content Management | Automated tagging and categorization |
| 🔬 Research | Computer vision & video intelligence projects |
| 📊 Digital Marketing | Campaign performance analytics |

---

## ⚠️ Challenges Faced

- 🔍 Selecting the most suitable cloud service for large-scale video processing.
- 🔄 Designing an efficient workflow for handling video uploads and analysis.
- 🎯 Improving the accuracy and relevance of generated analysis results.
- 🔗 Integrating multiple services while maintaining smooth application performance.

---

## 🚀 Future Enhancements

- [ ] 📝 Video summarization
- [ ] 😊 Emotion detection
- [ ] 🎙️ Speech-to-text transcription
- [ ] 🔑 Keyword extraction
- [ ] 🌐 Multi-language support
- [ ] ⚡ Real-time video analytics
- [ ] 📊 Advanced reporting dashboard

---

## 👨‍💻 Author

> Developed as a computer vision and video intelligence project focused on transforming raw video content into meaningful insights using AI and cloud technologies.

---

<div align="center">

Made with ❤️ using
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=flat&logo=cloudinary&logoColor=white)](https://cloudinary.com)

</div>
