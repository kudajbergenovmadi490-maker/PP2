-- Procedure 1: insert or update a contact
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- Procedure 2: insert many contacts, skip invalid phones
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(names VARCHAR[], phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts(
        first_name VARCHAR,
        phone VARCHAR,
        reason TEXT
    ) ON COMMIT DELETE ROWS;

    DELETE FROM invalid_contacts;

    FOR i IN 1 .. array_length(names, 1) LOOP
        IF phones[i] !~ '^\+[0-9]{7,15}$' THEN
            INSERT INTO invalid_contacts VALUES (names[i], phones[i], 'Invalid phone');
        ELSIF names[i] = '' THEN
            INSERT INTO invalid_contacts VALUES (names[i], phones[i], 'Empty name');
        ELSE
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = names[i]) THEN
                UPDATE phonebook SET phone = phones[i] WHERE first_name = names[i];
            ELSE
                INSERT INTO phonebook(first_name, phone) VALUES (names[i], phones[i]);
            END IF;
        END IF;
    END LOOP;
END;
$$;


-- Procedure 3: delete a contact by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(value VARCHAR, by_what VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF by_what = 'name' THEN
        DELETE FROM phonebook WHERE first_name = value;
    ELSIF by_what = 'phone' THEN
        DELETE FROM phonebook WHERE phone = value;
    END IF;
END;
$$;
