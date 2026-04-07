-- ============================================================
-- Practice 8 – PhoneBook Functions
-- Run this file once in psql or pgAdmin before using phonebook.py
-- ============================================================

-- 1. Search contacts by pattern (name or phone)
CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT pb.id, pb.first_name, pb.phone
        FROM phonebook pb
        WHERE pb.first_name ILIKE '%' || p_pattern || '%'
           OR pb.phone      ILIKE '%' || p_pattern || '%'
        ORDER BY pb.first_name;
END;
$$ LANGUAGE plpgsql;


-- 2. Paginated query (LIMIT / OFFSET)
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT pb.id, pb.first_name, pb.phone
        FROM phonebook pb
        ORDER BY pb.id
        LIMIT p_limit
        OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
