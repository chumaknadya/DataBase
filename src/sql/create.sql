
CREATE TABLE customer(
  customer_id                SERIAL PRIMARY KEY,
  customer_name              VARCHAR(80) NOT NULL,
  customer_description       VARCHAR(180)
);

CREATE TABLE site_category(
   site_category_id          SERIAL PRIMARY KEY,
   name                      VARCHAR(80) NOT NULL
 );

CREATE TABLE site(
   site_id                   SERIAL PRIMARY KEY,
   site_name                 VARCHAR(80) NOT NULL,
   FOREIGN KEY (site_category_id)
   REFERENCES site_category(site_category_id)
   ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE team(
   team_id                   SERIAL PRIMARY KEY,
   team_name                 VARCHAR(80) NOT NULL,
   team_country              VARCHAR(80) NOT NULL
);

CREATE TABLE sales(
   sales_id                   SERIAL PRIMARY KEY,
   date                       DATE NOT NULL,
   cost                       INTEGER,
   FOREIGN KEY (customer_id)
   REFERENCES customer(customer_id)
   ON UPDATE CASCADE ON DELETE CASCADE,
   FOREIGN KEY (team_id)
   REFERENCES team(team_id)
   ON UPDATE CASCADE ON DELETE CASCADE,
   FOREIGN KEY (site_id)
   REFERENCES site(site_id)
   ON UPDATE CASCADE ON DELETE CASCADE
);
