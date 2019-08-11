import os

from importlib import import_module

from ..insight import Insight

from .collector import Collector
from .meta_regressor import MetaRegressor
from .recognizer import Recognizer
from .predictor import Predictor


class MetaLearn:
    def __init__(self, search_config, metric="accuracy", cv=5):
        self.search_config = search_config
        self.metric = metric
        self.cv = cv

        current_path = os.path.realpath(__file__)
        meta_learn_path, _ = current_path.rsplit("/", 1)

        meta_data_path = meta_learn_path + "/meta_data/"
        meta_regressor_path = meta_learn_path + "/meta_regressor/"

        self.model_list = list(self.search_config.keys())
        self.n_models = len(self.model_list)

        self.insight = Insight()

        self.memory = Collector(self.search_config, meta_data_path=meta_data_path, cv=3)
        self.meta_regressor = MetaRegressor(meta_learn_path)
        self.recognizer = Recognizer(search_config)
        self.predictor = Predictor(search_config, meta_regressor_path)

        self.model_list = list(self.search_config.keys())

    def collect(self, X, y):
        dataset_str = self.insight.recognize_data(X, y)
        self.memory.extract(X, y, dataset_str)

    def train(self, model_list):
        self.meta_regressor.train_meta_regressor(model_list)

    def search(self, dataset_config):
        X_test = self.recognizer.get_test_metadata(dataset_config)

        self.best_hyperpara_dict, self.best_score = self.predictor.search(X_test)