<h1 id="covid19_scenarios" align="center">
  COVID19-Forecasting
</h1>
<blockquote align="center">
Visualising and Simulating COVID-19 cases using statistical models
</blockquote>

COVID-19 is affecting us to a great extent. This project uses Johns Hopkins COVID-19 dataset for visualizing the impact of the viurs in the world and also predicting the cases for the next days.

## Motivation
The outbreak of the novel coronavirus disease brought considerable turmoil all around the world. I am interested about how the spread of infectious diseases such as COVID-19 can happen. Is there anything we know about the mechanism of the spread disease?

SIR model is a mathematical model describing the structure of how the infectious disease. It is a kind of compartmental model describing the dynamics of infectious disease. The model divides the population into compartments. Each compartment is expected to have the same characteristics. SIR represents the three compartments segmented by the model.

- Susceptible
- Infectious
- Recovered

<img src="https://github.com/ahmedrachid/COVID19-Forecasting/blob/master/sir.png" />

Susceptible is a group of people who are vulnerable to exposure with infectious people. They can be patient when the infection happens. The group of infectious represents the infected people. They can pass the disease to susceptible people and can be recovered in a specific period. Recovered people get immunity so that they are not susceptible to the same illness anymore. SIR model is a framework describing how the number of people in each group can change over time.

SIR model allows us to describe the number of people in each compartment with the ordinary differential equation. β is a parameter controlling how much the disease can be transmitted through exposure. It is determined by the chance of contact and the probability of disease transmission. 
γ is a parameter expressing how much the disease can be recovered in a specific period. Once the people are healed, they get immunity. There is no chance for them to go back susceptible again.

<img src="https://github.com/ahmedrachid/COVID19-Forecasting/blob/master/ode.png" />

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
