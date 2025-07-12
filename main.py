import json
import argparse

import google_books_api_fetcher
import scan_barecode


def capture():
    try:
        with open('data.json', 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)
    except FileNotFoundError:
        donnees = {}
    previous_barecode = None

    debug = True
    show_frame = debug

    for frame in scan_barecode.read_from_video_capture(dev_video=2, debug=True, show_frame=True):
        barecode = scan_barecode.detect_barecode(frame, debug=debug, show_frame=show_frame)
        # ISBN start wih 978 or 979 | avoid some miss detection
        if previous_barecode != barecode and barecode is not None and barecode[0] == "97":
            previous_barecode = barecode
            print(barecode)

            if barecode in donnees:
                donnees[barecode]["nb_stock"] += 1
            else:
                donnees[barecode] = {"nb_stock": 1}

            with open('data.json', 'w', encoding='utf-8') as fichier:
                json.dump(donnees, fichier, indent=4, ensure_ascii=False)


def fetch():
    try:
        with open('data.json', 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)
    except FileNotFoundError:
        donnees = {}

    for isbn in donnees:
        if "book_info" not in donnees[isbn]:
            # Actually I use only Google Books API to fetch book information
            # If needed to fetch from more APIs use something loke :
            # https://github.com/Antrayguesn/search_place/blob/main/search_place/strategies/fetcher_strategy.py
            volume_info = google_books_api_fetcher.fetch_book_information_google(isbn)

            donnees[isbn]["book_info"] = volume_info

            with open('data.json', 'w', encoding='utf-8') as fichier:
                json.dump(donnees, fichier, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--capture-from-video', action='store_true', help='Activer le mode capture par video.')
    group.add_argument('--fetch', action='store_true', help='Activer le mode fetch.')

    args = parser.parse_args()

    if args.capture:
        capture()
    elif args.fetch:
        fetch()


if __name__ == "__main__":
    main()
