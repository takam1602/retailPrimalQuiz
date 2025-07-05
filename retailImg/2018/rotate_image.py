#!/usr/bin/env python3
"""
指定ディレクトリ（デフォルトはカレント）にある JPEG/PNG 画像を
任意の角度だけ回転させて保存するスクリプト。

使い方:
    python rotate_images.py -a 37                # *.jpg を 37° 反時計回りに（上書き）
    python rotate_images.py -a -90 -s rotated/   # 時計回り 90°、rotated/ に保存
"""
import argparse
from pathlib import Path
from PIL import Image, ExifTags

def parse_args():
    p = argparse.ArgumentParser(description="Bulk-rotate images.")
    p.add_argument("-a", "--angle", type=float, required=True,
                   help="回転角度（正:反時計回り，負:時計回り）")
    p.add_argument("-d", "--dir", default=".",
                   help="入力ディレクトリ（デフォルト: 現在のディレクトリ）")
    p.add_argument("-s", "--save_dir", default=None,
                   help="保存先ディレクトリ（省略すると上書き）")
    p.add_argument("--ext", default=".jpg,.jpeg,.png",
                   help="対象拡張子をカンマ区切りで指定")
    return p.parse_args()

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    """EXIF Orientation を考慮して画像を正立させる（必要なら）"""
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, 1)
            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except Exception:
        pass
    return img

def main():
    args = parse_args()
    in_dir = Path(args.dir)
    exts = tuple(e.lower() for e in args.ext.split(","))
    out_dir = Path(args.save_dir) if args.save_dir else in_dir
    if args.save_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    for path in sorted(in_dir.iterdir()):
        if path.suffix.lower() not in exts:
            continue
        with Image.open(path) as im:
            im = fix_exif_orientation(im)
            rotated = im.rotate(args.angle, expand=True)
            save_path = (out_dir / path.name
                         if args.save_dir is None
                         else out_dir / path.name)
            rotated.save(save_path, quality=95)
            print(f"Saved: {save_path}")

if __name__ == "__main__":
    main()
