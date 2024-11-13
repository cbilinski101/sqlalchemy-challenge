# SQLAlchemy Climate Analysis Challenge

## Overview

This project involves using Python's SQLAlchemy library to analyze climate data from Hawaii. The goal is to perform exploratory climate analysis, retrieving temperature and precipitation data to answer specific questions and provide insights using Python data visualization libraries like Matplotlib.

## Project Structure
* README.md - Project overview
* app.py - Flask API for climate data
* climate_analysis.ipynb - Jupyter Notebook for data analysis
* Resources/
    * hawaii.sqlite - SQLite database with climate data

## Dataset

The data is provided in an SQLite database (`hawaii.sqlite`) that contains two tables:
- **Measurement**: This table holds data on precipitation, temperature, and dates.
- **Station**: This table holds information about the different weather stations.

The project queries this database to extract insights about temperature trends, precipitation patterns, and other climate metrics.

## Setup

1. Clone this repository:
   ```bash
   bash

   git clone https://github.comcbilinski101sqlalchemy-challenge.git
   cd sqlalchemy-challenge

2. Install required Python packages:
   ```bash
   bash 

   pip install -r requirements.txt

3. Ensure that hawaii.sqlite is available in the Resources folder.

## Analysis & Visualization
### 1. Precipitation Analysis

We calculate the precipitation for the last 12 months of data, visualizing it using Matplotlib. The goal is to understand seasonal variations and rainfall trends in Hawaii.

### 2. Temperature Analysis

Using data from the most active station, we calculate daily temperatures for the last year. This allows us to create:

* A histogram of temperature observations.
* Trend analysis charts to observe temperature variation over time.

### 3. Temperature Statistics

This section includes functions to calculate temperature statistics (min, max, average) over a specified date range.

## Flask API

A Flask API (app.py) is included to provide access to this data via HTTP requests. Available routes include:

* /api/v1.0/precipitation - Returns JSON precipitation data for the last year.
* /api/v1.0/stations - Returns a JSON list of weather stations.
* /api/v1.0/tobs - Returns JSON temperature data for the most active station.
* /api/v1.0/<start> and /api/v1.0/<start>/<end> - Returns temperature statistics (min, max, avg) from the specified date range.

To start the API, run:
```bash
bash

python app.py
```
## Example Queries

Here’s how you can perform some of the core queries in SQLAlchemy:

- **Get Last 12 Months of Precipitation Data:**

```python
python

most_recent_date = session.query(func.max(Measurement.date)).scalar()
last_year = dt.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)
results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year).\
    order_by(Measurement.date).all()
```
- **Return a list of stations from the dataset:**

```python
python

def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of stations from the dataset.
    results = session.query(Station.name).all()
```
## Visualization
Charts are displayed in the Jupyter Notebook to showcase trends and insights drawn from the data.

## Dependencies
The project requires the following libraries:

* SQLAlchemy
* Flask
* Pandas
* Numpy
* Matplotlib
* Jupyter Notebook

These can be installed with ```pip install -r requirements.txt```.

## Contributing

Feel free to fork this repository, make changes, and create pull requests.

## License
This project is licensed under the MIT License.

## Acknowledgments

This project was developed with the assistance of the following resources:

- **Xpert Learning Assistant** – Provided guidance on SQLAlchemy and data analysis.
- **GitLab UofT Activities** – Supplied foundational activities and exercises for analysis.
- **ChatGPT** – Assisted with code, explanations, and README formatting.

Thank you to these resources for supporting the development of this project.










