CREATE TABLE automator_logs (id SERIAL PRIMARY KEY, category VARCHAR(150), start_time TIMESTAMP, end_time TIMESTAMP, error TEXT);
CREATE TABLE automator_queries (id SERIAL PRIMARY KEY, title VARCHAR(150), category VARCHAR(150), description VARCHAR(150),  status VARCHAR(150), code TEXT, created_at TIMESTAMP, updated_at TIMESTAMP, rank INTEGER);

CREATE TABLE public.users (id SERIAL PRIMARY KEY, name VARCHAR(150));

INSERT INTO public.users (name) VALUES ('Mike');
INSERT INTO public.automator_queries (code, rank, status, category) VALUES ('UPDATE users SET name = ''Andrew''', 1, 'Live', 'Users');
INSERT INTO public.automator_queries (code, rank, status, category) VALUES ('UPDATE users SET name = ''John''', 2, 'Live', 'Accounts');
INSERT INTO public.automator_queries (code, rank, status, category) VALUES ('UPDATE users SET name = ''Chris''', 3, 'Draft', 'Users');
