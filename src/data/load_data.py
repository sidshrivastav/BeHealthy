from get_data import get_data, read_params
import argparse
import pandas as pd

ROOT_DIR = "D:\Project\BeHealthy"


def load_and_save(config_path):
    config = read_params(config_path)
    train_sentences, train_labels, test_sentences, test_labels = get_data(config_path)
    train_data = pd.DataFrame(
        {'sentences': train_sentences,
         'label': train_labels
         })
    test_data = pd.DataFrame(
        {'sentences': test_sentences,
         'label': test_labels
         })
    train_data_path = config["load_data"]["train_path"]
    test_data_path = config["load_data"]["test_path"]
    train_data.to_csv(ROOT_DIR + train_data_path, index=False)
    test_data.to_csv(ROOT_DIR + test_data_path, index=False)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=ROOT_DIR + "\config\params.yaml")
    parsed_args = args.parse_args()
    load_and_save(parsed_args.config)
