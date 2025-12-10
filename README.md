# Adaptive Learning Platform (DSA Project)
<!-- Badges -->
![Build Status](https://github.com/avkbsurya119/adaptive-learning-platform/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v1.json)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)

A Python-based **customised learning experience platform for adaptive education**, built as a Data Structures & Algorithms project.

It demonstrates how core ADTs can be combined to power a small “learning platform”:

- **Trie** – fast content search/autocomplete
- **Graph** – course prerequisites using a CourseGraph
- **Queue / Heap** – sequence scheduling with priorities
- **HashMap** – student registry (`dict` keyed by student id)
- **Array** – student activity history using an index + list
- **Recommendation system** – deterministic scoring using a heap-like ordering

This repo is designed to be:

- **Cleanly architected** – core logic separated from CLI
- **Tested** – pytest coverage for all core components
- **GitHub-ready** – CI workflow, clear structure, docs, and licensing

---

## 🔧 Features

- **Trie-based content search**
  - Insert course titles and sequence titles
  - Case-insensitive autocomplete for prefixes

- **CourseGraph with prerequisites**
  - Directed acyclic graph of courses
  - Maintains both:
    - `graph`: `prereq → [dependents]`
    - `reverse_graph`: `course → [prereqs]`
  - Topological sort (non-destructive)
  - Direct and transitive prerequisite queries

- **Sequence scheduler**
  - Schedules course sequences using a priority queue
  - Lower numeric priority = higher actual priority
  - Stable ordering (FIFO when priority is equal)

- **Student & history tracking**
  - Student profile with:
    - current course
    - completed sequences
    - progress counter
  - History backed by:
    - `array('I')` index
    - list of Activity objects
  - Logs sequence completions and quiz scores

- **Recommendation engine**
  - Deterministic scoring (no randomness)
  - Factors:
    - progress gap (how much is left to learn)
    - difficulty match
    - recency of activity
  - Returns ranked recommendations with human-readable explanations

- **CLI demo**
  - Register students
  - List courses and prerequisites
  - Search content
  - Enroll a student in a course
  - Complete sequences (scheduled)
  - View student history
  - Get course recommendations

---

## 📁 Project Structure

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
│  │  └─ student_service.py   # (optional / future extension)
│  ├─ recommendations/
│  │  └─ recommendation_engine.py
│  ├─ persistence/
│  │  └─ storage.py
│  ├─ config.py               # (optional / future extension)
│  └─ logging_config.py       # (optional / future extension)
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
│  ├─ 23cse203-data-structures-and-algorithm.pdf
│  ├─ architecture.md          # (optional / future extension)
│  └─ api_examples.md          # (optional / future extension)
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
