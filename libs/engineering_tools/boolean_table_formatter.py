
    
def compute_bool(a, b, c, f):
    if a == 1:
        a = True
    else :
        a = False
    if b == 1:
        b = True
    else :
        b = False
    if c == 1:
        c = True
    else :
        c = False
    r = f(a, b, c)
    
    if r:
        return 1
    else:
        return 0
    
def display_truth_table(f):
    cnt = 0
    boole = [0, 1]
    print ("|---------------|")
    print ("| a | b | c | r |")
    print ("|===============|")
    
    for (a, b, c) in [ (a, b, c) for a in boole for b in boole for c in boole]:
        cnt = cnt + compute_bool(a,b,c, f)
        print ("|",a, "|", b, "|", c, "|", compute_bool(a,b,c, f) , "|")
        print ("|-----------|---|")
    print ("Nombre de combinaisons vrai : ", cnt)

def test():
    assert compute_bool(0,0,0, lambda a,b,c : (a and not(b)) or c) == 0
    assert compute_bool(0,0,1, lambda a,b,c : (a and not(b)) or c) == 1
    assert compute_bool(0,1,0, lambda a,b,c : (a and not(b)) or c) == 0
    assert compute_bool(0,1,1, lambda a,b,c : (a and not(b)) or c) == 1
    assert compute_bool(1,0,0, lambda a,b,c : (a and not(b)) or c) == 1
    assert compute_bool(1,0,1, lambda a,b,c : (a and not(b)) or c) == 1
    assert compute_bool(1,1,0, lambda a,b,c : (a and not(b)) or c) == 0
    assert compute_bool(1,1,1, lambda a,b,c : (a and not(b)) or c) == 1
    
if __name__ == "__main__":
    test()
    fc = lambda a,b,c : not(a or not(b)) and (b or not(c))
    display_truth_table(fc)
