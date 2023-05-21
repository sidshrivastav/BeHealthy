import os
import argparse
import yaml
import logging
import spacy

ROOT_DIR = "D:\Project\BeHealthy"
model = spacy.load("en_core_web_sm")


def read_params(config_path):
    print(config_path)
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def process_file(filename):
    input_file = open(filename, 'r')
    file_content = input_file.readlines()
    input_file.close()

    out_lines = []  # To store list of sequences (sentences or labels)

    line_content = ""

    for word in file_content:
        word = word.strip()
        if word == "":  # If empty line, add the current sequence to out_lines
            out_lines.append(line_content)
            line_content = "";  # re-initialize
        else:
            if line_content:  # if non-empty, add new word after space
                line_content += " " + word
            else:
                line_content = word  # first word, no space required

    return out_lines


def getFeaturesForOneWord(sentence, pos, pos_tags):
    word = sentence[pos]

    # Define 12 features with PoS tag as one of the features
    features = [
        'word.lower=' + word.lower(),  # serves as word id
        'word[-3:]=' + word[-3:],  # last three characters
        'word[-2:]=' + word[-2:],  # last two characters
        'word.isupper=%s' % word.isupper(),  # is the word in all uppercase
        'word.isdigit=%s' % word.isdigit(),  # is the word a number
        'word.startsWithCapital=%s' % word[0].isupper(),  # is the word starting with a capital letter
        'word.pos=' + pos_tags[pos]
    ]

    # Use the previous word also while defining features
    if (pos > 0):
        prev_word = sentence[pos - 1]
        features.extend([
            'prev_word.lower=' + prev_word.lower(),
            'prev_word.isupper=%s' % prev_word.isupper(),
            'prev_word.isdigit=%s' % prev_word.isdigit(),
            'prev_word.startsWithCapital=%s' % prev_word[0].isupper(),
            'prev_word.pos=' + pos_tags[pos - 1]
        ])
    # Mark the begining and the end words of a sentence correctly in the form of features.
    else:
        features.append('BEG')  # feature to track begin of sentence

    if (pos == len(sentence) - 1):
        features.append('END')  # feature to track end of sentence

    return features


# Define a function to get features for a sentence using the 'getFeaturesForOneWord' function.
def getFeaturesForOneSentence(sentence):
    processed_sentence = model(sentence)  # spacy is applied to sentence

    pos_tags = []  # correctly identify pos tags
    for token in processed_sentence:
        pos_tags.append(token.pos_)

    sentence_list = sentence.split()  # List of words in sentence

    # Correctly calling getFeaturesForOneWord defined above
    return [getFeaturesForOneWord(sentence_list, pos, pos_tags) for pos in range(len(sentence_list))]


# Define a function to get the labels for a sentence.
def getLabelsInListForOneSentence(labels):
    return labels.split()


def get_data(config_path):
    config = read_params(config_path)
    data_path = config["data_source"]["path"]
    file_path = "{}\\{}\\".format(ROOT_DIR, data_path)
    train_sentences = process_file(file_path + "train_sent.txt")
    train_labels = process_file(file_path + 'train_label.txt')
    test_sentences = process_file(file_path + 'test_sent.txt')
    test_labels = process_file(file_path + 'test_label.txt')

    return train_sentences, train_labels, test_sentences, test_labels

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=ROOT_DIR + "\config\params.yaml")
    parsed_args = args.parse_args()
    get_data(parsed_args.config)
