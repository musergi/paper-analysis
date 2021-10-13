import os
import json
from functools import partial
import argparse
import pandas
import pandas as pd


class Paper:
    def __init__(self, title: str, authors: list, abstract: str, references: list):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.references = references

    def is_valid(self) -> bool:
        return bool(self.title) and len(self.authors) > 0

    @staticmethod
    def from_json(filepath: str):
        with open(filepath, 'r') as fp:
            json_dict = json.load(fp)
        authors = json_dict['authors'].split('; ')
        authors = list(filter(bool, authors))  # Filter empty strings
        return Paper(
            json_dict['title'].lower().strip(),
            authors,
            json_dict['abstract'],
            json_dict['references']
        )

    def __eq__(self, other):
        if not self.title:
            raise ValueError('Missing title in operand 1 of ==')
        if not other.title:
            raise ValueError('Missing title in operand 2 of ==')
        return self.title == other.title and len(self.authors) == len(other.authors)

    def __repr__(self):
        return f'Paper({self.title}, {self.authors}, {len(self.references)})'


parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
args = parser.parse_args()

filenames = os.listdir(args.input)
paths = map(partial(os.path.join, args.input), filenames)

papers = []
for path in paths:
    papers.append(Paper.from_json(path))
papers = list(filter(lambda p: p.is_valid(), papers))
print(*papers, sep='\n')

# Create paper database
paper_df = []
for paper in papers:
    paper_dict = {
        'title': paper.title,
        'author_count': len(paper.authors),
        'reference_count': len(paper.references)
    }
    paper_df.append(paper_dict)
paper_df = pd.DataFrame(paper_df)
print(paper_df.head())

# Add paper referenced to database
reference_df = []
for paper in papers:
    referenced_papers = []
    for reference in paper.references:
        referenced_papers.append(Paper(
            title=reference['title'].lower().strip(),
            authors=reference['authors'].split('; '),
            abstract='',
            references=[]
        ))
    for r_paper in referenced_papers:
        origin = paper_df.loc[
            (paper_df.title == paper.title) & (paper_df.author_count == len(paper.authors))].index[0]
        matching_rows = paper_df.loc[
            (paper_df.title == r_paper.title) & (paper_df.author_count == len(r_paper.authors))]
        if len(matching_rows) > 1:
            raise ValueError('More than one paper matched for reference')
        if len(matching_rows) == 1:
            reference = {
                'origin': origin,
                'destination': matching_rows.index[0]
            }
            reference_df.append(reference)
        else:
            paper_dict = {
                'title': r_paper.title,
                'author_count': len(r_paper.authors),
                'reference_count': 0
            }
            paper_df = paper_df.append(paper_dict, ignore_index=True)
            reference = {
                'origin': origin,
                'destination': paper_df.iloc[-1].index[0]
            }
reference_df = pd.DataFrame(reference_df)
print(paper_df.head())
print(reference_df.head())
