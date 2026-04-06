import collections.abc
import hashlib
import os
import pathlib
import zipfile

ROOT = pathlib.Path("../data")
TARGET = pathlib.Path("../schema")


def 列出所有文件(根路径: pathlib.Path) -> collections.abc.Iterable[pathlib.Path]:
    if 根路径.exists():
        if not 根路径.is_dir():
            yield 根路径
        else:
            for 子路径 in 根路径.iterdir():
                yield from 列出所有文件(根路径=子路径)


def 删除空文件夹(根路径: pathlib.Path, 删除其中文件: bool = False) -> None:
    if 根路径.exists():
        if 根路径.is_dir():
            for x in 根路径.iterdir():
                删除空文件夹(根路径=x, 删除其中文件=删除其中文件)
            if len(list(根路径.iterdir())) == 0:
                根路径.rmdir()
        elif 删除其中文件:
            根路径.unlink()


def first_step_unzip_all_files() -> None:
    """第一步：解压所有 ZIP 文件"""
    for file in [file for file in ROOT.iterdir() if file.suffix == ".zip"]:
        zipfile.ZipFile(file=file).extractall(path=ROOT.joinpath(file.stem))


def second_step_remove_duplicated_files() -> None:
    hash_set: set[str] = set()
    for package in [x.joinpath("schema") for x in ROOT.iterdir()]:
        for file in 列出所有文件(根路径=package):
            result: str = hashlib.md5(data=file.read_bytes()).hexdigest()
            if result in hash_set:
                file.unlink()
            else:
                hash_set.add(result)

    删除空文件夹(根路径=ROOT)


def third_step_move_to_common_schema() -> None:
    删除空文件夹(根路径=TARGET, 删除其中文件=True)

    moved: bool = False
    for package in [x.joinpath("schema") for x in ROOT.iterdir()]:
        if package.exists():
            assert moved is False, FileExistsError("XSD 文件存在修订！")
            package.move(target=TARGET)
            moved = True


def fourth_step_replace_online_references() -> None:
    for file in 列出所有文件(根路径=TARGET):
        content: str = file.read_text()
        replaced = False
        for old_string, relative_path in [
            ("http://schemas.opengis.net/gml/3.2.1", "ISO_19136_Schemas"),
            ("http://schemas.opengis.net/iso/19139/20070417", "ISO_19139_Schemas"),
            ("maven:com.uvic-cfar.swim:aixm-jaxb!/xsd", ""),
        ]:
            new_string: str = os.path.relpath(
                path=TARGET.joinpath(f"aixm511/xsd/{relative_path}"),
                start=file.parent,
            ).replace("\\", "/")
            if old_string in content:
                content = content.replace(old_string, new_string)
                replaced = True
        if replaced:
            file.write_text(data=content)


def fifth_step_replace_problem_reference() -> None:
    # 解决以下两个超过 10 个字符的 designator 的问题
    # Path: /message:AIXMBasicMessage/message:hasMember[32]/aixm:Airspace/aixm:timeSlice/aixm:AirspaceTimeSlice/aixm:designator
    # <aixm:designator xmlns:aixm="http://www.aixm.aero/schema/5.1.1">ZYHBAP02(05)</aixm:designator>
    # Path: /message:AIXMBasicMessage/message:hasMember[61]/aixm:Airspace/aixm:timeSlice/aixm:AirspaceTimeSlice/aixm:designator
    # <aixm:designator xmlns:aixm="http://www.aixm.aero/schema/5.1.1">ZYTLAP02(10)1</aixm:designator>
    u: pathlib.Path = TARGET.joinpath("aixm511/xsd/AIXM_DataTypes.xsd")
    u.write_text(
        data=u.read_text().replace('<maxLength value="10"/>', '<maxLength value="13"/>')
    )

    # 解决以下两个超过 10 个字符的 designator 的问题
    # Path: /message:AIXMBasicMessage/message:hasMember[166]/aixm:DesignatedPoint/aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:designator
    # <aixm:designator xmlns:aixm="http://www.aixm.aero/schema/5.1.1">****</aixm:designator>
    u.write_text(data=u.read_text().replace("([A-Z]|\\d)*", "([A-Z]|\\d|\\*)*"))


first_step_unzip_all_files()
second_step_remove_duplicated_files()
third_step_move_to_common_schema()
fourth_step_replace_online_references()
fifth_step_replace_problem_reference()
