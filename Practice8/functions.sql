-- Function 1: search contacts by name or phone
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT phonebook.id, phonebook.first_name, phonebook.phone
        FROM phonebook
        WHERE phonebook.first_name ILIKE '%' || pattern || '%'
        OR phonebook.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- Function 2: get contacts with pagination
CREATE OR REPLACE FUNCTION get_contacts_page(lim INT, off INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT phonebook.id, phonebook.first_name, phonebook.phone
        FROM phonebook
        ORDER BY phonebook.id
        LIMIT lim
        OFFSET off;
END;
$$ LANGUAGE plpgsql;
