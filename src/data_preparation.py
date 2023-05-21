import os
import argparse
import yaml
import logging


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def main(config_path, datasource):
    config = read_params(config_path)
    print(config)


def process_file(filename):
  input_file = open(filename, 'r')
  file_content = input_file.readlines()
  input_file.close()

  out_lines = [] #To store list of sequences (sentences or labels)

  line_content = ""

  for word in file_content:
    word = word.strip()
    if word == "": # If empty line, add the current sequence to out_lines
      out_lines.append(line_content)
      line_content = ""; # re-initialize
    else:
      if line_content: #if non-empty, add new word after space
        line_content += " "+word
      else:
        line_content = word # first word, no space required

  return out_lines


def get_data(config_path):
    config = read_params(config_path)

    print(config)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    default_config_path = os.path.join("config", "params.yaml")
    # args.add_argument("--config", default=default_config_path)
    # args.add_argument("--datasource", default=None)

    parsed_args = args.parse_args()
    get_data(parsed_args.config)
    # main(config_path=parsed_args.config, datasource=parsed_args.datasource)

