# WEB-HW-04
Your goal is to implement a universal web application. You can use files as a basis.

Following the example from the lecture, create a web application with routing for two HTML pages: index.html and message.html.

Also:

Handle processed resources when the application runs: style.css, logo.png;
Organize the work with expanding on the message.html page;
Return the error.html page in case of a 404 Not Found error;
Your application runs on port 3000.
To work with expanding, create a Socket server on port 5000. The algorithm works as follows: You enter data in the form, it goes to your web application, which further processes it using a socket (UDP protocol), to the socket server. The Socket server converts the received byte string into a dictionary and saves it in the json file data.json in the storage folder, where the key of each message is the time of receipt: message datetime.now(). That is, each new message from the web application is stored with the time it was received in the storage/data.json file.
Use one file main.py to create your web application. Run the HTTP server and Socket server in different threads.

Additional task:

Configure Dockerfile and run the enterprise as a Docker container
Use the volumes mechanism to store data from the storage/data.json outside the container.
