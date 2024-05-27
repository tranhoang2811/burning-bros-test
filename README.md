# Burning Bros Technical Test

This repository contains the source code for the Burning Bros technical test. The project involves crawling data from a specified website, storing the data, and analyzing the dataset.

## Instructions

### Prerequisites

Before running the source code, ensure you have Python 3.9 or above installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Crawling Script

The crawling logic is implemented in the `crawling.py` file. To run the crawling script, execute the `main.py` file:

    python main.py

### Data Storage

The crawled data will be stored in the `data` folder. Ensure that this directory exists.

#### Data Description

| Dataset    | Description                                        |
|------------|----------------------------------------------------|
| DAY_1      | The gold price fluctuations in the past 1 day      |
| WEEK_1     | The gold price fluctuations in the past 1 week     |
| MONTH_1    | The gold price fluctuations in the past 1 month    |
| YTD        | The gold price fluctuations from the beginning of this year |
| YEAR_1     | The gold price fluctuations in the past 1 year     |
| YEAR_3     | The gold price fluctuations in the past 3 years    |
| MAX        | The gold price fluctuations through history until now |
| CUSTOM     | The gold price fluctuations in the custom time range |

### Data Analysis

The analysis for the crawled dataset can be found in the following link:

[Data Analysis Link](https://drive.google.com/drive/folders/1GhvnQ2qDRvz4QwS0Z-hQwRXqFMIcun0d?usp=drive_link)

## Repository Structure

- `crawling.py`: Contains the crawling logic to scrape data from the specified website.
- `main.py`: The entry point of the application which triggers the crawling process.
- `data/`: Directory where the crawled data is stored.
- `requirements.txt`: File containing all the required packages for the project.

## Usage

1. Ensure you have installed all the dependencies.
2. Run the `main.py` script to start the crawling process.
3. Check the `data` folder for the stored data.
4. Follow the link provided above for the analysis of the dataset.
