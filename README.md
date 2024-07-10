
# Cow Cure

Cow Cure is a web-app project developed by Poojya Gupta, Bhavya Parmar and Dikshita Bargoda that helps farmers quickly and accurately identify potential health issues in their cattle, enabling timely and appropriate interventions to ensure their health and productivity.


## Authors

- [@Bhavya Parmar](https://www.github.com/bhavya-parmar)
- [@Poojya Gupta](https://www.github.com/poojyagupta)
- @Dikshita Bargoda


## Features

- 3-Step Cattle Disease Finder tool - uses a bipartite graph to match input symptoms to the disease
- Detailed information about the disease (Symptoms, Causes, Treatments, Preventions)
- Flask Backend
- Queries Form connected to Google Sheets
- Search disease bar with auto-suggest
- Fully Responsive
- Clean UI


## Deployment

Once you have downloaded the repository ensure that it's structure is as shown below:

```bash
Website Codes/
│
├── app.py
├── Cow Diseases.xlsx
├── README.txt
├── LICENSE.txt
|
├── templates/
│   ├── all_diseases.html
│   ├── disease_info.html
│   ├── disease.html
│   ├── index.html
│   ├── symptom1.html
│   ├── symptom2.html
│   ├── symptom3.html
|
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   ├── about-img.png
│   │   ├── bg img.png
│   │   ├── Cow cure bar dark transparent.png
│   │   ├── Cow cure logo light transparent.png
│   │   ├── disease-finder-bg-img.png
│   │   ├── home-img.png
│   │   ├── image 1.png
│   ├── js/
│   │   ├── script.js
│   │   └── multi.js
```
Then copy the path of Cow Disease.xlsx file.

Then open the app.py file and then in line 9:

```bash
df = pd.read_excel(r"Website Codes\Cow Diseases.xlsx", sheet_name="All in one")
```
Replace "Website Codes\Cow Diseases.xlsx" with your copied path.

```bash
df = pd.read_excel(r"Your_Copied_Path\Cow Diseases.xlsx", sheet_name="All in one")
```
Ensure that you have the following libraries installed in Python :
- pandas
- networkx
- flask (Framework)
- openpyxl

Now you are all set to go. Run the app.py file and open the live server given in the output.
## Queries Sheet

Link to the Google sheet containing the queries form submission data:
https://docs.google.com/spreadsheets/d/1TPleohFeJbJ9fZ1lEk3sKo0SwRtRAmOrdKamjNocNUg/edit?usp=sharing

## Contributing

Contributions are always welcome!

If you would like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.


## License

See the LICENSE.txt file for details.


