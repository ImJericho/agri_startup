# Crop Market Prices Dashboard

## Overview

The Crop Market Prices Dashboard is a web application built using Streamlit that allows users to explore and analyze the market prices of various crops over time. The application fetches data from a MongoDB database and displays it in an interactive and user-friendly manner.

## Features

- **Time Series Graph with Average Prices**: Visualize the average price of crops over time.
- **Time Series Graph with Districts**: Visualize market-wise prices of crops.
- **Update Data in Atlas**: Update the crop market data in the MongoDB Atlas database.


## Deployed Application

You can access the deployed application using the following link: [Crop Market Prices Dashboard](https://vivek-agri.streamlit.app/)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/agri_startup.git
    cd agri_startup
    ```

2. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up MongoDB**:
    - Ensure you have a MongoDB instance running.
    - Update the MongoDB connection details in [mongo_dao.py](http://_vscodecontentref_/1).

4. **Run the application**:
    ```sh
    streamlit run frontend/main.py
    ```

## Usage

### Time Series Graph with Average Prices

1. Select a crop from the dropdown menu.
2. Choose the date range using the slider.
3. Click the "Submit" button to display the graph.

### Time Series Graph with Districts

1. Select a crop from the dropdown menu.
2. Select one or more markets from the multiselect menu.
3. Choose the date range using the slider.
4. Click the "Submit" button to display the graph.

### Update Data in Atlas

1. Enter the password to access the update functionality.
2. Click the "Update" button next to the commodity you want to update.
3. The application will process the update and display a success or error message.

## File Structure

- [main.py](http://_vscodecontentref_/2): The main Streamlit application file.
- [backend](http://_vscodecontentref_/3): Contains backend processing scripts.
- `common/`: Contains common utility scripts.
- `dataset/metadata/`: Contains metadata files for commodities, states, districts, and markets.
- `requirements.txt`: Lists the required Python packages.

## Dependencies

- Streamlit
- Pandas
- MongoDB
- Selenium
- Plotly

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](http://_vscodecontentref_/4) file for details.

## Acknowledgements

- Thanks to the developers of Streamlit, Pandas, and Plotly for their amazing libraries.
- Special thanks to the Agmarknet website for providing the crop market data.