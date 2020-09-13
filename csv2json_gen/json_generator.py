"""Runner script to accept CSV file and dump a JSON tree"""

import json
import sys
from csv import reader

from csv2json_gen import get_logger
from csv2json_gen.csv_tree import generate_tree, level_format
from csv2json_gen.exceptions import EmptyCSV, InvalidArgs, InvalidCSVFormat

logger = get_logger("json_generator")


def read_csv(csv_file):
    """Return a 2D array of CSV entries"""
    data = []
    with open(csv_file, "r") as file_h:
        for line in reader(file_h):
            data.append(line)

    if not data:
        logger.error("Data after reading the CSV: %s", str(data))
        raise EmptyCSV("%s is empty!!" % csv_file)

    logger.info("No. of entries identified : %s", str(len(data)))
    return data


def main():
    """Main Runner method"""
    try:
        if len(sys.argv) != 2:
            logger.error("Invalid argument set provided: %s", sys.argv)
            raise InvalidArgs("Please provide a csv file!!")

        csv_data = read_csv(sys.argv[1])

        order = level_format(csv_data.pop(0))
        logger.info("Parsing order for generation tree: %s",order)

        data = generate_tree(csv_data, order)
        logger.info("JSON tree parsing done!")

        with open("data.json", "w") as file_p:
            json.dump(data, file_p, indent=4)

        logger.info("JSON file logged. Open data.json to view output")
    except InvalidArgs as exc:
        logger.exception(str(exc))
    except EmptyCSV as exc:
        logger.exception(str(exc))
    except FileNotFoundError as exc:
        logger.exception(str(exc))
    except InvalidCSVFormat as exc:
        logger.exception(str(exc))


if __name__ == "__main__":
    main()
