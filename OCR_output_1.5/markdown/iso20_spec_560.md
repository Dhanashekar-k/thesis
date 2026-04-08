<长期以来>

In the example above, the first PriceRule starts at 0 kW, and goes up to 1 kW. The second PriceRule goes from 1 kW to 2 kW. The third PriceRule starts at 3 kW and goes upwards.

When StackedPrices is false, the cost would be calculated as:

Total cost =  $ (1\ \text{kW} \times \0.13/\text{kWh}) + (3\ \text{kW} \times \0.28/\text{kWh}) = \0.97. $

When the PriceAlgorithm is 2-PeakPower, the cost would be calculated as:

Total cost =  $ (1\ \text{kW} \times \0.13/\text{kWh}) + (3\ \text{kW} \times \0.28/\text{kWh}) = \0.97. $

When the PriceAlgorithm is 3-StackedEnergy, the cost would be calculated as:

Total cost = (1 kW * $0.13/kWh) + (1 kW * $0.13/kWh) + (1 kW * $0.25/kWh) + (1 kW * $0.28/kWh) = $0.66.