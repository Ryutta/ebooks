import argparse
import os

from fpdf import FPDF, Align

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_page', help='開始ページ', type=int, required=True)
    parser.add_argument('-e', '--end_page', help='終了ページ', type=int, required=True)
    parser.add_argument('-o', '--output_dir', help='出力ディレクトリ', default='.')
    parser.add_argument('-c', '--chapter_name', help='章などの名前')

    return parser.parse_args()


def generate_image_path(
    output_dir: str,
    page: int,
    chapter_name: str,
) -> str:
    """
    保存する画像のパスを生成します。

    Args:
        output_dir (str): 出力ディレクトリのルートパス。
        page (int): ページ番号。
        chapter_name (str): 章の名前（ファイル名に使用）。

    Returns:
        str: 画像ファイルのフルパス。
    """
    if chapter_name:
        return f"{output_dir}/image/{chapter_name}_{page}.png"
    return f"{output_dir}/image/{page}.png"


def _generate_pdf_path(
    output_dir: str,
    start_page: int,
    end_page: int,
    chapter_name: str,
) -> str:
    """
    保存するPDFのパスを生成します。

    Args:
        output_dir (str): 出力ディレクトリのルートパス。
        start_page (int): 開始ページ番号。
        end_page (int): 終了ページ番号。
        chapter_name (str): 章の名前（ファイル名に使用）。

    Returns:
        str: PDFファイルのフルパス。
    """
    if chapter_name:
        return f"{output_dir}/pdf/{chapter_name}_{start_page}_{end_page}.pdf"
    return f"{output_dir}/pdf/{start_page}_{end_page}.pdf"


def image_to_pdf(
    start_page: int,
    end_page: int,
    output_dir: str,
    chapter_name: str,
) -> None:
    """
    複数の画像を1つのPDFとして保存します。
    ※この機能は `fpdf2` ライブラリを使用しています。

    Args:
        start_page (int): 開始ページ番号。
        end_page (int): 終了ページ番号。
        output_dir (str): 画像のディレクトリ。
        chapter_name (str): 章の名前。
    """
    print("画像をPDFに変換します")
    pdf = FPDF()
    pdf.set_auto_page_break(False)

    for page in range(start_page, end_page+1):
        image = generate_image_path(output_dir, page, chapter_name)
        if not os.path.exists(image):
            print(f"警告: 画像が見つかりません: {image}")
            continue

        pdf.add_page()
        # 画像を中央に配置。w=pdf.epw でページ幅いっぱいにすることも可能。
        # Align.C は fpdf2 でサポートされています。
        try:
            pdf.image(image, x=Align.C)
        except Exception as e:
            print(f"画像追加エラー: {e}")
            continue

        print(f"{image} を追加しました")

    pdf_path = _generate_pdf_path(output_dir, start_page, end_page, chapter_name)
    try:
        pdf.output(pdf_path)
        print(f"PDFを {pdf_path} に保存しました")
    except Exception as e:
        print(f"PDF保存エラー: {e}")


def _main():
    args = _parse_args()

    start_page = args.start_page
    end_page = args.end_page
    output_dir = args.output_dir
    chapter_name = args.chapter_name

    pdf_dir = os.path.join(output_dir, "pdf")
    for dir_path in [output_dir, pdf_dir]:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    image_to_pdf(start_page, end_page, output_dir, chapter_name)


if __name__ == "__main__":
    _main()
