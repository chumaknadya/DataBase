INSERT INTO country(name)
(SELECT md5(random()::text) FROM generate_series(1, 5));

INSERT INTO team(team_name, team_description, team_country_id)
(SELECT md5(random()::text),
        md5(random()::text),
        (SELECT country_id FROM country ORDER BY random()  LIMIT 1) FROM generate_series(1, 5));

INSERT INTO customer(customer_name, date_of_birth)
(SELECT md5(random()::text),
        (CURRENT_DATE -(random() * (CURRENT_DATE -'01.01.1850'))::int) FROM generate_series(1, 5));


INSERT INTO site_category(name)
(SELECT md5(random()::text)  FROM generate_series(1, 5));

INSERT INTO site(site_name, site_category_id)
(SELECT md5(random()::text),
        (SELECT country_id FROM country ORDER BY random() LIMIT 1) FROM generate_series(1, 5));

INSERT INTO sales(date, done, customer_id, team_id, site_id)
(SELECT     ('01.01.2000'::date -(random() * ('01.01.2000'::date -'01.01.1975'::date))::int),
            random() > 0.5,
            (SELECT customer_id FROM customer ORDER BY random() LIMIT 1),
            (SELECT team_id FROM team ORDER BY random() LIMIT 1),
            (SELECT site_id FROM site ORDER BY random() LIMIT 1) FROM generate_series(1, 5));

