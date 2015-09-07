import random
from datetime import datetime
import redis


class ABExperiment(object):

    """Initiates an A/B test experiment

        Parameters:

        user:
            A representation of user

    """

    def __init__(self, host='localhost', port=6379):
        self._r = redis.StrictRedis(host=host, port=port)

    def ab_test(self, name, user, control_value, treatment_value):
        """Create an A/B test
        """
        self._name = name
        self._control_value = control_value
        self._treatment_value = treatment_value

        # start an test, by choosing uniformly among control_value and
        # treatment_value
        choice = random.randrange(0, 2)
        if choice:
            value = treatment_value
        else:
            value = control_value

        # log the data to redis
        data = (',').join([name, str(user), str(value), str(datetime.now())])
        self._r.rpush('experiments', data)

        return value

    def finished(self, name, user, value):
        # log finished conversion to redis
        data = (',').join([name, str(user), str(datetime.now()), value])
        self._r.rpush('finished_exp', data)
