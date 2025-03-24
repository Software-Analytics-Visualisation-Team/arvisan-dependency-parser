# ARViSAN Dependency Parser
The `dependency_parser` is a Python tool created to parse different types of dependencies and generate input for ARViSAN. Currently, the parser supports parsing component dependencies collected from a study with Thermo Fisher Scientific. The parser can be easily extended to further support new sources of dependencies.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Folder structure](#folder-structure)
- [Input Files](#input-files)
- [Parser Configuration](#parser-configuration)
- [Example configuration](#example-configuration)
- [How to Run the Tool](#how-to-run-the-tool)

## ARViSAN repositories
ARViSAN is separated into two main and two additional repositories described below:
 - **[ARViSAN frontend](https://github.com/Software-Analytics-Visualisation-Team/arvisan-frontend)**: Responsible for rendering the graph and showing the analyses to the end user.
- **[ARVISAN backend](https://github.com/Software-Analytics-Visualisation-Team/arvisan-backend)**: Contains various endpoints for processing and executing queries to the graph database. 
- **ARVISAN dependency parser (this repository)**: Extendable Python script to preprocess software dependencies and convert them in ARViSAN's input format. Can be used to create input for visualizing confromance between expected (allowed) dependencies and actual (implementation) dependencies.
- **[ARVISAN input parser](https://github.com/Software-Analytics-Visualisation-Team/arvisan-input-parser)**:  Script created to specifically parse *OutSystems* consumer-producer data with functional domain (Application group) data into a labeled property graph, readable by Cytoscape. This script was used in the proof-of-concept version of ARViSAN.


## Installation
To install the required packages, navigate to the `DEPENDENCY_ANALYZER/dependency_parser` directory and run the following command:

```sh
pip install -r requirements.txt
```

This will install all the necessary dependencies listed in the `requirements.txt` file.

## Folder structure
```bash
dependency_parser/
│── data/                                   # Stores input data for parsers and visualization
│   │── input/                              # Example inputs for different parsers
│   │   │── subsystem_dependencies/         
│   │   │   │── dependencies.txt            # Folders containing the extracted dependencies for several releases
│   │   │   │── subsystem_mapping.csv       # Mapping from components to subsystems and subsystem groups
│   │   │   │── expected_dependencies.csv   # Expected dependencies (based on Ref Arch)
│   │── output/                             # Stores generated outputs (optional)             
│── parsers/                                # Parser scripts
│── violation_checkers/                     # Violation checker scripts
│── utils/                                  # General utility scripts
│── config.json                             # Configuration file
│── dependency_parser.py                    # Main parser script
│── requirements.txt                        # Necessary Python dependencies
│── README.md                               # Documentation
│── tests/                                  # Unit tests
```

## Input Files
The base parser requires the following input files (example data can be found in the `\data\input\<parser_type>_dependencies`) folder:

- **dependencies file**: Contains dependencies to be processed.
- **mapping.csv**: A mapping between the low level nodes and their parents. For the subsystem dependency visualization the mapping maps each ThermoFisher component to a subsystem and subsystem group. It also includes deployment information and interface details. 
- **expected_dependencies.csv (Optional)**: Lists expected/allowed dependencies to be used for violation highlighting. The `.` value signifies that any value is accepted (e.g., Category `.` means any value in the `Category` column is acceptable).

## Parser Configuration
The configuration file is a JSON file that specifies the paths to the input files and the output directory. Below are the configuration values:

- **parser_type**: Specifies the type of parser to use. Currently, this can be `subsystem_parser`.
- **dependencies_path**: The path to the file containing the dependencies between components. This file is typically located in the `data/input/<parser_type>_dependencies/` folder.
- **mapping_path**: The path to the CSV file that maps components to subsystems and subsystem groups. This file is typically located in the `data/input/<parser_type>_dependencies/` folder.
- **expected_dependencies_path**: (Optional) The path to the CSV file that lists the expected or allowed dependencies. This file is used for violation highlighting and is typically located in the `data/input/<parser_type>_dependencies/` folder.
- **output_dir**: The directory where the output files (nodes and edges CSV files) will be saved. This directory is typically located in the `data/output/<parser_type>_dependencies/` folder.

## Example configuration
```json
{
    "parser_type": "subsystem_parser",
    "dependencies_path": "C:/arvisan-dependency-parser/data/input/subsystem_dependencies/dependencies.txt",
    "mapping_path": "C:/arvisan-dependency-parser/data/input/subsystem_dependencies/subsystem_mapping.csv",
    "expected_dependencies_path": "C:/arvisan-dependency-parser/data/input/subsystem_dependencies/expected_dependencies.csv",
    "output_dir": "C:/arvisan-dependency-parser/data/output/subsystem_dependencies/"
}
```

## How to Run the Tool
To generate new input for the visualization tool (after you've setup the configuration) open a command line in the `DEPENDENCY_ANALYZER\dependency_parser` folder and run:

```sh
python -m dependency_parser {graph name}
```

Replace `{graph name}` with the actual name you want to use for the graph.

This command creates two files in `{output_dir}\{graph name}` containing the nodes and edges for the visualization tool:

- **{graph name}-nodes.csv**: Lists all nodes with their attributes.
- **{graph name}-edges.csv**: Lists all edges (dependencies) between the nodes.
