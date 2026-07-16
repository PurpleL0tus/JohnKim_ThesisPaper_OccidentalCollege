import json
import re


if __name__ == '__main__':
    with open('data.json', 'r') as f:
        data = json.load(f)

    print(f'loaded {len(data)} regexes')

    with open('corpus.txt', 'a') as corpus:
        for entry in data:
            regex = entry['regex']
            regex = re.sub(r'\s+', '', regex)
            regex = re.sub(r'\(\?#.*\)', '', regex)
            print(regex)
            corpus.write(f"{regex}    ")  # tsv
