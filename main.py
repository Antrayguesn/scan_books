import argparse
import scan_barecode
import requests

from get_plateform import is_raspberry

IS_RASPBERRY = is_raspberry()

if IS_RASPBERRY:
    import RPI_signal


def capture(dev_video, debug, show_capture):
    previous_barecode = None

    for frame in scan_barecode.read_from_video_capture(dev_video=dev_video, debug=debug, show_frame=show_capture):
        barecode = scan_barecode.detect_barecode(frame, debug=debug, show_frame=show_capture)
        # ISBN start wih 978 or 979 | avoid some miss detection
        if barecode and previous_barecode != barecode and barecode[:2] == "97":
            previous_barecode = barecode
            yield barecode


def get_book_data(booklyb_url: str, isbn: str) -> dict:
    try:
        ret = requests.get(f"{booklyb_url}/book_data/{isbn}")
        return ret.json()
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-c', '--capture-from-video', action='store_true', help='Activer le mode capture par video.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Active le mode verbeux.')
    parser.add_argument('-f', '--show-capture', action='store_true', default=False, help='Ouvre une fênetre avec la capture de la video.')

    parser.add_argument(
        '-b', "--booklyb-url",
        type=str,
        default="http://127.0.0.1:5000",
        help="URL du serveur de gestion de livre booklyb (par défaut: http://127.0.0.1:5000)"
    )

    parser.add_argument(
        '-d', "--device",
        type=str,
        default="0",
        help="Index ou chemin du device video (par défaut: 0, utilisé uniquement avec --capture-from-video)"
    )

    args = parser.parse_args()

    if args.capture_from_video:

        dev = args.device
        debug = args.verbose
        show_frame = args.show_capture

        url_booklyb = args.booklyb_url

        for barecode in capture(dev, debug, show_frame):
            if debug:
                print(barecode)
            if barecode:
                if IS_RASPBERRY:
                    RPI_signal.beep(True)
                book_data = get_book_data(url_booklyb, barecode)
                if IS_RASPBERRY:
                    RPI_signal.print_book(barecode, book_data.title)
            else:
                if is_raspberry():
                    RPI_signal.beep(False)


if __name__ == "__main__":
    main()
