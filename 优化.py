#!/usr/bin/python3

import collections.abc
import hashlib
import pathlib
import zipfile


def 解压文件(zip_file_path: pathlib.Path, extract_to_dir: pathlib.Path) -> None:
    extract_to_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(file=zip_file_path) as zip_ref:
        zip_ref.extractall(path=extract_to_dir)


class 重复索引表:
    def __init__(self) -> None:
        self.by_size: dict[int, set[pathlib.Path]] = {}
        self.hashes: dict[pathlib.Path, str] = {}

    def 计算文件哈希(self, path: pathlib.Path) -> str:
        if path not in self.hashes:
            self.hashes[path] = hashlib.sha256(data=path.read_bytes()).hexdigest()
        return self.hashes[path]

    def 文件重复(self, path: pathlib.Path) -> pathlib.Path | None:
        key: int = path.lstat().st_size
        if key in self.by_size:
            for 既有文件 in self.by_size[key]:
                if self.计算文件哈希(path=既有文件) == self.计算文件哈希(path=path):
                    return 既有文件
        if key not in self.by_size:
            self.by_size[key] = set()
        self.by_size[key].add(path)


def 列出所有文件(
    路径: pathlib.Path,
) -> collections.abc.Generator[pathlib.Path, None, None]:
    if 路径.is_dir():
        for 子路径 in 路径.iterdir():
            yield from 列出所有文件(路径=子路径)
    else:
        yield 路径


def 计算大小(root_path: pathlib.Path) -> float:
    return sum(
        path.lstat().st_size / path.lstat().st_nlink
        for path in 列出所有文件(路径=root_path)
    )


根目录 = pathlib.Path("content")

for x in sorted(pathlib.Path("raw").iterdir()):
    if x.suffix == ".zip" and not 根目录.joinpath(x.stem).exists():
        解压文件(zip_file_path=x, extract_to_dir=根目录)
        print(x)

s = 重复索引表()
优化前文件总大小: float = 计算大小(root_path=根目录)
print(f"优化前文件总大小为 {优化前文件总大小}")

for 当前文件 in 列出所有文件(路径=根目录):
    if 当前文件.lstat().st_nlink == 1:
        重复文件: pathlib.Path | None = s.文件重复(path=当前文件)
        if 重复文件:
            try:
                print(当前文件, 重复文件)
            except UnicodeEncodeError:
                pass
            当前文件.unlink()
            当前文件.hardlink_to(target=重复文件)

优化后文件总大小: float = 计算大小(root_path=根目录)
print(f"优化后文件总大小为 {优化后文件总大小}")
print(
    f"优化了 {round(number=(1 - 优化后文件总大小 / 优化前文件总大小) * 100, ndigits=2)}%"
)
