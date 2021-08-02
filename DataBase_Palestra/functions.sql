CREATE PROCEDURE test(ciao INT) AS $$
    BEGIN
        FOR i IN 0..5 LOOP
            INSERT INTO corsislot VALUES(ciao, i);
        END LOOP;
    END;
$$ LANGUAGE 'plpgsql';