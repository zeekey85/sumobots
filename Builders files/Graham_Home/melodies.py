# Note frequencies in Hertz
note_frequencies = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,
    "C5": 523.25,
    "A5": 880.00,
    "P": 0,  # Pause
}

# Duration of each note in seconds
note_durations = {
    "quarter": 0.5,  # 500 milliseconds
    "eighth": 0.25,  # 250 milliseconds
    "half": 1.0,  # 1000 milliseconds or 1 second
}

# Melody for the robot startup
robot_startup_melody = [
    ("C4", "quarter"),
    ("P", "eighth"),
    ("C4", "quarter"),
    ("P", "eighth"),
    ("C4", "quarter"),
    ("P", "eighth"),
    ("C5", "half"),
]


def note_values(note, duration):
    return note_frequencies[note], note_durations[duration]
