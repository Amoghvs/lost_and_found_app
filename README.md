## Description

Lost & Found App built with FastAPI, designed to help users report, and recover lost or found items in public spaces. The app includes features for item reporting, smart matching, photo uploads, user comments, and audit logging.

## Features
📦 Report Lost or Found Items – Users can create posts with descriptions, images, locations, and timestamps.

🔍 Matching Engine – The backend supports logic to detect and suggest possible matches between lost and found reports.

🖼️ Photo Uploads – Users can attach photos to enhance identification.


## Tech Stack
Backend: FastAPI

ORM: SQLAlchemy

Validation: Pydantic

Database: PostgreSQL (or SQLite for development)

Containerization: Docker

File Storage: minIO