# Web Phishing Detection

## Tech Stacks Used

- HTML
- CSS
- Javascript
- Flask
- IBM Db2 on cloud

### Procedure to Run this application

- Clone this repository
```
$ git clone https://github.com/IBM-EPBL/IBM-Project-44647-1660725800.git
```

- Navigate to `Final_Deliverables/Source_Code/Flask` directory

- Open the cmd or terminal and install all the packages in the requirements.txt. To do that, run
```
pip install -r requirements.txt
```

- Then Create the IBM Cloud account and in that, create the IBM Db 2 Cloud Service

- Then download the digital signature file from ibm cloud db 2 service and put it in flask folder root directory

- create the .env file in the flask folder root directory. Then insert the db credentials in the following link and add this link to .env file,
```
IBMDB_URL='DATABASE=DATABASE_NAME;HOSTNAME=HOST_NAME;PORT=PORT_NUMBER;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=USER_ID;PWD=PASSWORD'
```

- To create the secret key, open the terminal, type the following and you will get the secret key
```
>>> import os
>>> os.urandom(24)
```

- Then insert the secret key in .env file.
```
SECRET_KEY= SECRET_KEY_VALUE
```

- Then, In IBM Db2 Cloud service, create the table and it's scheme like the following:

![14](https://user-images.githubusercontent.com/113231326/202849986-4a42c4f7-a378-4126-9562-101d8bb63974.jpg)

![15](https://user-images.githubusercontent.com/113231326/202849988-d0508afd-85ae-4a0a-a75a-09f5b766a2b5.jpg)

![16](https://user-images.githubusercontent.com/113231326/202849989-a25d06ac-baee-442e-a5ed-52fb599db8bf.jpg)


- For the contact form to send the queries, use the service called email.js.

- Create the account on email.js (https://www.emailjs.com/)

- Then create the mail service and template on email.js

- Then take the service id, template id and user id and paste it in contact.js (/static/js/contact.js)

- To run the application,
 ```
flask --app app --debug run
```
