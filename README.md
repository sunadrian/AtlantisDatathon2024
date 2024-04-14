# Best Buyer

![building_buyer](https://github.com/sunadrian/AtlantisDatathon2024/blob/main/images/building_buyer_cover.png)

# Authors
- Marvin Bun
- Adrian Sun
- Karm Patel
- Paul Tran

# Description

Building Buyer is a web application assisting users with a budget interested in purchasing property in a specified zip code. This application leverages Meliassa's Property Assessment Dataset for data visualization of building prices per zip code. The data set consists of features such as zip code, total assessment price, property address, and more.

# Getting Started

1) Clone the repository

`git clone https://github.com/sunadrian/AtlantisDatathon2024.git`

2) Install requirements

`pip install -r requirements.txt`

3) Run application

Change the directory in the terminal to the current repository and run:

`streamlit run app.py` or  `python3 -m streamlit run app.py` 

4) Once running, input a valid zip code within Southern California(roughly OC county to LA county) and optionally add a budget to get the top 5 results. A video demonstration can be found [here](https://www.youtube.com/watch?v=nCryiT0Zlqw).

# Methods

**Data Processing**

We processed the data by dropping columns we deemed unnecessary(i.e. pool area) and extracted features relevant to the data we wanted to visualize. 

**Data Visualization**

Based on our visualizations there are 3 key takeaways:
- The average cost of housing per year follows the steady climb, describing the story of inflation and the housing crisis in 2008
- The room distribution peaks and shows that 29% of buildings in dataset have 6 rooms
-  Within Southern California, Corona Del Mar has the highest average assessed value


![Average Housing Per Year](https://github.com/sunadrian/AtlantisDatathon2024/blob/main/images/avg_housing.png)

![Mean Assessed Value by City](https://github.com/sunadrian/AtlantisDatathon2024/blob/main/images/mean_assessment.png)

![Room Distribution](https://github.com/sunadrian/AtlantisDatathon2024/blob/main/images/room_distribution.png)

