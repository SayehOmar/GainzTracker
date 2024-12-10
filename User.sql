CREATE TABLE user_data (
    id SERIAL PRIMARY KEY,          -- Unique ID for each record
    date DATE NOT NULL,             -- Date of the entry
    workout TEXT NOT NULL,          -- Selected workout(s)
    creatine_intake FLOAT,          -- Creatine intake in grams
    weight FLOAT                    -- User's weight in Kg
);
 