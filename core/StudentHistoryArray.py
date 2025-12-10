from datetime import datetime
import array

class Activity:
    def __init__(self, activity_type, timestamp, score=None, metadata=None):
        self.activity_type = activity_type
        self.timestamp = timestamp
        self.score = score
        self.metadata = metadata

    def __repr__(self):
        return (f"Activity(type={self.activity_type}, timestamp={self.timestamp},"
                f" score={self.score}, metadata={self.metadata})")


class StudentHistoryArray:
    def __init__(self):
        self.history_index = array.array('I')
        self.activities = []

    def append_activity(self, activity_type, timestamp, score=None, metadata=None):
        activity = Activity(activity_type, timestamp, score, metadata)
        self.history_index.append(len(self.activities))
        self.activities.append(activity)

    def iterate_activities(self):
        for i in self.history_index:
            yield self.activities[i]

    def __iter__(self):
        return iter(self.activities)
