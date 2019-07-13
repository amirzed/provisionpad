import redis

r = redis.Redis(
    host='localhost',
    port=6379, 
    password='')

def get_box_name(available_names, created_instances):
    """
    gets redis variables names and returns the best name for the
    newly created instance
    """
    nval = r.lpop(available_names)
    if nval is not None and nval.decode('utf-8') not in runnin_instances:
        boxn = nval.decode('utf-8')
    else:
        boxi = int(r.get(created_instances)) + 1
        boxn = 'box{0}'.format(boxi)
        r.incr(created_instances)
    return boxn
        
if __name__ == "__main__":
    print (get_box_name('available_names', 'created_instances'))
