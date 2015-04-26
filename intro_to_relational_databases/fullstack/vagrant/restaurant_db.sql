

CREATE TABLE restaurants (
       id serial primary key,
       name text not null
);

CREATE TABLE menu_item (
       item_id serial primary key,
       name text not null,
       description text,
       course text,
       price money not null,
       restaurant int references restaurants(id)
);
