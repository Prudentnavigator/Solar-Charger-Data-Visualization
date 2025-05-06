# <ins>***Victron Solar-Charger Data Visualization***</ins>

## ***Overview***
This app is designed to visualize various aspects of solar data (i.e; Victron Solar-Charger MPPT 100|50)
from the CSV file of the Victron Connect app.
It provides interactive plots, allowing users to explore different metrics such as daylight hours,
solar yield, maximum power output, charge stages, and more.


![startup screen](/ScreenShots/app_gui.png)


## ***Requirements***
- Python 3.x
- Tkinter (usually included with Python)
- Install dependencies.


    pip3 install -r requirements.txt

    or

    uv pip3 install -r requirements.txt

    or

    uv add -r requirements



## ***How to Use***
1. **Prepare Your Data**:
   Download the `SolarHistory.csv` file from the Victron Connect App (Phone/Desktop/Labtop).

2. **Run the Script**:

   
   python3 main.py
  

3. **Interact with the GUI**:

> [!NOTE]
> If it is the first time that the app is running, click the 'add data' button and choose
  the `SolarHistory.csv` file from the filedialog popup.
> Subsequently more data can be added by clicking the 'add data' button.

> [!IMPORTANT]
> Victron Connect App only stores data for up to 29 days!
  Please make sure to add data frequently to avoid data gaps.

   - Click on buttons to plot different metrics.
   - Close the application using the "X" button in the top right corner.


## ***Features***    
- **Interactive Plotting**: Users can select which metric they want to visualize by clicking on the corresponding buttons.
- **Data Check**: The script checks if it's time to add a new CSV file and alerts the user if necessary.
- **Logging**: Provides detailed logs of program execution for debugging and tracking.


### ***Contributing***
Feel free to contribute by submitting pull requests or issues. Any improvements or new features are welcome!


### ***SUPPORT/CONTACT:***
  If you have any questions, need help or want to report a bug, please contact me at tommy_software@mailfence.com.
