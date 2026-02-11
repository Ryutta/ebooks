"""
スクリーンショットを連続撮影し、PDFファイルとして保存するメインスクリプト。
ユーザーが指定した範囲を撮影し、画像として保存した後、それらをまとめてPDFにします。
"""
import argparse
import os
import sys

# screenshot.py と image2pdf.py は同じディレクトリにあると想定
try:
    from screenshot import decide_capture_region, capture_screen
    from image2pdf import image_to_pdf
except ImportError as e:
    print(f"モジュールのインポートエラー: {e}")
    print("必要なライブラリ (pyautogui, fpdf2) がインストールされているか確認してください。")
    sys.exit(1)


def _parse_args():
    parser = argparse.ArgumentParser(description="スクリーンショット撮影 & PDF作成ツール")
    parser.add_argument('-s', '--start_page', help='開始ページ番号', type=int, required=True)
    parser.add_argument('-e', '--end_page', help='終了ページ番号', type=int, required=True)
    parser.add_argument('-o', '--output_dir', help='出力ディレクトリ (デフォルト: 現在のディレクトリ)', default='.')
    parser.add_argument('-c', '--chapter_name', help='章などの名前 (ファイル名の接頭辞になります)', default='')
    parser.add_argument('-k', '--key', help='ページ送りキー (right または left)', default=None, choices=['right', 'left'])

    return parser.parse_args()


def _main():
    args = _parse_args()

    start_page = args.start_page
    end_page = args.end_page
    output_dir = args.output_dir
    chapter_name = args.chapter_name
    key = args.key

    # ディレクトリの準備
    image_dir = os.path.join(output_dir, "image")
    pdf_dir = os.path.join(output_dir, "pdf")

    try:
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(pdf_dir, exist_ok=True)
    except OSError as e:
        print(f"ディレクトリ作成エラー: {e}")
        sys.exit(1)

    print("=== スクリーンショット PDF 作成ツール ===")
    print(f"出力先: {os.path.abspath(output_dir)}")
    print(f"ページ範囲: {start_page} ～ {end_page}")
    if chapter_name:
        print(f"章の名前: {chapter_name}")
    print("========================================")
    print()

    try:
        # 1. スクショする範囲を指定
        print("【ステップ1: キャプチャ範囲の指定】")
        # region = (左上のx座標, 左上のy座標, スクショの横幅, スクショの縦幅)
        region = decide_capture_region()
        print("範囲指定が完了しました。")
        print()

        # 2. スクリーンショット撮影
        print("【ステップ2: スクリーンショット撮影】")
        if key:
            capture_screen(start_page, end_page, output_dir, chapter_name, region, key)
        else:
            capture_screen(start_page, end_page, output_dir, chapter_name, region)
        print("撮影が完了しました。")
        print()

        # 3. PDF作成
        print("【ステップ3: PDF作成】")
        image_to_pdf(start_page, end_page, output_dir, chapter_name)

    except KeyboardInterrupt:
        print("\n処理が中断されました。")
        sys.exit(0)
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")
        sys.exit(1)

    print()
    print("全ての工程が正常に完了しました。お疲れ様でした！")


if __name__ == "__main__":
    _main()
