import flet
from flet import *
import requests
from app import secret
import datetime
api_key = secret

latitude = str(input("Enter the latitude to check: "))
longitude =str(input("Enter the longitude to check :"))

_current = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}")
# _current = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat=33.44&lon=33.44&appid={api_key}")

place = _current.json()["name"]


# list of days of the week

days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]




def main (page: Page):
    page.horizontal_alignment='center'
    page.vertical_alignment = 'center'
    #tp container

    #animation
    def  _expand(e):
        #make sure to change the control when doing the bottom portion of the app

        if e.data == "true":
            _c.content.controls[1].height = 560
            _c.content.controls[1].update()
        else:
            _c.content.controls[1].height = 660 * 0.40
            _c.content.controls[1].update()

    #define current temp
    def _current_temp():
        #this function will only fetch the temperature we require from the entered location
        #i use the json method and pass in keys for the specific value we want 
        _current_temp = int(_current.json()['main']['temp'])
        _current_temp = _current_temp - 273

        _current_weather = _current.json()['weather'][0]["main"]
        _current_description = _current.json()['weather'][0]["description"]
        _current_wind =int(_current.json()['wind']['speed'])
        _current_humidity = int(_current.json()['main']['humidity'])
        _current_feels = int(_current.json()['main']['feels_like'])
        return [
            _current_temp,
            _current_weather,
            _current_description,
            _current_wind,
            _current_humidity,
            _current_feels
        ]
    
    #defining current extra
    def _current_extra():
        #set up an empty list
        _extra_info = []

        #create a nested list of the data
        _extra = [
            [
                #getting the visibility of todays weather
                #so i divide by 1000 to get the result in km
                int(_current.json()['visibility'])/1000,
                #now we can pass in the extra info we want to display during the for loop
                "km",
                "visibility",
                "./assets/visibility.png"

            ],
            [
                #pressure data
                round(_current.json()['main']['pressure']*0.03, 2),
                #now we can pass in the extra info we want to display during the for loop
                "inHg",
                "Pressure",
                "./assets/barometer.png"

            ],
            [
                #converting unix time to readable time using datetime
                #the .fromtimestamp()method can convert unix time to datetime object and we can also add the .strfttime()method to format the time as needed

                datetime.datetime.fromtimestamp(
                    _current.json()['sys']['sunset']
                ).strftime("%m-%d-%Y %H:%I%p"),
                "",
                "Sunset",
                "./assets/sunset.jpg"
            ],
            [
                #converting unix time to readable time using datetime
                #the .fromtimestamp()method can convert unix time to datetime object and we can also add the .strfttime()method to format the time as needed

                datetime.datetime.fromtimestamp(
                    _current.json()['sys']['sunrise']
                ).strftime("%%m-%d-%Y %H:%I%p"),
                "",
                "Sunset",
                "./assets/sunrise.jpg"

                

            ]
        ]

        #now we can create the UI and pass in the data before returning

        for data in _extra:
            _extra_info.append(
                Container(
                    bgcolor="white10",
                    border_radius=12,
                    alignment=alignment.center,
                    content=Column(
                        alignment='center',
                        horizontal_alignment="center",
                        spacing=25,
                        controls=[
                            Container(
                                alignment=alignment.center,
                                content=Image(
                                    #we can start passing in the info here
                                    src=data[3],
                                    color='white'
                                ),
                                width=32,
                                height=32,
                            ),
                            Container(
                                content=Column(
                                    alignment='center',
                                    horizontal_alignment="center",
                                    spacing=0,
                                    controls=[
                                        Text(
                                            str(data[0]
                                                ) + "" + data[1],
                                                size=14,
                                        ),
                                        Text(
                                            data[2],
                                            size=11,
                                            color="white54",
                                        )

                                    ]

                                )
                            )
                        ]
                    )
                )
            )

            return _extra_info



        




#top container
    def _top():
        #we can now call the list from the function

        _today = _current_temp()

        _today_extra = GridView(
            max_extent=150,
            expand=1,
            run_spacing=5,
            spacing=5,
        )

        for info in _current_extra():
            _today_extra.controls.append(info)


        top = Container(
            width=310,
            height=660 * 0.40,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["lightblue600", "lightblue900"],

            ),
            border_radius=35,
            animate=animation.Animation(duration=450,
            curve="decelerate"),
            on_hover=lambda e: _expand(e),
            content =Column(
                alignment='start',
                spacing=10,
                controls=[
                    Row(
                        alignment='center',
                        controls=[Text(place + " CA",
                                       size=16,
                                       weight='w500',
                                       )
                                ],
                        ),

                        Container(padding=padding.only
                        (bottom=5)),
                        Row(
                            alignment='center',
                            spacing=30,
                            controls=[
                                Column(
                                    controls=[
                                        Container(
                                            width=90,
                                            height=90,
                                            image_src="./assets/cloudy.jpg"

                                        )

                                    ]
                                ),
                                Column(
                                    spacing=5,
                                    horizontal_alignment='center',
                                    controls=[
                                        Text(
                                            "Today",
                                            size=12,
                                            text_align="center",
                                        
                                        ),
                                        Row(
                                            vertical_alignment='start',
                                            spacing=0,
                                            controls=[
                                                Container
                                                      (content=Text(
                                                          #from  requests
                                                          _today[0],
                                                          size=52,
                                                          
                                                      ),
                                                ),
                                                Container(
                                                    content=
                                                    Text(
                                                        "o",
                                                        size=28,
                                                        text_align="center",

                                                    )
                                                )
                                            ],
                                        ),
                                        Text(
                                            _today[1] + "- Overcast",
                                            size=10,
                                            color='white54',
                                            text_align="center",
  
                                        ),

                                    ],
                                ),
                            ],

                        ),

                        Divider(height=8, thickness=1, color="white10"),
                        Row(
                            alignment='spaceAround',
                            controls=[
                                Container(
                                    content=Column(
                                        horizontal_alignment="center",
                                        spacing=2,
                                        controls=[
                                            Container(
                                                alignment=alignment.center,
                                                content=Image(
                                                    src="./assets/wind.png",
                                                    color="white",
                                                ),
                                                width=20,
                                                height=20,

                                            ),
                                            Text(
                                                #pass the data as string so as we can concatenate it
                                                str(_today[3]) + "km/hr",
                                                size=11,

                                            ),
                                            Text(
                                                "wind",
                                                size=9,
                                                color="white54",
                                            )
                                        ]

                                    )
                                ),
                                 Container(
                                    content=Column(
                                        horizontal_alignment="center",
                                        spacing=2,
                                        controls=[
                                            Container(
                                                alignment=alignment.center,
                                                content=Image(
                                                    src="./assets/humidity.png",
                                                    color="white",
                                                ),
                                                width=20,
                                                height=20,

                                            ),
                                            Text(
                                                #pass the data as string so as we can concatenate it
                                                str(_today[4]) + "%",
                                                size=11,

                                            ),
                                            Text(
                                                "Humidity",
                                                size=9,
                                                color="white54",
                                            )
                                        ]

                                    )
                                ),
                                Container(
                                    content=Column(
                                        horizontal_alignment="center",
                                        spacing=2,
                                        controls=[
                                            Container(
                                                alignment=alignment.center,
                                                content=Image(
                                                    src="./assets/thermometer.png",
                                                    color="white",
                                                ),
                                                width=20,
                                                height=20,

                                            ),
                                            Text(
                                                
                                                #pass the data as string so as we can concatenate it
                                                str(_today[5],) + "K",
                                                size=11,

                                            ),
                                            Text(
                                                "Feels like",
                                                size=9,
                                                color="white54",
                                            )
                                        ]

                                    )
                                )
                            ]

                        ),
                        #we can  pass in the data that will show on hover
                        _today_extra,

                                          
                                       
                    ],
            ),

        )

        return top
    
    # bottom data

    def _bot_data():
        #like the top portion, we'll be using a more effective approach
        _bot_data = []
        #range is the number of days to forecast
        for index in range(1,8):
            _bot_data.append(
                Row(
                    spacing=5,
                    alignment='spaceBetween',
                    controls=[
                        Row(
                            expand=1,
                            alignment='start',
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Text(
                                        #I want to get the days starting from tomrrow and will be using various datetime methods
                                        #calling the list defined at the top
                                        days[
                                            #call the weekday function
                                            datetime.datetime.weekday(
                                                 #call fromtimestamp function to convert unix time to readable data
                                                 datetime.datetime.fromtimestamp(
                                                     _current.json()['dt'],
                                                     
                                                 )
                                            )
                                           

                                        ]
                                    )
                                )
                            ]
                        ),
                        Row(
                            expand=1,
                            controls=[
                                Container(
                                    content=Row(
                                        alignment='start',
                                        controls=[
                                            Container(
                                                width=20,
                                                height=20,
                                                alignment=alignment.center_left,
                                                content=Image(
                                                    src=f'./assets/forecast/{_current.json()["weather"][0]["main"].lower()}.png'

                                                ),

                                            ),
                                            Text(

                                                _current.json()["weather"][0]["main"],
                                                size=11,
                                                color="white54",
                                                text_align="center",
                                            )

                                        ]
                                    )
                                )
                            ]

                        ),
                        Row(
                            expand=1,
                            alignment='end',
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Row(
                                        alignment='center',
                                        spacing=5,
                                        controls=[
                                            Container(
                                                width=20,
                                                content=Text(
                                                    int(_current.json()["main"]["temp_max"])

                                                

                                                )
                                            )
                                        ]

                                    )
                                )
                            ]


                        )
                          
                    ],
                )

            )
        return _bot_data




    def _bottom():
        _bot_column = Column(
            alignment='center',
            horizontal_alignment='center',
            spacing=25,
        )

        for data in _bot_data():
            _bot_column.controls.append(data)

        bottom = Container(
            padding=padding.only(top=280, left=20, right=20,
                                 bottom=20),
                                 content=_bot_column,

        )
        return bottom


    _c = Container(
        width=320,
        height=660,
        border_radius=35,
        bgcolor="black",
        padding=10,
        content=Stack(
            width=300,
            height=850,
            controls=[
                #first control is placed at the bottom of the stack
                _bottom(),
                _top(),
                ],
            ),
         
        )
    page.add(_c)



if __name__ == '__main__':
    flet.app(target=main, assets_dir="assets")