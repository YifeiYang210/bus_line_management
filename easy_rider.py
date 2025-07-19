"""
(六) 按需停靠站
按需停靠站（标记为字母 O）不能是起始站、终点站或换乘站。
在此阶段，您需要使用第 4 阶段的检查来识别错误标记为 O 的站点，并仅显示正确的按需站点。

目标：
1. 输入包含 JSON 格式数据的字符串。
2. 检查所有出发点、终点站和换乘站是否不是“按需”。
3. 显示标有 O 的非起点、终点或转运停靠点的停靠点。
4. 输出的格式应与示例中所示的格式相同。

示例1：
[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "O",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": 256,
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "09:20"
    },
    {
        "bus_id": 256,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Abbey Road",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10:12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "08:13"
    },
    {
        "bus_id": 512,
        "stop_id": 6,
        "stop_name": "Abbey Road",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:16"
    }
]

Type and field validation: 0 errors
bus_id: 0
stop_id: 0
stop_name: 0
next_stop: 0
stop_type: 0
a_time: 0

Line names and number of stops:
bus_id: 128 stops: 4
bus_id: 256 stops: 4
bus_id: 512 stops: 2

Start stops: 3 ['Bourbon Street', 'Pilotow Street', 'Prospekt Avenue']
Transfer stops: 3 ['Abbey Road', 'Elm Street', 'Sesame Street']
Finish stops: 2 ['Abbey Road', 'Sesame Street']
On demand stops: 1 ['Fifth Avenue']
""" 

import json
import re
from typing import List, Dict, Any
    

def validate_bus_line_data(data):
    """
    (一) 检查数据类型
    您刚刚开始整理 “Easy Rider” 公交公司的现有数据库，数据中有很多错误。
    在下面的输入数据示例中，有些字段没有值，特定字段中的字符数过多或过少。
    幸运的是，有一些文档可以帮助您解决这些混乱，然而，这份文件并不是百分之百完整的，上面有咖啡和撕掉的部分。
    以下是您拥有的文件：Documentation.jpg 和 Diagram_of_the_bus_line.jpg。
    在此阶段，您需要使用文档，并将输入数据中的字段与 Type 和 Other 列中指定的要求进行比较。

    目标：
    1. 输入包含 JSON 格式数据的字符串。
    2. 检查数据类型是否匹配。
    3. 检查必填字段是否已填写。
    4. 显示有关在总数和每个字段中找到的错误数的信息。请记住，可能根本没有错误。
    5. 输出的格式应与示例中所示的格式相同。

    现在无需担心格式（名称验证）。在此阶段，我们只确保字段具有正确的类型，并且所有必需的字段都已填充。
    请注意，像 stop_type 类型为 Char，字段可以为空或包含单个字符 （字符串）

    输入：
    [
        {
            "bus_id": 128,
            "stop_id": 1,
            "stop_name": "Prospekt Avenue",
            "next_stop": 3,
            "stop_type": "S",
            "a_time": 8.12
        },
        {
            "bus_id": 128,
            "stop_id": 3,
            "stop_name": "",
            "next_stop": 5,
            "stop_type": "",
            "a_time": "08:19"
        },
        {
            "bus_id": 128,
            "stop_id": 5,
            "stop_name": "Fifth Avenue",
            "next_stop": 7,
            "stop_type": "O",
            "a_time": "08:25"
        },
        {
            "bus_id": 128,
            "stop_id": "7",
            "stop_name": "Sesame Street",
            "next_stop": 0,
            "stop_type": "F",
            "a_time": "08:37"
        },
        {
            "bus_id": "",
            "stop_id": 2,
            "stop_name": "Pilotow Street",
            "next_stop": 3,
            "stop_type": "S",
            "a_time": ""
        },
        {
            "bus_id": 256,
            "stop_id": 3,
            "stop_name": "Elm Street",
            "next_stop": 6,
            "stop_type": "",
            "a_time": "09:45"
        },
        {
            "bus_id": 256,
            "stop_id": 6,
            "stop_name": "Sunset Boulevard",
            "next_stop": 7,
            "stop_type": "",
            "a_time": "09:59"
        },
        {
            "bus_id": 256,
            "stop_id": 7,
            "stop_name": "Sesame Street",
            "next_stop": "0",
            "stop_type": "F",
            "a_time": "10:12"
        },
        {
            "bus_id": 512,
            "stop_id": 4,
            "stop_name": "Bourbon Street",
            "next_stop": 6,
            "stop_type": "S",
            "a_time": "08:13"
        },
        {
            "bus_id": "512",
            "stop_id": 6,
            "stop_name": "Sunset Boulevard",
            "next_stop": 0,
            "stop_type": 5,
            "a_time": "08:16"
        }
    ]

    输出：
    Type and field validation: 8 errors
    bus_id: 2
    stop_id: 1
    stop_name: 1
    next_stop: 1
    stop_type: 1
    a_time: 2
    """
    """
    (五) 到站时间
    检查即将到来的站点的到达时间是否合理：它们应该增加。
    在此阶段，您需要更新检查 a_time 错误：合并之前的格式和类型检查与正确到达时间的检查。
    目标：
    1. 输入包含 JSON 格式数据的字符串。
    2. 检查给定公交线路的即将到来的站点的到达时间是否正在增加。
    请注意，每条单独的公交路线已经根据停靠点的顺序进行了排序。
    3. 如果下一站的到达时间早于或等于当前停靠点的时间，请停止检查该公交线路并注意错误的站点。
    将错误事例数与 a_time 错误总数相加。对于正确的停止点，不要显示任何内容。
    4. 输出的格式应与示例中所示的格式相同。
    示例1：
    [
        {"bus_id": 128, "a_time": "08:12"}, 
        {"bus_id": 128, "a_time": "08:19"}, 
        {"bus_id": 128, "a_time": "08:17"}, 
        {"bus_id": 128, "a_time": "08:07"},
        {"bus_id": 256, "a_time": "09:20"},
        {"bus_id": 256, "a_time": "09:45"},
        {"bus_id": 256, "a_time": "09:44"}, 
        {"bus_id": 256, "a_time": "10:12"},
        {"bus_id": 512, "a_time": "08:13"},
        {"bus_id": 512, "a_time": "08:16"}
    ]
    Type and field validation: 6 errors
    a_time: 3

    示例2：
    [
        {"bus_id": 128, "a_time": "08:12"}, 
        {"bus_id": 128, "a_time": "8:19"}, 
        {"bus_id": 128, "a_time": "08:25"}, 
        {"bus_id": 128, "a_time": "08:77"},
        {"bus_id": 256, "a_time": "09:20"},
        {"bus_id": 256, "a_time": "09:45"},
        {"bus_id": 256, "a_time": "09:59"}, 
        {"bus_id": 256, "a_time": "10.12"},
        {"bus_id": 512, "a_time": "38:13"},
        {"bus_id": 512, "a_time": "08:16"}
    ]
    Type and field validation: 6 errors
    a_time: 4
    """
    errors = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0
    }
    
    # entry is a dictionary representing a bus stop entry
    for entry in data:
        if not isinstance(entry.get("bus_id"), int):
            errors["bus_id"] += 1
        if not isinstance(entry.get("stop_id"), int):
            errors["stop_id"] += 1
        if not isinstance(entry.get("stop_name"), str) or len(entry.get("stop_name", "")) == 0:
            errors["stop_name"] += 1
        if not isinstance(entry.get("next_stop"), int):
            errors["next_stop"] += 1
        if not (isinstance(entry.get("stop_type"), str) and (len(entry.get("stop_type", "")) == 1 or entry.get("stop_type") == "")):
            errors["stop_type"] += 1
        if not (isinstance(entry.get("a_time"), str) and len(entry.get("a_time")) == 5):
            errors["a_time"] += 1
    
    total_errors = sum(errors.values())
    
    print(f"Type and field validation: {total_errors} errors")
    for field, count in errors.items():
        print(f"{field}: {count}")


def validate_syntax(data):
    """
    (二) 检查数据语法
    在此阶段，除了检查输入是否有缺失数据和所需类型外，您还将验证以下三个字段的后缀名称：
    stop_name、stop_type 和 a_time。
    因此，将类型和字段验证以及格式验证的错误相加，然后将它们一起显示。

    stop_name 字段的格式为 [proper name][suffix]
    suffix: Road/Avenue/Boulevard/Street
    Proper name starts with a capital letter.

    stop_type 字段的格式为单个字符，可能为空。
    S - starting stop, O - stop on demand, F - final stop

    a_time 时间格式为军用时间（24 小时，hh：mm）。这意味着存在某些限制
    1. 第一位数字不能是 3、4 等;
    2. 小于 10 小时时，其前面应为 0，例如 08：34;
    3. 分隔符应为 colon ：。

    目标：
    1. 输入包含 JSON 格式数据的字符串。
    2. 检查数据类型是否匹配，并且是否像以前一样填写了必填字段。
    3. 计算 stop_name、stop_type、a_time 的格式错误数，并合并相关字段的错误计数。
    4. 与上一阶段一样，打印有关总和每个字段中发现的错误数的信息。请记住，可能根本没有错误。
    5. 输出的格式应与示例中所示的格式相同。

    示例：
    [
        {
            "bus_id": 128,
            "stop_id": 1,
            "stop_name": "Prospekt Av.",
            "next_stop": 3,
            "stop_type": "S",
            "a_time": "08:12"
        },
        {
            "bus_id": 128,
            "stop_id": 3,
            "stop_name": "Elm Street",
            "next_stop": 5,
            "stop_type": "",
            "a_time": "8:19"
        },
        {
            "bus_id": 128,
            "stop_id": 5,
            "stop_name": "Fifth Avenue",
            "next_stop": 7,
            "stop_type": "K",
            "a_time": "08:25"
        },
        {
            "bus_id": 128,
            "stop_id": "7",
            "stop_name": "Sesame Street",
            "next_stop": 0,
            "stop_type": "F",
            "a_time": "08:77"
        },
        {
            "bus_id": "",
            "stop_id": 2,
            "stop_name": "Pilotow Street",
            "next_stop": 3,
            "stop_type": "S",
            "a_time": "09:20"
        },
        {
            "bus_id": 256,
            "stop_id": 3,
            "stop_name": "Elm",
            "next_stop": 6,
            "stop_type": "",
            "a_time": "09:45"
        },
        {
            "bus_id": 256,
            "stop_id": 6,
            "stop_name": "Sunset Boulevard",
            "next_stop": 7,
            "stop_type": "A",
            "a_time": "09:59"
        },
        {
            "bus_id": 256,
            "stop_id": 7,
            "stop_name": "Sesame Street",
            "next_stop": "0",
            "stop_type": "F",
            "a_time": "10.12"
        },
        {
            "bus_id": 512,
            "stop_id": 4,
            "stop_name": "bourbon street",
            "next_stop": 6,
            "stop_type": "S",
            "a_time": "38:13"
        },
        {
            "bus_id": "512",
            "stop_id": 6,
            "stop_name": "Sunset Boulevard",
            "next_stop": 0,
            "stop_type": "F",
            "a_time": "08:16"
        }
    ]
    Type and field validation: 13 errors
    bus_id: 2
    stop_id: 1
    stop_name: 3
    next_stop: 1
    stop_type: 2
    a_time: 4
    """
    errors = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0
    }
    
    # Regex patterns for validation
    stop_name_pattern = re.compile(r"^[A-Z][a-zA-Z\s]*(Road|Avenue|Boulevard|Street)$")
    stop_type_pattern = re.compile(r"^[SFO]?$")
    a_time_pattern = re.compile(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")

    # 3. 辅助结构：记录每条线路上一站的到站时间（分钟数）及是否已出现顺序错误
    last_time: Dict[int, int] = {}        # {bus_id: minutes}
    broken_line: Dict[int, bool] = {}     # {bus_id: True}  → 一旦出错后续不再检查该线

    # dict.get如果键不存在，则返回默认值 None
    for entry in data:
        if not isinstance(entry.get("bus_id"), int):
            errors["bus_id"] += 1
        if not isinstance(entry.get("stop_id"), int):
            errors["stop_id"] += 1
        if not isinstance(entry.get("stop_name"), str) or not stop_name_pattern.match(entry.get("stop_name", "")):
            errors["stop_name"] += 1
        if not isinstance(entry.get("next_stop"), int):
            errors["next_stop"] += 1
        if not stop_type_pattern.match(entry.get("stop_type", "")):
            errors["stop_type"] += 1
        if not a_time_pattern.match(entry.get("a_time", "")):
            errors["a_time"] += 1

        bus_id = entry.get("bus_id")
        a_time = entry.get("a_time")
        minutes_now = int(a_time[:2]) * 60 + int(a_time[3:])

        # 如果此前该线路已发现递增性错误，跳过继续下一条记录
        if broken_line.get(bus_id, False):
            continue

        # 第一次看到该线路
        if bus_id not in last_time:
            last_time[bus_id] = minutes_now
            continue

        # 递增性判断
        if minutes_now <= last_time[bus_id]:
            errors["a_time"] += 1          # 与格式错误合并计数
            broken_line[bus_id] = True     # 标记该线路后续不再检查
            # 不更新 last_time，直接进入下一条
        else:
            last_time[bus_id] = minutes_now

    total_errors = sum(errors.values())
    
    print(f"Type and field validation: {total_errors} errors")
    for field, count in errors.items():
        print(f"{field}: {count}")


def find_bus_lines(data):
    """
    (三) 公交线路信息
    目标：
    1. 输入包含 JSON 格式数据的字符串。
    2. 像以前一样检查数据类型、必填字段和格式。
    3. 查找所有公交线路的名称。
    4. 验证每条线路的停靠点数。
    5. 输出的格式应与示例中所示的格式相同。

    示例输出：

    Line names and number of stops:
    bus_id: 128 stops: 4
    bus_id: 256 stops: 4
    bus_id: 512 stops: 2
    """
    bus_lines = {}
    
    for entry in data:
        bus_id = entry.get("bus_id")
        if bus_id is not None:
            if bus_id not in bus_lines:
                bus_lines[bus_id] = 0
            bus_lines[bus_id] += 1
    
    print()
    print("Line names and number of stops:")
    for bus_id, stops in bus_lines.items():
        print(f"bus_id: {bus_id} stops: {stops}")


def find_special_stops(data):
    """
    (四) 特殊站点
    目标：
    1. 确保每条公交线路恰好有一个起点（S）和一个终点（F）。
    2. 如果所有公交线路都符合条件，就统计每条公交车线路有多少个起点和终点站。按字母顺序打印其唯一名称。
    3. 计算换乘站并按字母顺序打印其唯一名称。换乘站是至少两条公交线路共用的站点。
    4. 输出的格式应与示例中所示的格式相同。按每条公交车线路的起始站，换乘站，终点站的顺序换行打印。
    如[
        {"bus_id": 128,"stop_name": "Prospekt Avenue","stop_type": "S",},
        {"bus_id": 128,"stop_name": "Elm Street","stop_type": "",},
        {"bus_id": 128,"stop_name": "Fifth Avenue","stop_type": "O",},
        {"bus_id": 128,"stop_name": "Sesame Street","stop_type": "F"},
        {"bus_id": 256,"stop_name": "Pilotow Street","stop_type": "S"},
        {"bus_id": 256,"stop_name": "Elm Street","stop_type": "O"},
        {"bus_id": 256,"stop_name": "Sesame Street","stop_type": "F"},
        {"bus_id": 512,"stop_name": "Bourbon Street","stop_type": "S"},
        {"bus_id": 512,"stop_name": "Sunset Boulevard","stop_type": "F"},
    ]
    Start stops: 3 ['Bourbon Street', 'Pilotow Street', 'Prospekt Avenue']
    Transfer stops: 3 ['Elm Street', 'Sesame Street', 'Sunset Boulevard']
    Finish stops: 2 ['Sesame Street', 'Sunset Boulevard']
    5. 如果公交线路不符合此条件，请停止检查并打印有关它的消息。不要继续检查其他公交线路。
    如，bus_id: 512 没有起点或终点站，则输出：There is no start or end stop for the line: 512
    """
    """
    (六) 按需停靠站
    按需停靠站（标记为字母 O）不能是起始站、终点站或换乘站。
    在此阶段，您需要使用第 4 阶段的检查来识别错误标记为 O 的站点，并仅显示正确的按需站点。

    目标：
    1. 输入包含 JSON 格式数据的字符串。
    2. 检查所有出发点、终点站和换乘站是否不是“按需”。
    3. 显示标有 O 的非起点、终点或转运停靠点的停靠点。
    4. 输出的格式应与示例中所示的格式相同。

    示例：
    [
        {"bus_id": 128, "stop_name": "Prospekt Avenue", "stop_type": "S"},
        {"bus_id": 128, "stop_name": "Elm Street", "stop_type": "O"},
        {"bus_id": 128, "stop_name": "Fifth Avenue", "stop_type": "O"},
        {"bus_id": 128, "stop_name": "Sesame Street", "stop_type": "F"},
        {"bus_id": 256, "stop_name": "Pilotow Street", "stop_type": "S"},
        {"bus_id": 256, "stop_name": "Elm Street", "stop_type": ""},
        {"bus_id": 256, "stop_name": "Abbey Road", "stop_type": "O"},
        {"bus_id": 256, "stop_name": "Sesame Street", "stop_type": "F"},
        {"bus_id": 512, "stop_name": "Bourbon Street", "stop_type": "S"},
        {"bus_id": 512, "stop_name": "Abbey Road", "stop_type": "F"}
    ]

    Start stops: 3 ['Bourbon Street', 'Pilotow Street', 'Prospekt Avenue']
    Transfer stops: 3 ['Abbey Road', 'Elm Street', 'Sesame Street']
    Finish stops: 2 ['Abbey Road', 'Sesame Street']
    On demand stops: 1 ['Fifth Avenue']
    """
    # 1. 结构初始化
    bus_info = {}                   # {bus_id: {"start": int, "finish": int}}
    start_stops, finish_stops, o_stops = set(), set(), set()
    stop_to_buses = {}              # {stop_name: set(bus_id)}

    # 2. 单次遍历收集信息
    for entry in data:
        bus_id = entry.get("bus_id")
        stop_name = entry.get("stop_name")
        stop_type = entry.get("stop_type", "")

        # 更新线路统计
        bus_info.setdefault(bus_id, {"start": 0, "finish": 0})
        if stop_type == "S":
            bus_info[bus_id]["start"] += 1
            start_stops.add(stop_name)
        if stop_type == "F":
            bus_info[bus_id]["finish"] += 1
            finish_stops.add(stop_name)
        if stop_type == "O":
            o_stops.add(stop_name)

        # 建立站点 → 线路映射
        stop_to_buses.setdefault(stop_name, set()).add(bus_id)

    # 3. 验证每条线路恰好 1×S 与 1×F
    for bid, cnt in bus_info.items():
        if cnt["start"] != 1 or cnt["finish"] != 1:
            print(f"There is no start or end stop for the line: {bid}")
            return                          # 直接结束，不再做后续统计

    # ---------- 4. 计算换乘站（保持为 set） ----------
    transfer_stops = {
        stop for stop, buses in stop_to_buses.items() if len(buses) >= 2
    }

    # ---------- 5. 合法按需站 ----------
    correct_on_demand = sorted(
        o_stops - start_stops - finish_stops - transfer_stops
    )

    # ---------- 6. 输出 ----------
    print(f"Start stops: {len(start_stops)} {sorted(start_stops)}")
    print(f"Transfer stops: {len(transfer_stops)} {sorted(transfer_stops)}")
    print(f"Finish stops: {len(finish_stops)} {sorted(finish_stops)}")
    print(f"On demand stops: {len(correct_on_demand)} {correct_on_demand}")


if __name__ == "__main__":
    # Read input from stdin
    input_data = input().strip()
    
    # Parse JSON data
    try:
        bus_line_data = json.loads(input_data)
        validate_syntax(bus_line_data)
        find_bus_lines(bus_line_data)
        find_special_stops(bus_line_data)
    except json.JSONDecodeError:
        print("Invalid JSON input")
