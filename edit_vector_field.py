def edit_vx_func(relation):
    f = open("vitx.py", 'w')
    f.write("from numpy import sin, cos, exp, sqrt, log, tan, arccos, arcsin, arctan, sinc, pi\n\ndef vx(x,y,t):\n\tv = "+relation+"\n\treturn v")
    f.close()
    return

def edit_vy_func(relation):
    f = open("vity.py", 'w')
    f.write("from numpy import sin, cos, exp, sqrt, log, tan, arccos, arcsin, arctan, sinc, pi\n\ndef vy(x,y,t):\n\tv = "+relation+"\n\treturn v")
    f.close()
    return

def edit_vr_func(relation):
    f = open("vitr.py", 'w')
    f.write("from numpy import sin, cos, exp, sqrt, log, tan, arccos, arcsin, arctan, sinc, pi\n\ndef vr(r,th,x,y,t):\n\tv = "+relation+"\n\treturn v")
    f.close()
    return

def edit_vth_func(relation):
    f = open("vitth.py", 'w')
    f.write("from numpy import sin, cos, exp, sqrt, log, tan, arccos, arcsin, arctan, sinc, pi\n\ndef vth(r,th,x,y,t):\n\tv = "+relation+"\n\treturn v")
    f.close()
    return
