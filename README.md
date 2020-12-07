# COVID19-Forecasting

Visualising and Simulating COVID-19 cases using statistical models
COVID-19 is affecting us to a great extent. This project uses Johns Hopkins COVID-19 dataset for visualizing the impact of the viurs in the world and also predicting the cases for the next days.

## Visualisation

Dash Plotly framework is used for visualising real / predicted cases for different countries.

## 
## Data Sources

The dataset used is available in:

- [CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)

### Run the project

* Clone this repository.
* Enter the directory where you clone it, and run the following code in the terminal (or command prompt).
```sh
docker build -t dash .
docker run -p 8050:8050 dash
```
