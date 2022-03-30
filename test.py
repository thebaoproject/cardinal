from wiktionaryparser import WiktionaryParser

if __name__ == '__main__':
    wp = WiktionaryParser()
    word = wp.fetch("dictionary")
    print(word)
