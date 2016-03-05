from math import pi, cos, sin, radians


def main():
    global svgtowrite
    svgtowrite = list()
    instructions = list()

    points = list()
    points.append((100.0, 100.0))

    max_x = 0.0
    max_y = 0.0

    angle = 0.0

    color = "black"

    with open("LOGO-ELDLC.logo") as p:
        initsvgfile()

        instructions = p.read().split()


        max_x, max_y = process(instructions, points, color, angle, max_x, max_y)


        endsvgfile(max_x, max_y)
        writesvgfile()



def forward(distance, point, color, angle):
    new_x = point[0] + distance * cos(angle)
    new_y = point[1] + distance * sin(angle)
    svgtowrite.append("<line x1=\"" + str(point[0]) + "\" y1=\"" + str(point[1]) + "\" x2=\"" + str(new_x) + "\"" + " y2=\"" + str(new_y) + "\"" + " stroke=\"black\"/>\n")
    return new_x, new_y


def initsvgfile():
    svgtowrite.append("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    svgtowrite.append("<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"200\" height=\"200\">\n")
    svgtowrite.append("<title>Exemple LOGO</title>\n")
    svgtowrite.append("<desc>Du LOGO.</desc>\n")


def endsvgfile(max_x, max_y):
    svgtowrite[1] = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"" + str(max_x) + "\" height=\"" + str(max_y) + "\">\n"
    svgtowrite.append("</svg>")


def writesvgfile():
    with open("file.svg", "w") as f:
        f.writelines(svgtowrite)


def process(instructions, points, color, angle, max_x, max_y, iPoint=0, iInstruction=0):
    if len(instructions) != 0:
        nbrepeat_new = None

        print(iInstruction)
        command = instructions[iInstruction]
        distance = instructions[iInstruction+1]

        command = command.replace("[", "")
        distance = distance.replace("]", "")

        distance = float(distance)

        if command == "FORWARD":
            iPoint += 1
            points.insert(iPoint, forward(distance, points[iPoint-1], color, angle))
            if points[iPoint][0] > max_x:
                max_x = points[iPoint][0]
            if points[iPoint][1] > max_y:
                max_y = points[iPoint][1]

        if command == "LEFT":
            angle -= radians(distance)

        if command == "RIGHT":
            angle += radians(distance)

        if command == "REPEAT":
            nbrepeat_new = distance

        nbrepeat -= 1

        if nbrepeat_new != None:
            nbrepeat = nbrepeat_new

        if nbrepeat == 0 and nbrepeat_new == None:
            return process(instructions, points, color, angle, max_x, max_y, 1, iPoint, iInstruction+2)
        else:
            nbrepeat_new = None
            return process(instructions, points, color, angle, max_x, max_y, nbrepeat, iPoint, iInstruction+2)



    return max_x, max_y

main()
