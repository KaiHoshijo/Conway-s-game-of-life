# Created by Kai Hoshijo
# 3/4/19
# step by step process 
# create class that contains the grid
# create second class that maintains the cells and their natures

import grid, cells
from flask import Flask, Response, make_response

row = 5
col = 5
grid = grid.Grid(row, col)
cell = cells.Cell(grid)
app = Flask(__name__)

@app.route("/")
def index():
    return "hello"

@app.route("/messy")
def messy():
    p = ""
    for i in gen():
        p += i
    return p
    # return "<p> {} </p>".format(p)
    # return """
    #     <p> {} <p>   
    #     """.format(cell.grid.return_show())
def gen():
    cell.check_all()
    for i in range(row):
        yield " <p> {} </p> ".format(" ".join(cell.grid.return_show()[i]))

if __name__ == "__main__":
    print("got this far")
    app.run(threaded = True, debug = True)

    print("move 0")
    cell.grid.show()
    for i in range(1, 11):
        print("move {}".format(i))
        cell.check_all()
        cell.grid.show()