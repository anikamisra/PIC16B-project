<h1 align="center">Chordy</h1>

  <p align="center">
    Project for PIC16B Winter 2024 group 1. 
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-chordy">Welcome</a></li>
    <li><a href="#chordy-setup">Setup</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#sources-and-citations">Sources and Citations</a></li>
  </ol>
</details>


<!-- ABOUT CHORDY -->
## About Chordy

Welcome to chordy, a web app that allows you to search for an artist, their songs, and display backtrack! 

<!-- ABOUT CHORDY -->
## Chordy Setup

This is our git repository for the project: https://github.com/anikamisra/PIC16B-project

Begin by cloning and unziping the repository in your local computer. Then open the project in your preferred IDE (I am using Pycharm and recommends it)

Add a file named **.env** with the database passwords next to app.py. The file should include and only include the following line:

```console
DB_PSWD=0YnrLGO4d5dxjtSc
```

Now open terminal on your IDE and enter the following commands (note that you should be currently at the PIC16B-project directory):

```console
cd chord_scraper
```
You may need to 
```console
python -m pip install "pymongo [srv]"
```
Also, make sure to pip install the following packages: 
- flask
- flask_cors
- dotenv
- midiutil
- mingus
- pandas
- pychord
- Selenium
- scrapy

And pip install any other non-existing or non-updated packages. This may depend on your current environment. 

When there is no warnings (and you are at the chord_scraper directory), 
```console
ls
```
to check if you see **app.py**. If you do, run the following command:
```console
flask run
```
You should see something like this on your terminal (note that mongoDB connection works best when using UCLA WIFI, other connections may lead to timeout error):
```console
(PIC16B-24W) athena@Athenas-MacBook-Pro chord_scraper % flask run
mongodb+srv://Chordy:0YnrLGO4d5dxjtSc@cluster0.pirmgae.mongodb.net/
Pinged your deployment. You successfully connected to MongoDB!
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
Now you have Chordy running on http://127.0.0.1:5000!

<!-- CONTRIBUTORS -->
## Contributors

Athena, Izzy, and Anika


<!-- SOURCES AND CITATIONS -->
## Sources and Citations
* https://medium.com/@stevehiehn/how-to-generate-music-with-python-the-basics-62e8ea9b99a5
* https://tedboy.github.io/flask/generated/flask.send_file.html

