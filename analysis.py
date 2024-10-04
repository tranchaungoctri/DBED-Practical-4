data_file = "movies.nt"
language_tag = "@en-US"
line_ending = " ."

predicate_has_type = "<http://adelaide.edu.au/dbed/hasType>"
predicate_has_name = "<http://adelaide.edu.au/dbed/hasName>"
predicate_has_actor = "<http://adelaide.edu.au/dbed/hasActor>"
uri_person = "<http://adelaide.edu.au/dbed/Person>"
predicate_prefix = "<http://adelaide.edu.au/dbed/has"


def _is_uri(some_text):
    # simple text without regular expressions
    if some_text.find(' ') >= 0:
        return False
    return some_text.startswith("<") and some_text.endswith(">")

def _is_blank_node(some_text):
    # simple text without regular expressions
    if some_text.find(' ') >= 0:
        return False
    return some_text.startswith("_:")

def _is_literal(some_text):
    return some_text.startswith("\"") and some_text.endswith("\"")
    
def _parse_line(line):
    # this could be done using regex
    
    # for each line, remove newline character(s)
    line = line.strip()
    #print(line)
    
    # throw an error if line doesn't end as required by file format
    assert line.endswith(line_ending), line
    # remove the ending part
    line = line[:-len(line_ending)]
    
    # find subject
    i = line.find(" ")
    # throw an error, if no whitespace
    assert i >= 0, line
    # split string into subject and the rest
    s = line[:i]
    line = line[(i + 1):]
    # throw an error if subject is neither a URI nor a blank node
    assert _is_uri(s) or _is_blank_node(s), s

    # find predicate
    i = line.find(" ")
    # throw an error, if no whitespace
    assert i >= 0, line
    # split string into predicate and the rest
    p = line[:i]
    line = line[(i + 1):]
    # throw an error if predicate is not a URI
    assert _is_uri(p), str(p)
    
    # object is everything else
    o = line
    
    # remove language tag if needed
    if o.endswith(language_tag):
        o = o[:-len(language_tag)]

    # object must be a URI, blank node, or string literal
    # throw an error if it's not
    assert _is_uri(o) or _is_blank_node(o) or _is_literal(o), o
    
    #print([s, p, o])
    return s, p, o

def _compute_stats():
    # ... you can add variables here ...
    n_triples = 0 #total of triples
    n_people = set() #number of distinct people mentioned in ANY role
    actor_movie_count = {} #map each actor to movie they are in

    #variables to calculate highweight
    a_weight = {} #map actor to weight
    a_names = {} #map actor URL to name
    a_order = {} #track actor's order
    
    # open file and read it line by line
    # assume utf8 encoding, ignore non-parseable characters
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            # get subject, predicate and object
            s, p, o = _parse_line(line)
            
    ###########################################################
    # ... your code here ...
    # you can add functions and variables as needed;
    # however, do NOT remove or modify existing code;
    # _compute_stats() must return four values as described;
    # you can add print statements if you like, but only the
    # last four printed lines will be assessed;
    ###########################################################
            #increment number of triples
            n_triples+= 1
            
            #track district person
            if  _is_uri(s) or _is_blank_node(s):
                n_people.add(s)

            # Store actor names
            if p == predicate_has_name:
                a_names[s] = o.strip('"')
        
            #count movies per actor
            if p == predicate_has_actor and (_is_uri(o) or _is_blank_node(o)):
                if o not in actor_movie_count:
                    actor_movie_count[o] = 0
                    a_weight[o] = 0

                actor_movie_count[o] += 1

                #track the order
                if s not in a_order:
                    a_order[s] = []

                a_order[s].append(o)
                
                #calculate weight
                weight = 1 / len(a_order[s])
                a_weight[o] += weight 
            
    ###########################################################
    # n_triples -- number of distinct triples
    # n_people -- number of distinct people mentioned in ANY role
    #             (e.g., actor, director, producer, etc.)
    # n_top_actors -- number of people appeared as ACTORS in
    #                 M movies, where M is the maximum number
    #                 of movies any person appeared in as an actor
    # n_highweight_actor -- the 'weight' of an actor is calculated by 
    #               dividing each 'appearance' by their place in 
    #               the cast list. If we add up all of these, we
    #               get the cumulative weight of the actor. The 
    #               'highweight' is the largest cumulative weight.
    # s_name -- the name of the highweight actor
    ###########################################################

    #number of distinct triples
    n_people = len(n_people)

    #calcule max movies
    max_movies = 0
    for count in actor_movie_count.values():
        if count > max_movies:
            max_movies = count


    #calculate top actors is in max movies
    n_top_actors = 0
    for count in actor_movie_count.values():
        if count == max_movies:
            n_top_actors += 1


    #calculate highweight actor and name
    n_highweight_actor = max(a_weight.values())
    
    s_name = a_names.get(max(a_weight, key=a_weight.get), "")


    return n_triples, n_people, n_top_actors, n_highweight_actor, s_name

# DO NOT CHANGE THE FINAL OUTPUT FORMATTING BELOW THIS LINE
if __name__ == "__main__":
    n_triples, n_people, n_top_actors, n_highweight_actor, s_name = _compute_stats()
    print()
    print(f"{n_triples:,} (n_triples)")
    print(f"{n_people:,} (n_people)")
    print(f"{n_top_actors} (n_top_actors)")
    print(f"{n_highweight_actor} (n_highweight_actor)")
    print(f"{s_name} (s_name)")
