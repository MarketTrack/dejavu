import dejavu.fingerprint as fingerprint
import dejavu.decoder as decoder
import time

class BaseRecognizer(object):
    def __init__(self, dejavu):
        self.dejavu = dejavu
        self.Fs = None

    def _recognize(self, *data):
        matches = []
        for d in data:
            matches.extend(self.dejavu.find_matches(d, Fs=self.Fs))
        return self.dejavu.align_matches(matches, self.Fs)

    def _recognize_multiple(self, maxMatches, minConfidence, *data):
        matches = []
        for d in data:
            matches.extend(self.dejavu.find_matches(d, Fs=self.Fs))

        songs = []
        for _ in range(maxMatches):
            songMatch = self.dejavu.align_matches(matches, self.Fs)
            if songMatch is None or int(songMatch['confidence']) < minConfidence:
                break
            songs.append(songMatch)
            matches = [m for m in matches if m[0] != songMatch['song_id']]

        return songs

    def recognize(self):
        pass  # base class does nothing

class StreamRecognizer(BaseRecognizer):
    def __init__(self, dejavu):
        super(StreamRecognizer, self).__init__(dejavu)

    def recognize_stream(self, channels, samplerate, maxMatches, minConfidence):
        self.Fs = samplerate

        t = time.time()
        matches = {}
        matches['results'] = self._recognize_multiple(maxMatches, minConfidence, *channels)
        t = time.time() - t
        matches['match_time'] = t

        return matches

    def recognize(self, channels, samplerate, maxMatches=1, minConfidence=0):
        return self.recognize_stream(channels, samplerate, maxMatches, minConfidence)
