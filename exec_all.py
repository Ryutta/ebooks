"""スクショして一つのPDFにして保存する"""
import argparse
import os

from screenshot import decide_capture_region, capture_screen
from image2pdf import image_to_pdf


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_page', help='開始ページ', type=int, required=True)
    parser.add_argument('-e', '--end_page', help='終了ページ', type=int, required=True)
    parser.add_argument('-o', '--output_dir', help='出力ディレクトリ', default='.')
    parser.add_argument('-c', '--chapter_name', help='章などの名前')

    return parser.parse_args()


def _main():
    args = _parse_args()

    start_page = args.start_page
    end_page = args.end_page
    output_dir = args.output_dir
    chapter_name = args.chapter_name

    image_dir = output_dir + "/image"
    pdf_dir = output_dir + "/pdf"
    for dir in [output_dir, image_dir, pdf_dir]:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    # スクショする範囲を指定します
    # region = (左上のx座標, 左上のy座標, スクショの横幅, スクショの縦幅)
    region = decide_capture_region()

    capture_screen(start_page, end_page, output_dir, chapter_name, region)
    image_to_pdf(start_page, end_page, output_dir, chapter_name)

    print("全ての工程が完了しました")


if __name__ == "__main__":
    _main()
