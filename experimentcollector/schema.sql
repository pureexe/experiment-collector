create table if not exists experiment(
    exp_id integer primary key autoincrement,
    exp_name text,
    exp_description text,
    var_name text
);
create table if not exists fact(
    exp_id integer,
    step_id integer,
    var_name text,
    val real,
    errmsg text
);