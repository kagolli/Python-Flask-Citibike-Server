Kevin Agolli
Jeffrey Liu

After installing all the required python packages, we can run this with the command line:
    python3 server.py
    OR
    python server.py
We can visit the page at http://127.0.0.1:5000/ or localhost:5000

In this program we gather information about bike sharing. Bike sharing is beginning to grow a lot in some countries in Asia and we were curious to see how people were using bike sharing in America.

server.py:
    route: '/api'
    simply returns a string

    route: '/'
    front page, returns an analysis on a json file. After reading the file, we collect all the
    stations names and place the repsective stations with their counts. Additionally, we calculate the
    distances traveled along with the average. All the current data is in the LA area

    route '/bikes'
    allows a user to see all the open bikes in NYC. This is getting data from an open API, so in 
    addition, it will update if the user refreshes the page

home.html
    html that displays the page

numbers.html
    html that displays the live CitiBike data in New York City