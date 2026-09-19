"""把 data/ 下所有数据包的所有 Baseline 文件都过一遍模型。

解析结果会缓存在 cache/ 中，因此第一次运行较慢，之后会快很多。

用法（工作目录为 backend/）：
    uv run test.py [关键字 ...]
"""

import sys
import typing

import main
from china_eaip_dataset.aixm.features import CommonRoot

ALL_FILES: list[str] = list(typing.get_args(main.File))


def check(folder: main.BaselineDataPackage, keyword: str) -> str | None:
    """校验单个文件，返回错误描述；解析成功时返回 None。"""
    try:
        CommonRoot.model_validate(obj=folder.read_file(typing.cast(main.File, keyword)))
    except Exception as error:  # noqa: BLE001
        return f"{type(error).__name__}: {error}"
    return None


def main_function() -> None:
    folders: list[main.BaselineDataPackage] = sorted(
        main.BaselineDataPackage.list_all(), key=lambda x: x.filename
    )
    keywords: list[str] = sys.argv[1:] or ALL_FILES
    passed: int = 0
    for folder in folders:
        for keyword in keywords:
            error: str | None = check(folder=folder, keyword=keyword)
            if error is None:
                passed += 1
                continue
            print(f"!!! {folder.filename} {keyword}\n{error}\n", flush=True)
    print(f"合计 {passed}/{len(folders) * len(keywords)} 通过")


if __name__ == "__main__":
    main_function()
