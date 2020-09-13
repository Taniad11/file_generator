# CSV to JSON Tree Generator

The file generator tech test comes with a mock data CSV that represents one of the many types of data that we have to deal with at Morrisons.
The challenge is to consume and transform the CSV file in to a nested JSON file which will form a tree structure.

## The desired form

From the CSV, you will see that the data follows a parent child structure. The first entry is always at the top of the tree, with the following entries being children of the previous column. The example below shows the structure of what it would look like.

```
[
  {
    "label": "Meat & Fish",
    "id": "179549",
    "link": "https://groceries.morrisons.com/browse/179549",
    "children": [
      {
        "label": "3 For £9.00 Meat & Poultry",
        "id": "179545",
        "link": "https://groceries.morrisons.com/browse/179549/179545",
        "children": []
      },
      {
        "label": "Fish",
        "id": "176741",
        "link": "https://groceries.morrisons.com/browse/179549/176741",
        "children": [
          {
            "label": "Fish Counter",
            "id": "176780",
            "link": "https://groceries.morrisons.com/browse/179549/176741/176780",
            "children": [
              {
                "label": "Salmon",
                "id": "176979",
                "link": "https://groceries.morrisons.com/browse/179549/176741/176780/176979",
                "children": []
              }
            ]
          }
        ]
      }
    ]
  }
]

```
## Deliverables

### Installation

Package can be locally installed using pip. (Please ensure requirements.txt are installed as well)

```
pip install -r requirements.txt
pip install -e .
```

### Usage

Pass the CSV file as a cmd line argument to json_generator.py. In case the CSV file is not provided, the code will bail out.
```
python json_generator.py resources/<file>.csv
```

### Approach
Code has been written by only leveraging inbuilt python packages.
* csv file is read using csv.reader
* DFS based approach to scan thru the CSV and generate the necessary tree
* json_generator leverages csv_tree.CSVTree class for returning the JSON data
* Unitests for the packages are written using pytest
* Parsing of CSV logic strictly depends on the first header row of the file. This also imposes a validation for uniform structure before proceeding with parsing of the code.
