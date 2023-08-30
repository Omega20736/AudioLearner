class AudioSyncer:

    def __init__(self, left_bound, right_bound, window_size, sampling_rate, audio_path):
        self.live_feed_start = left_bound
        self.live_feed_end = left_bound + window_size

        self.ref_feed_start = left_bound
        self.ref_feed_end = left_bound + window_size

        self.window_size = window_size
        self.sampling_rate = sampling_rate
        self.audio_path = audio_path
        # Assuming the length of the reference feed can be inferred from the audio file.
        self.ref_feed_length = self._get_audio_length(audio_path)

    def _get_audio_length(self, audio_path):
        import librosa
        y, _ = librosa.load(audio_path, sr=self.sampling_rate)
        return len(y) / self.sampling_rate  # Length in seconds

    def adjust_boundaries(self, time_diff):
        # If the player is ahead (positive time difference)
        if time_diff > 0:
            self.ref_feed_end += time_diff  # expand the reference window

        # If the player is behind (negative time difference)
        elif time_diff < 0:
            self.ref_feed_end += time_diff  # reduce the reference window

        # Move the window boundaries for both live and reference feeds by window size
        self.live_feed_start += self.window_size
        self.live_feed_end += self.window_size
        self.ref_feed_start += self.window_size
        self.ref_feed_end += self.window_size

        # Bound checking
        if self.live_feed_end > self.ref_feed_length:
            self.live_feed_end = self.ref_feed_length

        if self.ref_feed_end > self.ref_feed_length:
            self.ref_feed_end = self.ref_feed_length

        return self.live_feed_start, self.live_feed_end, self.ref_feed_start, self.ref_feed_end

    # This method can be called each time there's a new time difference detected
    def sync(self, detected_time_diff):
        return self.adjust_boundaries(detected_time_diff)