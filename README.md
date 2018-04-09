# Two Line Element Predictor
### Author: Tan Ren Jie
### Dated: 14 Oct 20117
[Two Line Elements (TLE)][1](https://en.wikipedia.org/wiki/Two-line_element_set) is a data format widely used to track objects orbiting Earth. Encoded in the TLE is the 6-D state vectors, [BSTAR][2](https://en.wikipedia.org/wiki/BSTAR) drag term, first and second derivative of the mean motion of the object.  <br>

There are various established propagation models such as SGP, SGP4, SDP4, SGP8 and SDP8 which are used to predict the future state vectors of the satellites. However, due to the inherent uncertainties of the TLE, this error gets propagated through time as well. For example, a typical TLE downloaded from [Celestrak][3](https://celestrak.com/)

## To run
1. Create the Resource and Imaging Mission by changing and running the creating_IM_params.py and creating_resource_params.py file (you can skip this step to run the sample simulation I have created.)
2. Open the main.py file and uncomment out the algorithm you want to use. Run it.
3. This would generate 2 .csv files per orbit (Results and Remaining targets)
4. To plot, open the subplotting.py file and change the numberOfOrbits variable to the same as the last number of the orbit.

## Plots
![plots](plotting_results.png)

# References
[1] Two Line Element https://en.wikipedia.org/wiki/Two-line_element_set
[2] BSTAR Drag Term https://en.wikipedia.org/wiki/BSTAR
[3] Celestrek
