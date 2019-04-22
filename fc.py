def reset_vectors(gouttes, canvas):
    to_del = []
    k=0
    for g in gouttes:
        to_del.append(k)
        canvas.delete(g.gui)
    for sup in to_del[::-1]:
        gouttes.pop(k)
    return
