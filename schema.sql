DROP TABLE IF EXISTS vehicles;

CREATE TABLE vehicles
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type CHAR(3),
    brand VARCHAR(20),
    model VARCHAR(15),
    engine_size CHAR(4),
    production_year CHAR(4),
    market_value INTEGER(5)
    );

INSERT INTO vehicles (type, brand, model, engine_size, production_year, market_value)
VALUES 
("Saloon",   "Ford",          "Mondeo",      "1.6L",   "2012",    32425),
("Van",      "Ford",          "Transit",     "2.0L",   "2015",    27575),
("Van",      "Mercedes Benz", "Sprinter",    "3.0L",   "2014",    19700),
("SUV",      "Nissan",        "Patrol Y62",  "3.0L",   "2016",    32790),
("Hatchback","Opel",          "Corsa",       "1.4L",   "2015",    17795),
("MPV",      "Opel",          "Zafira",      "2.0L",   "2014",    34295),
("Hatchback","Renault",       "Megane",      "1.6L",   "2016",    20740),
("Van",      "Toyota",        "Hiace",       "2.8L",   "2019",    45180),
("Hatchback","Volkswagen",    "Polo",        "1.0L",   "2017",    17965),
("SUV",      "Toyota",        "RAV4",        "2.5L",   "2018",    21500),
("Saloon",   "Honda",         "Accord",      "2.0L",   "2011",    15570),
("Sport",    "Chevrolet",     "Camaro",      "2.0L",   "2017",    55690),
("MPV",      "Kia",           "Carnival",    "2.2L",   "2016",    17000),
("Estate",   "Volkswagen",    "Passat",      "2.0L",   "2019",    30500),
("SUV",      "Nissan",        "Pathfinder",  "3.5L",   "2019",    26840),
("Saloon",   "BMW",           "3 Series",    "2.0L",   "2020",    28500),
("Sport",    "Toyota",        "86",          "2.0L",   "2012",    34500)
;


DROP TABLE IF EXISTS credentials;

CREATE TABLE credentials
(
    name VARCHAR(15),
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(25) NOT NULL,
    admin VARCHAR(5) NOT NULL,
    watchlist TEXT
);


DROP TABLE IF EXISTS orders;

CREATE TABLE orders
(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20),
    vehicle_id INTEGER,
    date CHAR(10)
);


SELECT *
FROM vehicles;

SELECT *
FROM credentials;

SELECT *
FROM orders;

SELECT credentials.name, credentials.username, credentials.password, credentials.admin, vehicles.id, vehicles.brand, vehicles.model, orders.order_id, orders.date
                                FROM vehicles
                                JOIN orders
                                JOIN credentials
                                ON vehicles.id = orders.vehicle_id
                                AND orders.username = credentials.username
                                WHERE credentials.username = "c"