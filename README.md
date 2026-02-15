# ZUNO

ZUNO is a scalable social media platform built for college students and local creators to connect, share content, and grow within their nearby community. The platform focuses on simplicity, real engagement, and early creator monetization without algorithm manipulation.

---

## 🚀 Overview

ZUNO enables users to create an identity, share posts, interact with others, and build a local audience. The system is designed with a scalable architecture so it can grow from a small user base to a large production platform.

---

## ✨ Core Features

* Secure user authentication (username/email + password)
* Public and followers-only posts
* Image and short video sharing
* City-based discovery feed (Nearby + Latest)
* Follow / Unfollow system
* Likes and comments
* Real-time chat (1–1 messaging)
* Notifications
* Report & moderation system
* Hybrid verification (Earned or Paid)
* Early monetization eligibility

---

## 🧠 Monetization Model

Creators become eligible for monetization after meeting:

* 50+ Posts
* 100+ Followers
* 1000+ Total Reach

Users can:

* Earn verification for free
* OR buy verification early

Verification unlocks monetization features and creator privileges.

---

## 🏗️ Tech Stack

**Backend**

* Python (Flask)
* REST APIs
* JWT Authentication
* Modular architecture

**Database**

* MySQL / PostgreSQL (production-ready design)
* Redis (caching, sessions, realtime)

**Frontend**

* Flutter (cross-platform mobile app)

**Media**

* Cloud storage ready (AWS S3 / Cloudflare R2)

---

## 📁 Project Structure

```
zuno/
├─ backend/        # Flask backend (APIs, logic, database)
├─ frontend/       # Flutter mobile app
├─ docs/           # Design & architecture notes
├─ scripts/        # Setup & utility scripts
└─ README.md
```

---

## 🔐 Security Principles

* Passwords are hashed (never stored in plain text)
* JWT-based authentication
* Role-based admin control
* Input validation on all APIs
* Visibility and ownership enforced server-side
* Soft deletes for sensitive data

---

## ⚙️ Development Status

Current Version: **V1 (Core Platform)**

Implemented:

* Authentication
* Basic post system
* Feed (latest)
* Scalable backend structure

Planned:

* Follow graph
* City-based feed
* Chat system
* Notifications
* Verification & monetization
* Media optimization
* Scaling & performance

---

## 🎯 Vision

ZUNO aims to build a fast, simple, and scalable social platform where users grow through authenticity, consistency, and real engagement — not artificial algorithms.

---

## 📌 Note

This project is under active development. Architecture is designed for scalability, maintainability, and real-world deployment.

---
