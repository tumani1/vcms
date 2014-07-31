var user = {
    user: 'admin',
    pwd: 'admin',
    roles: [
        {role: "dbOwner", db: "next_tv"}
    ]
};

db.createUser(user);

