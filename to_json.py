import json
from requests.sessions import PreparedRequest
import scipdf
import argparse
import os
from functools import partial


def pdf_to_json(in_filepath: str, out_filepath: str):
    dictionary = scipdf.parse_pdf_to_dict(in_filepath)
    with open(out_filepath, 'w') as fp:
        json.dump(dictionary, fp)


parser = argparse.ArgumentParser()
parser.add_argument('--source_dir', required=True)
parser.add_argument('--destination_dir', required=True)
args = parser.parse_args()

source_dir_files = os.listdir(args.source_dir)


def is_pdf(filepath):
    _, extension = os.path.splitext(filepath)
    return extension.lower() == '.pdf'


source_dir_files = list(filter(is_pdf, source_dir_files))
prepend_source_dir_path = partial(os.path.join, args.source_dir)
source_filepaths = map(prepend_source_dir_path, source_dir_files)


def build_out_path(filename): return os.path.join(
    args.destination_dir, filename) + '.json'


destination_filepaths = map(build_out_path, source_dir_files)

for source_path, destination_path in zip(source_filepaths, destination_filepaths):
    print('-'*50)
    print(source_path)
    print(destination_path)
    pdf_to_json(source_path, destination_path)
