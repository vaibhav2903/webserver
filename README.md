Web Application Security CSEC 731

This project is for creating a  web server which is part of the course.

Hello! Welcome to my Web Server Project. Authored by Vaibhav Savala

For Testing Only HTTP_Parser
 1. Download the Repo, Then you can seen the http_parserr.py file
    run that file using these command in the same directory
 ~ $ python3 http_parserr.py

2. To Check With GET, use this command
 ~ $ python3 http_parserr.py GET_sample.txt
 
3. To Check With POST then use this command
 ~ $ python3 http_parserr.py POST_sample.txt

4. To Check With HEAD then use this command
 ~ $ python3 http_parserr.py HEAD_sample.txt

5. To Check With DELETE then use this command
 ~ $ python3 http_parserr.py DELETE_sample.txt
 
6. To Check With PUT then use this command
 ~ $ python3 http_parserr.py PUT_sample.txt


For Server.py Execution

For implementation of GET request use this commands
~ $ python3 server.py 127.0.0.1 8080
after running these command open browser and enter these
http://127.0.0.1:8080/greetings.php

For implementation of POST request use this commands
~ $ python3 server.py 127.0.0.1 8080
after running these command open browser and enter these
http://127.0.0.1:8080/D_GET_page.php?name=Vaibhav&age=25

FOR POST  request, first call the url 
http://127.0.0.1:8080/name.html

and then type in the name. Then, this will trigger a post page and the typed name will be displayed. 
The post page will be this. 
http://127.0.0.1:8080/post_name.php




I have implemented ansible in this repo as well. All of the scripts are in Ansible folder.
Run this script from inside the ansible folder. In this way, you will be able to run the scrips. 

You can use the following command to run the ansible script. 

ansible-playbook -i lab_demo.yml webserver_playbook.yml -u ubuntu  --private-key /Users/vaibhavsavala/Downloads/awscsec731web.pem

I have added the private key of my AWS EC2 instance. If you have yours, you can add it as well. Also, replace the files of lab_demo.yml with your 
ip address and user credentials and run the file. In this way, you will be able to run the ansible file without any issues.


