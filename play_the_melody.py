import winsound


class MelodyGame:

    def __init__(self, difficulty):
        self.notes = {
            "C": 261.6,
            "D": 293.7,
            "E": 329.6,
            "F": 349.2,
            "G": 392.0,
            "A": 440.0,
            "B": 493.9}
        self.melodies = {
            "Seven Nation Army": [
                ("E", 2000), ("E", 1000), ("G", 1000), ("E", 1000), ("D", 1000), ("C", 1000)]}

    def play_melody(self):
        for note in self.melodies["Seven Nation Army"]:
            winsound.Beep(self.notes[note[0]], note[1])
