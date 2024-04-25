---
layout: post
title:  "Tran Tran Log 1"
author: "Tran Tran"
date:   2024-04-24

---

### What I learned
At first, I thought of using equirectangular images to project the map onto the sphere. However after doing some experiments on TouchDesigner to simulate four projected images of an equirectangular image onto a sphere. I realized it wouldn’t work. I did some research on other types of projections. There are many types of Earth projections as inventions in early history to “flatten the Earth”. This was important when there was no technology, no GPS or Google Maps to show the routes. The variety of projections also depends on the use of it: whether to preserve direction, shape, distance, or shortest route. Equirectangular images are for projecting on a cylinder instead of a sphere. 
![touch designer workflow showing mercator projection](/engr352/assets/img/tran/mercator_sphere_projection.png)

### What I made
After further research into stereographic projection and discussion with Professor Hatton about finding a math formula to transform spherical vertex to the 2D image to the front, I created a model on GeoGebra to model this math problem. Since the model made easier to understand and checked for the solution, I applied basic math and trigonometry to code the formula try if the input matches with the GeoGebra’s input 

![geogebra model](/engr352/assets/img/tran/geogebra.png)
![code](/engr352/assets/img/tran/geogebra.png)

### Connection to the project
If succeeded, this formula can be used on the sphere's mesh to map the vertice and apply the color to its mapped pixel on the 2D files. Therefore, it can then be used to generate 2d images/videos to as inputs to the projectors. 

---
