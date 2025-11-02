db.users.aggregate([
  { $sort: { salary: 1 } },
  { $limit: 3 },
  { $project: { _id: 0, name: 1, city: 1, salary: 1 } }
])
