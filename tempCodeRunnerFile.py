c.executemany("INSERT INTO City VALUES (?,?,?,?,?,?,?,?)", cities)

c.executemany("INSERT INTO Animal VALUES (?,?,?,?,?,?,?)", animals)

c.executemany("INSERT INTO Plant VALUES (?,?,?,?,?,?)", plants)

c.executemany("INSERT INTO Tourist VALUES (?,?,?,?,?,?)", tourist_spots)

c.executemany("INSERT INTO Cities_Loc VALUES (?,?,?,?)", cities_loc)

c.executemany("INSERT INTO Tourist_Loc VALUES (?,?,?,?,?)", tourist_loc)

print('Command executed successfully!!!')