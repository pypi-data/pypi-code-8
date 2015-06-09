import pyrebase

ref = pyrebase.Firebase('https://newstestapp.firebaseio.com', 'WQJUSvWmnpraVQROTBrKQaubyCqx9UQCrWZmv2ul')


#this_last = ref.sort_by_first("articles", "time", 0, 10, None)
this_by = ref.sort_by("articles", "time", None)
print(this_by)