CREATE OR REPLACE FUNCTION process_customer_audit() RETURNS TRIGGER AS $customer_audit$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO customers_audit
            SELECT nextval('customer_id_seq'), 'D'::char, now(), user, OLD.customer_id;
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO customers_audit
            SELECT nextval('customer_id_seq'), 'U'::char, now(), user, NEW.customer_id;
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO customers_audit
            SELECT nextval('customer_id_seq'), 'I'::char, now(), user, NEW.customer_id;
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$customer_audit$ LANGUAGE plpgsql;

CREATE TRIGGER customer_audit
AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE PROCEDURE process_customer_audit();