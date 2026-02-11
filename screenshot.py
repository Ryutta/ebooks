import argparse
import os
from pathlib import Path
import time

try:
    import pyautogui as pag
except (ImportError, KeyError):
    # GUI環境がない場合などにエラーになる可能性がある
    pag = None

from image2pdf import generate_image_path

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_page', help='開始ページ', type=int, required=True)
    parser.add_argument('-e', '--end_page', help='終了ページ', type=int, required=True)
    parser.add_argument('-o', '--output_dir', help='出力ディレクトリ', default='.')
    parser.add_argument('-c', '--chapter_name', help='章などの名前')
    parser.add_argument('-k', '--key', help='ページ送りキー (right または left)', default='right', choices=['right', 'left'])

    return parser.parse_args()


def _get_cursor_position(
    wait_sec: int = 5
) -> tuple[int, int]:
    """
    指定秒数待機してから、現在のマウスカーソルの位置を取得します。

    Args:
        wait_sec (int): 待機する秒数（デフォルトは5秒）。

    Returns:
        tuple[int, int]: マウスカーソルの (x, y) 座標。
    """
    if pag is None:
        raise ImportError("pyautogui がインポートされていません。GUI環境で実行してください。")

    for sec in range(wait_sec, 0, -1):
        print(f"\r{sec} ", end="", flush=True)
        time.sleep(1)
    print("\r0 ", flush=True)  # カウントダウン終了
    print() # 改行
    return pag.position()


def decide_capture_region() -> tuple[int, int, int, int]:
    """
    ユーザーに対話的にスクリーンショットの範囲を指定させます。
    左上と右下の2点を指定することで、矩形範囲を決定します。

    Returns:
        tuple[int, int, int, int]: (左上のx座標, 左上のy座標, 横幅, 縦幅)
    """
    print("カーソルをスクショしたい範囲の左上角に合わせてください")
    x1, y1 = _get_cursor_position()
    print(f"左上の座標を({x1},{y1})にセットしました")

    print("カーソルをスクショしたい範囲の右下角に合わせてください")
    x2, y2 = _get_cursor_position()
    print(f"右下の座標を({x2},{y2})にセットしました")

    # 幅と高さを計算
    width = x2 - x1
    height = y2 - y1

    # 逆方向に指定された場合の補正
    if width < 0:
        x1 = x2
        width = -width
    if height < 0:
        y1 = y2
        height = -height

    return x1, y1, width, height


def capture_screen(
    start_page: int,
    end_page: int,
    output_dir: str,
    chapter_name: str,
    region: tuple[int, int, int, int],
    next_page_key: str = 'right',
) -> None:
    """
    指定された範囲のスクリーンショットを指定ページ数分撮影し、保存します。
    撮影ごとに 'right' キー（右矢印）を押してページ送りを行います。

    Args:
        start_page (int): 開始ページ番号。
        end_page (int): 終了ページ番号。
        output_dir (str): 画像の保存先ディレクトリ。
        chapter_name (str): 章の名前（ファイル名に使用）。
        region (tuple[int, int, int, int]): スクリーンショットの範囲 (x, y, width, height)。
        next_page_key (str): 次のページへ進むキー（'right' or 'left'）。
    """
    shot_span = 2  # 撮影間隔（秒）

    print(f"キャプチャ範囲: {region}")

    # スクリーンの移動
    print("撮影したいウィンドウを選択してください（5秒後に開始します）")
    for sec in range(5, 0, -1):
        print(f"\r{sec} ", end="", flush=True)
        time.sleep(1)
    print("\r0 ", flush=True)
    print()

    # 実行
    print("撮影を始めます")

    # 画像保存パス取得のため、image2pdf.generate_image_path を使用
    # output_dir は親ディレクトリを指しているが、generate_image_path 内で適切に処理されることを期待
    # ただし generate_image_path は output_dir/image/... を返す仕様であるか確認が必要

    if pag is None:
        raise ImportError("pyautogui がインポートされていません。GUI環境で実行してください。")

    for page in range(start_page, end_page+1):
        image_path = generate_image_path(output_dir, page, chapter_name)

        # スクリーンショット撮影
        s = pag.screenshot(region=region)
        s.save(image_path)
        print(f"保存: {image_path}")

        # 次のページへ
        pag.keyDown(next_page_key)
        pag.keyUp(next_page_key)
        time.sleep(shot_span)

    print(f"全ての画像を {Path(image_path).parent} に保存しました")


def _main():
    args = _parse_args()

    start_page = args.start_page
    end_page = args.end_page
    output_dir = args.output_dir
    chapter_name = args.chapter_name
    key = args.key

    image_dir = os.path.join(output_dir, "image")
    for dir_path in [output_dir, image_dir]:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    # スクショする範囲を指定します
    # region = (左上のx座標, 左上のy座標, スクショの横幅, スクショの縦幅)
    region = decide_capture_region()

    capture_screen(start_page, end_page, output_dir, chapter_name, region, key)


if __name__ == "__main__":
    _main()
