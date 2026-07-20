from app.graph import graph

state = {

    "query": "Latest AI applications in education",

    "iteration_count": 0,

    "audit_log": [],
}

for step in graph.stream(state):

    print(step)
    
 