var user = {
    user: 'admin',
    pwd: 'admin',
    roles: [
        {
        role: "userAdmin",
        db: "next_tv"
      }
    ]
};

db.createUser(user);

