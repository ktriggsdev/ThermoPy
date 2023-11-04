# Import pip module
import subprocess

# import all other modules
import tkinter as tk  # import tkinter module
import python_weather  # import python_weather module
import asyncio  # import asyncio module
import os  # import os module
import geopy  # import geopy module

# Get the requirements.txt file path
requirements_file_path = "requirements.txt"

# Install all requirements from the requirements.txt file
subprocess.run(["pip", "install", "-r", requirements_file_path])

root = tk.Tk()
root.title("Thermometer App")
root.minsize(300, 200)
root.config(bg="black")


def validate_city(city):
    if not city:
        return False
    geolocator = geopy.Nominatim(user_agent="temperature-app")  # initialize geopy geolocator
    try:
        location = geolocator.geocode(city)  # get location from city name
        if location:  # if location is not None
            return True
        else:
            return False
    except ValueError("City not recognised"):  # handle geopy exceptions
        return False


def separator():
    sep = tk.Frame(root, height=2, bg="black")
    sep.pack(fill="x", expand=True)


label = tk.Label(root, text="Please Enter Your City: ", font="calibri", bg="black", fg="white")

entry = tk.Entry(root, font="calibri", bg="black", fg="white", highlightbackground="white", highlightcolor="white")

entry.insert(0, "")

label.pack()
for i in range(6):
    separator()
entry.pack()
for i in range(6):
    separator()


async def get_weather(city):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)
        weather = weather.current.temperature
        return weather


def submit_entry():
    city = entry.get()
    if validate_city(city):
        weather = asyncio.run(get_weather(city))
        scale.set(weather)
        scale_color(weather)
    else:
        invalid_city = tk.Label(root,
                                text="City is incorrect, please format it as, City, State if from US, else format it" +
                                     " as City, Country", bg="black", fg="white")
        invalid_city.pack()
        invalid_city.after(5000, invalid_city.destroy)


submit = tk.Button(root, text="Submit", relief="raised", font="calibri", command=submit_entry)

submit.pack()
for i in range(6):
    separator()


def scale_color(weather):
    if int(weather) <= 0:
        scale.config(bg="lightblue1", fg="black")
    elif 0 < int(weather) <= 20:
        scale.config(bg="blue", fg="white")
    elif 20 < int(weather) <= 25:
        scale.config(bg="yellow", fg="black")
    elif 25 < int(weather) <= 32:
        scale.config(bg="orange", fg="black")
    else:
        scale.config(bg="red", fg="white")

    return weather


scale = tk.Scale(root, length=250, from_=50, to=-40, tickinterval=15,
                 orient="vertical")

scale.pack()
for i in range(6):
    separator()
if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    root.mainloop()
