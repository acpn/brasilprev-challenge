<p align="center">
  <img width="200" height="163" src="./assets/logo-brasilprev.svg">
</p>
<h1 align=center>BrasilPrev Challenge</h1>
<p align="center">Python API to simulate an virtual store CRUD (http://api.antonio-paes.com/health-check)</p>

## :computer: Tech:
- Python
- Flask
- SqlAlchemy
- Terraform
- Mysql
- Docker
- AWS

## :running: Create the database in AWS (RDS):
```shell
  # Clone this repository
  - git clone git@github.com:acpn/brasilprev-challenge.git

  # Enter in the project directory
  - cd [project folder]/terraform

  - The file credentials.tf holds the account destination credentials, put your credentials there and run (this could take some time, so just get a cup of coffe and relax):

  # Start terraform
  - terraform init
  - terraform apply
```

If everything it's ok you may have your Database created.

## :running: Create the infrastructure in AWS (ECS):
This section it's necessary only if you want to execute the project in your local machine, otherwise github actions will do all the process for you at each push to your repository.

Before make the API available in ECS you've to create and Bucket in AWS, to do that follow this tutorial: https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html, with the bucket created copy the name you gave and paste in the file ``providers.tf`` in the backend section.

After that just go through the project folder in ``terraform/ecs`` and run:

```shell  
  - terraform init
  - terraform apply
```

## Migrations
If your database was created and everything it's up and running the it's migration time :)

The file ``src/datbase/models.py`` holds the ability to create your tables, to do that just run:

```shell
  - python src/datbase/models.py db init
  - python src/datbase/models.py db migrate
  - python src/datbase/models.py db upgrade
```

After this sequency your tables should be created, to be sure of that just connect to your database in your favorite query builder.


## :running: Run the API
In the root folder has a file called .env.example, rename that file to .env and edit the variables inside to your correct values.

In terraform folder, file credentials.tf I set some default values to credentials, if you want just use them, but make sure the same values in credentials.tf it's in you .env file.

This credentials will be used to create your RDS instance and connect to the database.

I put a file called deploy_container.sh in the root repository to facilitate the API execution. In your terminal just run:

```shell
  - ./deploy_container.sh
```

## Functions
The API it's allowed to perform some operations that will be described as follow:

 - 0 - Check the API helth (necessary to terraform verify if everything it's ok when the infrastructure it's built)
 - 1 - Create, update, list and delete clients
 - 2 - Create, update, list and delete products
 - 3 - Create, update, list and delete orders


## Routes
The routes from the API it's (assuming localhost as your host):

0 - Status API
 - Check status API: GET - ``localhost:5000/health-check``

1 - Clients
 - Authenticate client: POST - ``localhost:5000/auth/login`` (necessary to pass email and password as a json file)
 - Create a new client: POST - ``localhost:5000/clients`` (necessary to pass name, email and password as a json file)
 - Update an given client: PUT - ``localhost:5000/clients/id`` (necessary to pass name, email, password as a json file and id as route param)
 - List all Clients: GET - ``localhost:5000/clients``
 - Remove an given client by ID: DELETE - ``localhost:5000/clients/id``  (necessary to pass an ID as route param)

2 - Products
 - Create a new product: POST - ``localhost:5000/products`` (necessary to pass description, price and quantity as a json file)
 - Update an given product: PUT - ``localhost:5000/products/id`` (necessary to pass description, price and quantity as a json file and id as route param)
 - List all products: GET - ``localhost:5000/products``
 - Remove an given product by ID: DELETE - ``localhost:5000/products/id`` (necessary to pass an ID as route param)

3 - Orders
 - Create a new order: POST - ``localhost:5000/orders`` (necessary to pass id_client, id_product and quantity as a json file)
 - Update an given order: PUT - ``localhost:5000/orders/id`` (necessary to pass the new quantity as a json file and id as route param, the total value will be updated automatic)
 - List all orders: GET - ``localhost:5000/orders``
 - Remove an given order by ID: DELETE - ``localhost:5000/orders/id`` (necessary to pass an ID as route param)


## Testing
To make your life a piece of cake I put a file inside the directory insomnia with the routes already setting up, so just download insomnia (https://insomnia.rest/) and import this file using the the option Import/Export > Import Data and then select From Clipboard (before that make sure you copy the data inside insomnia_routes file).

After that just try different routes and combinations to see how the API works.


## Testing Live
To turns things more efficient and nice as my point of view, all this project it's in a CI/CD process, so all this it's already running in AWS and you could access that by this link:

- http://api.antonio-paes.com/health-check

This link provides the last commited container image.

And then you can access all the other routes following the host: http://api.antonio-paes.com/<route_name>.

To be easy for you just use the step from insomnia configuration and change the host to http://api.antonio-paes.com/, that way all the routes should be working for you.


## Remarks

Some points about the code organization still bothering me, the code inside src could be improved refactoring the routes in specific files according to each responsability.

The GET method from orders could be improved to return the client name and the product description to be more readable.

The database creation could be integrated to infrastructure creation so with just one command you have your database and all infrastructure.


## :fork_and_knife: As yours

 - Fork this repository and setting up the env variables in your github account, sent a push to your forked repository and watch the magic happens!

If something goes wrong contact-me and we'll fix the problems.

Cheers!!
