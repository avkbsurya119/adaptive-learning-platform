# Architecture Overview

This document outlines the modular architecture of the Adaptive Learning Platform.

## Core Modules

### 1. Search (Trie)
- Fast autocomplete for course/sequence titles.
- Stored in `core/search/trie.py`.

### 2. Graph (CourseGraph)
- Directed acyclic graph (DAG) of courses.
- Tracks prerequisites.
- Topological sorting.
- Content association.

### 3. Scheduling (Priority Queue)
- Stable heap-based sequence scheduler.
- Controls sequence execution order.

### 4. Students & History
- Students tracked via dataclasses.
- History system uses array indexing + log entries.

### 5. Recommendations
- Deterministic scoring based on difficulty, progress gap, and recency.
- Ranking performed via sorted list.

### 6. Persistence
- JSON save/load for students and courses.
