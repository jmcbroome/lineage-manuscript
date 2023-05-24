import sys

for entry in sys.stdin:
    try:
        name, path = entry.strip().split("\t")
    except ValueError:
        continue
        # print(entry.strip())
    if name == 'clade':
        # print(entry.strip())
        continue
    bases = {}
    # print(path,file=sys.stderr)
    for step in path.split(">"):
        mstr = step.strip()
        if len(mstr) == 0:
            continue
        mutations = mstr.split(",")
        # print(step,file=sys.stderr)
        for m in mutations:
            # print(m,file=sys.stderr)
            location = int(m[1:-1])
            #first time its been seen- set the info.
            if location not in bases:
                bases[location] = [m[0],m[-1]]
            #if its a reversion to the reference, remove the location from tracking.
            elif m[-1] == bases[location][0]:
                bases.pop(location)
            #otherwise, update the alternative
            else:
                bases[location][1] = m[-1]
    #then reconstruct the mutation set and dump to stdout
    if len(bases) > 0:
        print(name, ",".join([v[0]+str(k)+v[1] for k,v in bases.items()]), sep='\t')