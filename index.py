import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app_setup import app

def about():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # CaloTrack - a personal calorie tracker
        Remember that "get fit" New Year's resolution you made months ago that you promptly forgot about?
        Ready to embark on the journey of counting your calories, planning your meals and exercises,
        and becoming the best version of you that you can be?  
        Well we have the perfect app for you - CaloTrack. 
        [On average](https://www.healthline.com/nutrition/how-many-calories-per-day#section1), 
        men should be eating 2000 calories a day to lose one pound a week, whereas women should be 
        eating 1500 a day to do the same. We'll help you achieve your goals in some time!

        Our application allows you to keep track of your caloric intake and the calories you shed
        during your daily exercises. CaloTrack allows you to incrementally input foods you've eaten
        today, be it your homemade eggs and bacon in the morning, or your favorite branded foods like
        McDonald's Big Mac. Stacked bar plots will indicate the amount of calories you've consumed.
        Simultaneously, you can enter the exercises you've performed today, and the duration you've
        done it, and you can see how your hard work balances out the calories you've eaten today to 
        arrive at a net caloric intake for the day!

        ### Data Source
        CaloTrack accesses a massive online database of nutrition and fitness information provided
        by the [**Nutritionix** API](https://developer.nutritionix.com/). The Nutritionix database
        contains information on over 600 thousand foods, including grocery foods (*675,982* items from 
        *33,358* grocery brands), restaurant foods (*151,9738* items from *787* restaurants), and 
        12,955 common foods. The exercise endpoint provides users the opportunity to search across
        thousands of exercises, and our app will help calculate the calories you've burned depending
        on the exercise duration (updates to allow users to include height, weight, age, and gender
        coming soon).

        ### CaloTracker vs CaloPlanner
        Available in this project is two web applications you can utilize. Firstly, we have our 
        CaloTracker, which as described earlier, allows users to input foods they've eaten and
        exercises they've done in order to track their calorie count.  
        Secondly, we have our CaloPlanner, which allows users to specify calorie filters to search
        and plan the foods they want to eat throughout the day, as well as the exercises they want
        to perform in order to reach their caloric goals!

        # Welcome, and best of luck on your journey to health, fitness, and prosperity!

        ''', style={'paddingLeft': '5%', 'paddingRight': '5%','margin-top': '50px'})], 
            className="row")

layout = html.Div([
    about(), 
    dcc.Link('Click here to check out our calorie logger...', href='/apps/app1', 
        style={'margin-left': '40%', 'color': '#274228'}),
    html.Br(),
    dcc.Link('And click here to check out our food and exercise explorer!', href='/apps/app2', 
        style={'margin-left': '35%', 'color': '#274228'}), 
    html.Br()
    ])

# if __name__ == '__main__':
#     app.run_server(debug=True, port=1050, host='0.0.0.0')