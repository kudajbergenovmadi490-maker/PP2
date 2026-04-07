-- ============================================================
-- Practice 8 – PhoneBook Stored Procedures
-- Run this file once in psql or pgAdmin before using phonebook.py
-- ============================================================

-- 1. Upsert: insert new contact or update phone if name already exists
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
        RAISE NOTICE 'Updated phone for %', p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone) VALUES (p_name, p_phone);
        RAISE NOTICE 'Inserted new contact: %', p_name;
    END IF;
END;
$$;


-- 2. Bulk insert with phone validation
--    Invalid rows are collected into a temp table instead of being inserted.
--    After the procedure returns, Python reads the invalid rows from
--    the temp table "invalid_contacts" within the same session.
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names  VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i       INT;
    v_name  VARCHAR;
    v_phone VARCHAR;
BEGIN
    -- Temp table to collect bad rows (visible in the same session)
    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts (
        first_name VARCHAR,
        phone      VARCHAR,
        reason     TEXT
    ) ON COMMIT DELETE ROWS;

    -- Clear previous run's data
    DELETE FROM invalid_contacts;

    FOR i IN 1 .. array_length(p_names, 1) LOOP
        v_name  := trim(p_names[i]);
        v_phone := trim(p_phones[i]);

        -- Validate: phone must start with + and contain only digits after
        IF v_phone !~ '^\+[0-9]{7,15}$' THEN
            INSERT INTO invalid_contacts VALUES (v_name, v_phone, 'Invalid phone format');
            CONTINUE;
        END IF;

        -- Validate: name must not be empty
        IF v_name = '' THEN
            INSERT INTO invalid_contacts VALUES (v_name, v_phone, 'Empty name');
            CONTINUE;
        END IF;

        -- Upsert valid row
        IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = v_name) THEN
            UPDATE phonebook SET phone = v_phone WHERE first_name = v_name;
        ELSE
            INSERT INTO phonebook(first_name, phone) VALUES (v_name, v_phone)
            ON CONFLICT (phone) DO NOTHING;
        END IF;
    END LOOP;
END;
$$;


-- 3. Delete contact by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR, p_by VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_by = 'name' THEN
        DELETE FROM phonebook WHERE first_name = p_value;
    ELSIF p_by = 'phone' THEN
        DELETE FROM phonebook WHERE phone = p_value;
    ELSE
        RAISE EXCEPTION 'p_by must be ''name'' or ''phone''';
    END IF;
END;
$$;
