import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app_setup import app
import base64


def about():
    return html.Div(children=[dcc.Markdown('''
    # About CaloTrack, by Lauren To and Jason Chan

    #### Project Executive Summary 
    We've created an interactive dashboard for users to explore and experiment with their dietary and exercise 
    habits. The main database that we use has the nutritional facts of a lot of different common foods, so we want 
    users to be able to add or select food items, and update a caloric graph accordingly that provides an estimate 
    of the number of calories/macros in each food item. Furthermore, our tools allow users to access exercise data 
    and estimate calories burned from a certain duration of exercise. The combination of these two makes up our 
    CaloTrack app, which allows users to track their total caloric intake throughout the day. Secondly, we've created 
    a CaloPlanner app which allows users to plan out their caloric intake throughout the day. Users can search by 
    food groups, filter by calories, as well as search and filter exercises. At the end of this project, we hope 
    users will have a better sense of their nutritional intake, as well as some ideas as to how they can change 
    their diet and exercise habits to reflect their personal goals and interests.

    #### Datasets, Nutritionix API
    We are using two nutrition and exercise datasets using the Nutritionix API (a nutrition app). The nutrition 
    database contains the nutritional facts of around 13000 common foods and, and seems to be updated anywhere between 
    multiple times daily to every 7 days. Similarly, the exercise data can be accessed via API calls and provides 
    estimates for the number of calories burned over various exercises - it uses an internal natural language processor 
    to process queries. Furthermore, optional demographics can be provided such as age, gender, weight, to generate 
    a more accurate prediction of calories burned. Our data was processed into Google Cloud Platform's BigQuery and 
    stored as SQL tables. An initial set of data from the API was created, but our dataset updates as users query the 
    API for results that do not already exist in our dataset. The corresponding query results are integrated with our 
    BigQuery tables and are made immediately available for the user to use.

    #### Next Steps, and Similar Projects
    Possible next steps in our project is to upgrade the user interface and improve the user experience. We currently
    only show caloric information for foods and exercises. However, the API allows us to access much more nutrient
    information of foods, including all nutrition information typically shown in nutrition labels. We could upgrade our
    application to allow users to see and keep track of those nutrients as well, so that our project is not just for
    counting calories, but also for tracking daily nutrition intake.
    There are other applications that are similar to the one we are building. For example, there are:
    * [Nutritionix App](https://www.nutritionix.com/app)
        * Nutritionix has their own app for tracking and storing foods that users eat to keep track of calories/macros.
        In particular, they have two rest API’s covering both branded foods (e.g. McDonalds, Whole Foods, etc), versus
        regular common foods (e.g. scrambled eggs, bacon).
    * [MyFitnessPal](https://www.myfitnesspal.com/)
        * MyFitnessPal is a similar app/website partnered with UnderArmour that allows users to track their calories
        through inputting different foods and exercises. They also have many branded and common foods available in their
        database, as well as a database of different exercises.
    * [Lose It!](https://loseit.com/)
        * Lose It! is an app that again allows users to log food and exercise and track their progress in achieving a
        personal weight goal. It also allows users to upload their Ancestry or 23andMe DNA ancestry to see how their
        genetics affect their weight gain.

    ## Additional Project Details

    #### Development Process, Data Acquisition, Caching, ETL Processing, Database Design

    First we establish API access to **Nutritionix** has been established by obtaining a private key. We wrote methods
     in order to query particular foods (common foods and branded foods) and obtain information like serving size,
     serving quantity, and number of calories. We also wrote methods to query particular exercises and obtain information
     on duration and number of calories. The JSON results from the API calls are processed into dataframes and saved 
     into csv files, with methods written to integrate new results with the original results stored in the csv files.

    A connection with **GCP BigQuery** and **GCP Cloud Storage** was established through API, and we built a database
    with three tables, corresponding to the three types of data we are storing. We have the **\"common\" table**, for
    common foods, has about 4500 rows currently, and **“branded” table**, for branded foods, such as the McDonald’s
    Big Mac, which has about 2400 rows. Both of these tables include fields `food_name, serving_unit, serving_qty,
    nf_calories`, while branded also has fields `brand_name_item_name, brand_name` to specify the brand. Our third table,
    the **\"exercises\" table**, has about 50 rows currently, and contains fields `name, duration_min, nf_calories`.

    On the front end, where the application is hosted in a web browser, we have the data tables pulled down from BigQuery
    and stored in local instances of dataframes. In both of our apps, CaloTracker and CaloPlanner, users see a stacked
    bar plot consisting of food and exercise items they have chosen. Three bar plots will be displayed; the first a
    stacked bar of the calories of the foods the user has eaten, the second, a stacked bar of the calories of exercises
    the user has performed, and a final bar representing the total net caloric intake of the user.

    Our visualizations interact with the user such that they can query and filter our table using natural language to
    select the desired foods or exercises. If the food/exercise they are looking for is already in our data tables,
    they can select that item through the drop down tables, and the stacked bar plot updates with the calorie amount of
    that food or exercise, as well as updating the total calorie intake bar.

    If the food or exercise they are looking for is not already in our table, they can simply input that item into a
    separate provided input box. At that point, the user's input is used to query the Nutritionix API and search for the
    appropriate information. The returned information is formatted into a table, saved as a csv, uploaded to GCP Storage,
    and from there is appended to our BigQuery tables. Finally, the in-browser dataframe is updated to include this new
    query, and the user is able to access and filter for that item in the original location. This dataframe that is
    pulled down from BigQuery is cached, and all of the users' iteraction with the dataframe is from cached data. The
    tables are only updated when a user inputs a new food/exercise query that doesn't already exist in our table, and
    the above process repeats.

    #### Final Technology Stack''', style={'paddingLeft': '5%', 'paddingRight': '5%', 'margin-top': '50px'}),
    html.Img(src = "/assets/techstack.png", style={'textAlign': 'center', 'width': '660px', 'margin-left': '22%'}),
    dcc.Markdown('''
    #### Code Links
    In the following links, you will find static versions of our ETL python code, which shows how our data was initially
    obtained, how we created our tables, integrated with GCP BigQuery, and how our code interacts with new user queries
    to update our database.

    *If you are unable to access the code due to privacy permissions reasons, simply email* **jason_chan1@brown.edu**
    *or* **lauren_to@brown.edu** *to request access*. We had to make our GitHub repository private for credential
    security reasons.
    * [Initial Data Retrieval](https://github.com/csjasonchan357/calotrack-1050-final/blob/master/ETL_initial.ipynb)
    * [Initial GCP BigQuery Table Setup](https://github.com/csjasonchan357/calotrack-1050-final/blob/master/ETL_GCP_initial.ipynb),
    * [Active ETL Code](https://github.com/csjasonchan357/calotrack-1050-final/blob/master/ETL.py)
    * [Active ETL Integration with GCP Code](https://github.com/csjasonchan357/calotrack-1050-final/blob/master/ETL_GCP.py)
    
    Below, you will find links to static versions of our visualization and enhancement code, which built the initial
    plots that you see on our applications. You will also find code for our applications, which provide the functionality
    that you see here on this website.
    * [Visualization Code](https://github.com/csjasonchan357/calotrack-1050-final/blob/master/visualization.ipynb)
    * [Enhancement Code](https://github.com/csjasonchan357/calotrack-1050-final/blob/master/enhancement.ipynb)
    * [CaloTracker App Code](https://github.com/csjasonchan357/calotrack-1050-final/blob/master/apps/app1.py)
    * [CaloPlanner App Code](https://github.com/csjasonchan357/calotrack-1050-final/blob/master/apps/app2.py)''', 
    style={'paddingLeft': '5%', 'paddingRight': '5%','margin-bottom': '25px'})])

layout = html.Div([about(), 
        dcc.Link('Return Home', href='/app', 
        style={'color': '#274228'})])