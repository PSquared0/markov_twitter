import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    char_count = len(key[0]) + len(key[1])
    print char_count

    while key in chains:
        word = choice(chains[key])
        char_count_check = char_count + len(word)
        if char_count_check > 110:
            break
        else:
            words.append(word)
            key = (key[1], word)
            char_count = char_count + len(word)
        
    print char_count
    return " ".join(words)
   


def tweet(chains):

    api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

   

    user_input = None
    while user_input != "q":
        print api.VerifyCredentials()

        status = api.PostUpdate(make_text(chains) + "#hbgracefall16")

        print status.text
        
        user_input = raw_input("Enter to tweet again [q to quit] >")
        



# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

tweet(chains)

# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)
