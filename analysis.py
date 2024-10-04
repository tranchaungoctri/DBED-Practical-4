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
    n_triples = 0
    n_people = set()
    actor_movie_count ={}
    actor_weight = {}
    max_movies = 0
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
            if  _is_uri(s) and s.startswith(uri_person):
                n_people.add(s)
            #count movies per actor
            if p == predicate_has_actor:
                actor = o
                if _is_uri(actor) and actor.startswith(uri_person):
                    if actor not in actor_movie_count:
                        actor_movie_count[actor] = 0
                    actor_movie_count[actor] += 1
                    #track max movies that actor is in
                    max_movies = max(max_movies, actor_movie_count[actor])
            
            #calculate actor weight
            if p.startwith(predicate_prefix):
                if p == predicate_has_actor:
                    order = len(actor_weight) + 1
                    actor_weight[o] = actor_weight.get(o, 0) + (1 / order)

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

    #total of distinct people
    n_people = len(n_people)

    #total number of top actors
    n_top_actors = sum(1 for count in actor_movie_count.values() if count == max_movies)

    #calculate highweight actor and name
    n_highweight_actor = max(actor_weight.values(), default=0)
    s_name = max(actor_weight, key=actor_weight.get, default="")

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
