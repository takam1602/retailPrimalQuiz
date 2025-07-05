#!/usr/bin/env python3
"""
resize_images.py
----------------
指定ディレクトリ配下の JPEG / PNG 画像を
  • 最長辺が `--max-size` ピクセルを超える場合だけ縮小（アスペクト比維持）
  • JPEG は `--quality` で再圧縮、PNG は可逆圧縮を最適化
  • メタデータ（EXIF / ICC など）を除去
して保存します。

デフォルトでは **上書き**。`--out-dir` を渡すと別フォルダに保存します。

使用例
------
# 画像が大きいときだけ 1920px に縮小し上書き
python resize_images.py --dir ./photos --max-size 1920 --quality 85

# サブディレクトリも含め再帰的に処理し、結果を ./resized に保存
python resize_images.py --dir ./photos --out-dir ./resized -r

# 最大 1280px、JPEG 品質 75、処理を 8 並列で実行
python resize_images.py -d ./imgs -m 1280 -q 75 -p 8
"""
import argparse
import concurrent.futures as cf
import sys
from pathlib import Path
from typing import Tuple

from PIL import Image, ExifTags

# ------------------------------- 解析用関数 ------------------------------- #
def _fix_exif_orientation(img: Image.Image) -> Image.Image:
    """EXIF Orientation に従い画像を正立させる。"""
    try:
        orientation_key = next(k for k, v in ExifTags.TAGS.items() if v == "Orientation")
        exif = img._getexif() or {}
        orientation = exif.get(orientation_key, 1)
        rotate_map = {3: 180, 6: 270, 8: 90}
        if orientation in rotate_map:
            img = img.rotate(rotate_map[orientation], expand=True)
    except Exception:
        # EXIF が無い or PIL が解釈できない場合はそのまま
        pass
    return img


def _process_file(
    in_path: Path,
    out_path: Path,
    max_size: int,
    quality: int,
) -> Tuple[Path, bool, str]:
    """1 ファイルを処理して (保存先, 変換したかどうか, 失敗した場合はエラーメッセージ) を返す。"""
    try:
        with Image.open(in_path) as im:
            im = _fix_exif_orientation(im)
            orig_size = im.size
            im.thumbnail((max_size, max_size), Image.LANCZOS)  # アスペクト比維持
            save_kwargs = dict(optimize=True)
            if in_path.suffix.lower() in (".jpg", ".jpeg"):
                save_kwargs.update(
                    format="JPEG",
                    quality=quality,
                    progressive=True,
                )
            else:  # PNG など
                save_kwargs.update(format=im.format)

            out_path.parent.mkdir(parents=True, exist_ok=True)
            im.save(out_path, **save_kwargs)
            converted = im.size != orig_size  # 縮小されたかどうか
            return out_path, converted, ""
    except Exception as e:
        return out_path, False, str(e)


# ------------------------------- メイン処理 ------------------------------- #
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Bulk resize & compress images.")
    p.add_argument("-d", "--dir", required=True, help="入力ディレクトリ")
    p.add_argument("-o", "--out-dir", default=None, help="出力ディレクトリ（省略で上書き）")
    p.add_argument(
        "-m",
        "--max-size",
        type=int,
        default=1920,
        help="最長辺の上限ピクセル（デフォルト: 1920）",
    )
    p.add_argument(
        "-q",
        "--quality",
        type=int,
        default=85,
        help="JPEG 品質 0–100（デフォルト: 85）",
    )
    p.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="サブディレクトリも含めて処理",
    )
    p.add_argument(
        "-p",
        "--processes",
        type=int,
        default=0,
        help="並列実行プロセス数（0 なら CPU コア数）",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    in_dir = Path(args.dir).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else in_dir
    suffixes = (".jpg", ".jpeg", ".png")

    if not in_dir.is_dir():
        sys.exit(f"[ERROR] 入力ディレクトリが見つかりません: {in_dir}")

    # 対象ファイル一覧
    files = (
        in_dir.rglob("*")
        if args.recursive
        else in_dir.glob("*")
    )
    targets = [p for p in files if p.suffix.lower() in suffixes and p.is_file()]

    if not targets:
        sys.exit("[INFO] 対象画像が見つかりませんでした。")

    print(f"[INFO] 画像 {len(targets)} 枚を処理します…")

    # 並列実行
    n_proc = args.processes or None
    with cf.ProcessPoolExecutor(max_workers=n_proc) as ex:
        futures = [
            ex.submit(
                _process_file,
                p,
                out_dir / p.relative_to(in_dir),
                args.max_size,
                args.quality,
            )
            for p in targets
        ]
        converted, skipped, failed = 0, 0, 0
        for f in cf.as_completed(futures):
            out_path, was_converted, err = f.result()
            if err:
                failed += 1
                print(f"[FAIL]  {out_path}: {err}")
            else:
                if was_converted:
                    converted += 1
                else:
                    skipped += 1

    print(
        f"[DONE] 完了: 縮小 {converted} 枚 / そのまま {skipped} 枚 / 失敗 {failed} 枚"
    )


if __name__ == "__main__":
    main()
