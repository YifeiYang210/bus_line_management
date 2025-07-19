import json
import re
    

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
    
    total_errors = sum(errors.values())
    
    print(f"Type and field validation: {total_errors} errors")
    for field, count in errors.items():
        print(f"{field}: {count}")


if __name__ == "__main__":
    # Read input from stdin
    input_data = input().strip()
    
    # Parse JSON data
    try:
        bus_line_data = json.loads(input_data)
        validate_syntax(bus_line_data)
    except json.JSONDecodeError:
        print("Invalid JSON input")
