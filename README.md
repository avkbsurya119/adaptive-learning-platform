# Adaptive Learning Platform (DSA Project)

![Build Status](https://github.com/avkbsurya119/adaptive-learning-platform/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Ruff](https://img.shields.io/badge/ruff-checked-brightgreen)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)

A modular, test-driven **Adaptive Learning Platform** built using classical **Data Structures & Algorithms (DSA)**.  
The system simulates how a real-world intelligent learning platform works—using data structures like Trie, Graph, Priority Queue, Array, and HashMap to power search, sequencing, history, and recommendations.

This project demonstrates clean architecture, modern Python practices, and full automated testing suitable for academic submission and professional portfolios.

---

## 📚 Features at a Glance

### 🔍 Trie-Based Content Search
Fast prefix-based search for:
- Course titles  
- Sequence titles  

Used for autocomplete and content discovery.

### 🔗 Graph-Based Course Prerequisites
Courses and their prerequisites are stored as a **Directed Acyclic Graph (DAG)**:
- Add courses  
- Add prerequisites  
- Retrieve direct and indirect prerequisites  
- Perform topological sorting  

### 🧵 Priority Sequence Scheduler
Sequences are scheduled using a **min-heap** priority queue:
- Lower priority = executed earlier  
- Stable ordering (FIFO for equal priority)  
- Students progress step-by-step  

### 📜 Student History (Array-Backed)
Logs activities using:
- Array indexes  
- Activity objects  

Tracks:
- Completed sequences  
- Quiz scores  
- Timestamps  

### 🎯 Deterministic Recommendation Engine
Ranks the next best courses using:
- Difficulty alignment  
- Progress gap  
- Recency of learning  

Provides **explanation strings** for transparency.

### 💻 CLI Demo
A full menu-driven CLI to interact with the system:
- Register students  
- Search content  
- Enroll in a course  
- Complete sequences  
- View history  
- Generate recommendations  

---

## 🧠 DSA Concepts Used

| Feature | Data Structure | File |
|--------|----------------|------|
| Content Search | Trie | `core/search/trie.py` |
| Course Prerequisites | Directed Graph | `core/graph/course_graph.py` |
| Sequence Scheduling | Min-Heap | `core/scheduling/sequence_scheduler.py` |
| Student Registry | HashMap (Dict) | `core/models/student.py` |
| Activity History | Array | `core/history/history.py` |
| Recommendations | Weighted Scoring + Sorting | `core/recommendations/recommendation_engine.py` |

---

## 🗂️ Project Structure



```text
adaptive-learning-platform/
├─ core/
│  ├─ models/
│  │  ├─ course.py
│  │  ├─ sequence.py
│  │  ├─ student.py
│  │  ├─ activity.py
│  │  └─ recommendation.py
│  ├─ search/
│  │  └─ trie.py
│  ├─ graph/
│  │  └─ course_graph.py
│  ├─ scheduling/
│  │  └─ sequence_scheduler.py
│  ├─ history/
│  │  └─ history.py
│  ├─ students/
│  │  └─ student_service.py 
│  ├─ recommendations/
│  │  └─ recommendation_engine.py
│  ├─ persistence/
│  │  └─ storage.py
│  ├─ config.py           
│  └─ logging_config.py      
├─ cli/
│  └─ cli.py
├─ tests/
│  ├─ test_trie.py
│  ├─ test_course_graph.py
│  ├─ test_sequence_scheduler.py
│  ├─ test_student_history.py
│  ├─ test_students.py
│  ├─ test_recommendations.py
│  ├─ test_storage.py
│  └─ test_integration_flow.py
├─ docs/
│  ├─ architecture.md     
│  └─ api_examples.md         
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ README.md
├─ CONTRIBUTING.md
├─ LICENSE
├─ requirements.txt
├─ pytest.ini
├─ .pre-commit-config.yaml     # (optional)
└─ .gitignore
