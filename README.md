# Standard Error Ellipse Calculation

In this project, the user opens *index.html* to upload a `.txt` file containing the **X and Y coordinates** of the control points of the area of interest, along with their **variance** values with respect to the X and Y axes and their **covariance** values. The input `.txt` file should follow the structure below (see also the example in **DATA.txt**):

> **Approximate Coordinates**
>
> **POINT x y**
>
> *point_name x-coordinate y-coordinate*
>
> **Variance-Covariance**
>
> *point_name*
>
> **sigmax2** *σx²_value*  
> **sigmay2** *σy²_value*  
> **sigmaxy** *σxy_value*

## Output
The output of the project consists of PNG images that depict the standard error ellipse for each control point based on its variance and covariance values. Example of an output PNG file:
<img src="docs/figs/Ellipse_B.png" alt="Description of the figure" width="800"/>
A brief description of the implemented theory can be found in [Theory of the Standard Error Ellipse](docs/Theory%20of%20the%20Standard%20Error%20Ellipse.pdf).
## Instructions
Install dependencies:
   ```bash
  pip install -r requirements.txt
   ```
Activate the uvicorn server through which backend.py is running:
 ```bash
 uvicorn backend:app --reload
   ```
Go to the local folder of the project, click *index.html* and then:
1. Upload the data txt file.
2. Click **Submit** button to plot the control points.
3. Click **Start Ellipse Calculation** to generate the output.

The output PNG images are automatically saved in the generated *Graph_Database* folder.

Methodology based on: A.M. Agatza-Balodimou, *Theory of Errors & Adjustments I*, National Technical University of Athens, School of Rural, Surveying and Geoinformatics Engineering, Athens, 2009.
