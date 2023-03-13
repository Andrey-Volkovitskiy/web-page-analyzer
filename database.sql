
    CREATE TABLE urls(
        id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        name varchar(255) NOT NULL UNIQUE,
        created_at timestamp NOT NULL
    )

    CREATE TABLE checks(
        id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        url_id bigint REFERENCES urls(id),
        status_code smallint,
        h1 text,
        title text,
        description text,
        created_at timestamp NOT NULL
    );
