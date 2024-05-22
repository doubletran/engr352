---
layout: post
title:  "Miguel Skill Log 3"
date:   2024-05-22 12:00:00 -0700

---

### What I Learned

In this phase of our "Space Walk" project, I focused on enhancing our ability to project video onto a spherical surface, specifically a weather balloon, making the experience more dynamic and user-friendly. I explored a range of tools, including a shift from our initial TouchDesigner setup to potentially more robust alternatives like custom JavaScript applications.

One significant area of development was in creating a "time-to-angle" program. This involved calculating the necessary displacement in our video projections to align with the Earth's rotation, given the fixed angles of our projectors. This mathematical modeling ensures that the video on the weather balloon matches real-time rotational movements, enhancing the realism of our celestial displays.

I used Tran's existing simulations as a primary resource, allowing me to refine our projections based on more comprehensive data. This hands-on experimentation helped me understand the complexities of dual projector setups and how to synchronize our visuals effectively with the spherical medium.

### Artifact Related to What I Learned

Here is a screenshot of the JavaScript application I developed:

![image](/engr352/assets/img/mig/javascriptExample.png)

This application is part of my exploration into creating a more effective control panel for our project. It represents the initial steps towards a more adaptable and precise projection system.

### What I Made

I created an improved version of our original control panel in TouchDesigner, integrating a new feature: the time-to-degree offset equation. This addition is crucial for calculating the exact frame or segment of our video feed that should be projected at any given moment, based on the real-time rotation of the Earth model we use.

This new control panel is designed to manage dual projector setups more efficiently, ensuring that both projectors display perfectly aligned segments of our Earth video, according to the calculated angles.

### Connection to the Project

The development of this enhanced control system directly supports the immersive experience we aim to create with "Space Walk." By accurately aligning video projections with the Earth's rotation, we ensure that viewers receive a realistic and engaging portrayal of celestial phenomena.

This technical improvement ties back to the core objectives of our project — to inspire wonder and connect viewers more deeply with the vastness of the universe through accurate and dynamic visual representations. My work on the control panel and the time-to-degree programming ensures that our project remains at the cutting edge of digital projection technology, enhancing both the artistic and scientific value of our exhibit.

---