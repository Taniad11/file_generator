"""CSV tree libraries

Consists of libraries to parse CSV values to and generate a JSON tree.
"""

import re
from typing import Dict, List, Tuple

from csv2json_gen.exceptions import InvalidCSVFormat

Node = Dict[str, str]
NodeList = List[Node]
NodeResult = Tuple[Node, bool]


def valid_key(key: str) -> str:
    """Validate if key is a known keyword from pre-defined dictionary.

    :param key: keyword to validate
    :type img: str
    :return: True if exists
    :rtype: bool
    :raises InvalidCSVFormat: if key is not known
    """
    keywords = {"link": ["URL"], "label": ["Name"], "id": ["ID"]}

    for k, value in keywords.items():
        if key in value:
            return k
    raise InvalidCSVFormat(f"Unknown Column Name : {key}")


def level_exists(node: Node, node_list: NodeList) -> NodeResult:
    """Validate if a Node exists in a branch of the Tree.

    Compares all keys except "children" inside a node.
    Will return back the same value with False if search fails.

    :param node: node to be searched inside the tree
    :type node: Node
    :param node_list: branch of a tree or entire tree
    :type node_list: NodeList
    :return: Existing Node and search result
    :rtype: NodeResult
    """
    for data in node_list:
        result = []
        for k in data:
            if k != "children":
                result.append(data[k] == node[k])
        if all(result):
            return data, True
    return node, False


def level_format(head_row: List[str]) -> List[str]:
    """Uses head row of CSV to determine order of parsing for each CSV row.

    :param head_row: Header row of the CSV file
    :type head_row: List[str]
    :return: order in which values are supposed to be parsed in a row.
    :rtype: List[str]
    """
    order_decider = None
    order = []

    for head in head_row[1:]:
        if not head.startswith("Level"):
            raise InvalidCSVFormat(
                f"Column {head} is not prefixed with 'Level n' keyword"
            )

        level, col_name = re.findall(r"Level (\d*)\W*(\w*)", head).pop()
        col_name = valid_key(col_name)

        order_decider = level if not order_decider else order_decider
        if level == order_decider:
            order.append(col_name)
        else:
            break
    return order


def generate_branch(row: List[str], order: List[str]) -> NodeList:
    """Based on a CSV row value generate a branch of a Tree

    :param row: CSV row
    :type row: List[str]
    :param order: order in which a CSV row is to be parse
    :type order: List[str]
    :return: A list of dictionary nodes representing branch of the Tree.
    :rtype: NodeList
    """
    lvl_node = []

    for i in range(1, len(row), len(order)):
        lvl_values = row[i : i + len(order)]
        if all(lvl_values):
            node = dict(zip(order, lvl_values))
            node["children"] = []
            lvl_node.append(node)

    return lvl_node


def generate_tree(csv_data: List[List[str]], order: List[str]) -> List[NodeList]:
    """Generate a JSON tree based on CSV values passed as a 2D array

    :param csv_data: CSV data entries
    :type row: List[List[str]]
    :param order: order in which a CSV row is to be parse
    :type order: List[str]
    :return: JSON tree
    :rtype: List[NodeList]
    """
    tree = []

    for row in csv_data:
        branch = generate_branch(row, order)
        if not branch:
            continue

        branch[0], root_result = level_exists(branch[0], tree)

        for i in range(len(branch) - 1):
            branch[i + 1], result = level_exists(branch[i + 1], branch[i]["children"])
            if not result:
                branch[i]["children"].append(branch[i + 1])

        if not root_result:
            tree.append(branch[0])
    return tree
