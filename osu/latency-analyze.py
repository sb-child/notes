import os
import sys
import math
import argparse
from pathlib import Path
from typing import List

SCRIPT_PATH = Path(__file__).resolve()
CWD = Path(SCRIPT_PATH).parent


def parser():
    p = argparse.ArgumentParser(
        prog='analyze.py',
        description='osu! play data analyzer | 算算你的平均准度喵',
    )
    p.add_argument('datafile', help='数据文件')
    return p


def ur_map(x: float) -> float:
    '''
    map a ur value (0..=1000) to (1..=0)
    '''
    x = min(max(0, x), 1000)
    def fx(x): return 0.0001 * x - 0.2 * x + 100
    x = fx(x) / 100
    return x


class ScorePoint:
    def __init__(self, hit_error: float, ur: float) -> None:
        self._hit_error = hit_error
        self._ur = ur

    @property
    def ur(self) -> float:
        '''
        Unstable Rate, in 0.1 ms.
        '''
        return self._ur

    @property
    def hit_error(self) -> float:
        '''
        Hit Error, in 1 ms.

        Negative = early, Positive = late
        '''
        return self._hit_error


class DataFile:
    def __init__(self, fp: Path, title: str, points: List[ScorePoint]) -> None:
        self.filepath = fp
        self.title = title
        self.points = points

    def ur_to_weight(self) -> List[float]:
        ur_weight = [ur_map(i.ur) for i in self.points]
        max_ur_weight = max(ur_weight)
        ur_weight_offset_factor = 1 / max_ur_weight
        normed_ur_weight = [
            pow(i * ur_weight_offset_factor, 2) for i in ur_weight]
        print(f"ur_weight: {ur_weight}")
        print(f"max_ur_weight: {max_ur_weight}")
        print(f"ur_weight_offset_factor: {ur_weight_offset_factor}")
        print(f"normed_ur_weight: {normed_ur_weight}")

        
        pass

    def offset_hit_error(self) -> List[float]:
        min_hit_error = min([i.hit_error for i in self.points])
        max_hit_error = max([i.hit_error for i in self.points])
        avg_hit_error = sum(
            [i.hit_error for i in self.points]) / len(self.points)
        hit_error_range = max_hit_error - min_hit_error
        hit_error_mean = sum([max_hit_error, min_hit_error]) / 2
        # offseted = [i.hit_error - max_hit_error for i in self.points]
        print(f"min_hit_error: {min_hit_error}")
        print(f"max_hit_error: {max_hit_error}")
        print(f"avg_hit_error: {avg_hit_error}")
        print(f"hit_error_range: {hit_error_range}")
        print(f"hit_error_mean: {hit_error_mean}")
        # print(f"offseted: {offseted}")
        pass


def open_data_file(fp: Path) -> DataFile:
    title = ""
    points: List[ScorePoint] = []
    with fp.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                if not title:
                    title = s.lstrip("#").strip()
                continue
            parts = s.split()
            if len(parts) < 2:
                continue
            try:
                hit_error = float(parts[0])
                ur = float(parts[1])
            except ValueError:
                continue
            points.append(ScorePoint(hit_error, ur))
    return DataFile(fp, title, points)


def main():
    args = parser().parse_args()
    datafile_path = Path(args.datafile).resolve()
    if not datafile_path.exists():
        print(f"你指定的 {datafile_path} 不存在")
        return
    if not datafile_path.is_file():
        print(f"你指定的 {datafile_path} 并不是一个文件")
        return
    print(f"正在分析 {datafile_path} ...")
    try:
        datafile = open_data_file(datafile_path)
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        print(f"文件解析失败: {e}")
        return
    datafile.offset_hit_error()
    datafile.ur_to_weight()
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("执行已中断")
