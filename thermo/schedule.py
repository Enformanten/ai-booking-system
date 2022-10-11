import numpy as np


class Schedule:
    def __init__(
        self,
        schedule: np.ndarray,
        target_class: float,
        keep_warm: float,
    ):
        """
        School schedule
        Args:
            schedule (np.ndarray): matrix of 1hot encodings showing if there
                is a lecture at that hour in that room or not.
                Lectures are assumed to last 1h
                The first row should always be a row of 0s.

            target_class: target temperature during a lecture.
            keep_warm: target temperature if a lecture hall is to be kept warm.
        """
        self.schedule = schedule
        self.D = schedule.shape[1]
        self.target = target_class
        self.keep_warm = keep_warm

    def get_target(self, t):

        hour = int(t // 60)
        out = np.zeros(self.D)
        for i in range(self.D):
            if self.schedule[hour, i] == 1:
                out[i] = self.target
            elif (
                self.schedule[(hour + 1) :, i].sum() * self.schedule[:hour, i].sum() > 0
            ):
                out[i] = self.keep_warm

        return out
