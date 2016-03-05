from math import pi, cos, sin, radians


# I don't use recursive function because of the maximum recursion depth3

# Please read COMMANDS.md

def main():
    LOGO_STROKES = ["black", "blue", "green", "cyan", "red", "magenta", "yellow", "white", "brown", "tan", "green", "aqua",
                   "salmon", "purple", "orange", "grey"]

    filename_LOGO = "flower.logo"   # Nom du fichier LOGO
    filename_SVG = "LOGO-ELDLC.svg"     # Nom du fichier SVG

    repeat_start = [] # liste contenant l'indice du premier token de chaque REPEAT
    nb_left_repeat = [] # liste contenant le nombre de répétitions restantes pour chaque REPEAT
    segments = []  # Liste des segments [ ((x1, y1), (x2, y2), stroke, stroke-width, writing), (...), (...) ]

    ###################
    # DEFAULT VALUE   #
    ###################
    angle = 0
    stroke = "black"
    stroke_width = 1
    writing = True
    iCommand = 0
    iPoint = 0
    iRepeat = -1

    #########################
    # WE READ THE LOGO FILE #
    #########################

    commands = read_logo(filename_LOGO)   # Liste des commands

    ############################
    # WE PROCESS THE LOGO FILE #
    ############################

    while True:
        if iCommand < len(commands):
            command = commands[iCommand].upper()

            if iRepeat > -1 and command == "]":
                nb_left_repeat[iRepeat] -= 1

                if nb_left_repeat[iRepeat] == 0:
                    iCommand += 1
                    iRepeat -= 1
                    nb_left_repeat.pop()
                    repeat_start.pop()
                else:
                    iCommand = repeat_start[iRepeat]

            else:
                if command == "FORWARD" or command == "FD" or command == "BACKWARD" or command == "BK":
                    error, parameter = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = float(parameter[0])
                            if command == "BK" or command == "BACKWARD":
                                parameter = -parameter

                            if len(segments) == 0:
                                segments.append((
                                    [100,100],
                                    [100+parameter*cos(angle), 100+parameter*sin(angle)],
                                    stroke,
                                    stroke_width,
                                    writing
                                ))
                            else:
                                segments.append((
                                    [segments[iPoint-1][1][0], segments[iPoint-1][1][1]],
                                    [segments[iPoint-1][1][0]+parameter*cos(angle), segments[iPoint-1][1][1]+parameter*sin(angle)],
                                    stroke,
                                    stroke_width,
                                    writing
                                ))

                            iPoint += 1
                        except:
                            print("Invalid parameter {0} for command {1}. Turtle did not move.".format(str(parameter), str(command)))

                        iCommand += 2
                    else:
                        iCommand += 1

                elif command == "LEFT" or command == "LT":
                    error, parameter = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = float(parameter[0])
                            angle -= radians(parameter)
                        except:
                            print("Invalid parameter {0} for command {1}. Angle did not change.".format(str(parameter), str(command)))

                        iCommand += 2
                    else:
                        iCommand += 1

                elif command == "RIGHT" or command == "RT":
                    error, parameter = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = float(parameter[0])
                            angle += radians(parameter)
                        except:
                            print("Invalid parameter {0} for command {1}. Angle did not change.".format(str(parameter), str(command)))

                        iCommand += 2
                    else:
                        iCommand += 1

                elif command == "SETCOLOR":
                    error, parameter = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = int(parameter[0])

                            if 0 <= parameter < len(LOGO_STROKES):
                                stroke = LOGO_STROKES[parameter]
                            else:
                                print("Invalid parameter {0} for command {1}. Color did not change.".format(str(parameter), str(command)))
                        except:
                            if parameter.count(",") == 2:
                                try:
                                    r, g, b = map(int, parameter.split(","))
                                    stroke = "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))
                                except ValueError:
                                    print("Invalid parameter {0} for command {1}. Color did not change.".format(str(parameter), str(command)))
                            else:
                                if parameter.lower() in LOGO_STROKES:
                                    stroke = parameter
                                else:
                                    print("Invalid parameter {0} for command {1}. Color did not change.".format(str(parameter), str(command)))

                        iCommand += 2
                    else:
                        iCommand += 1

                elif command == "SETWIDTH":
                    error, parameter = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            stroke_width = int(parameter[0])
                        except:
                            print("Invalid parameter {0} for command {1}. Line width did not change.".format(str(parameter), str(command)))

                        iCommand += 2
                    else:
                        iCommand += 1

                elif command == "PENDOWN" or command == "PD":
                    writing = True
                    iCommand += 1

                elif command == "PENUP" or command == "PU":
                    writing = False
                    iCommand += 1

                elif command == "REPEAT":
                    error, parameter = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = int(parameter[0])
                        except:
                            print("Invalid parameter {0} for command {1}. Repeat ignored.".format(str(parameter), str(command)))
                            iCommand += 1
                        else:
                            nb_left_repeat.append(parameter)
                            iCommand += 3
                            repeat_start.append(iCommand)
                            iRepeat += 1
                    else:
                        iCommand += 1

                else:
                    print("Syntax error : {0} is not a valid command.".format(str(command)))
                    iCommand += 1

        else:
            break

    ###################
    # CENTER THE SVG  #
    ###################

    translate(get_min(segments), segments)

    ###################
    # WRITE THE SVG   #
    ###################

    write_svg(segments, filename_SVG)


def read_logo(filename):
    with open(filename) as READER_LOGO:
        return READER_LOGO.read().replace("[", " [ ").replace("]", " ] ").split()


def get_min(segments):
    minx1 = 0
    miny1 = 0

    for segment in segments:
        currentx1 = segment[0][0]
        currenty1 = segment[0][1]

        if currentx1 < minx1:
            minx1 = currentx1

        if currenty1 < miny1:
            miny1 = currenty1

    return minx1, miny1


def translate(coordinates, segments):
    for segment in segments:
        segment[0][0] += -coordinates[0]
        segment[1][0] += -coordinates[0]

        segment[0][1] += -coordinates[1]
        segment[1][1] += -coordinates[1]


def clamp(x):
    return max(0, min(x, 255))


def write_svg(segments, filename):
    with open(filename, "w") as WRITER_SVG:
        WRITER_SVG.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        WRITER_SVG.write("<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"20000\" height=\"20000\">\n")
        WRITER_SVG.write("<title>Exemple LOGO</title>\n")
        WRITER_SVG.write("<desc>Du LOGO.</desc>\n")

        for segment in segments:
            towrite = ""
            if segment[4]:
                towrite += "<line x1=\"{0}\" y1=\"{1}\" x2=\"{2}\" y2=\"{3}\" ".format(str(segment[0][0]),
                                                                                       str(segment[0][1]),
                                                                                       str(segment[1][0]),
                                                                                       str(segment[1][1]))

                towrite += "stroke=\"{0}\" ".format(str(segment[2]))

                if segment[3] != 1:
                    towrite += "stroke-width=\"{0}\" ".format(str(segment[3]))

                towrite += "/>\n"

                WRITER_SVG.write(towrite)
        WRITER_SVG.write("</svg>")


def get_parameters(commands, iCommand, nb_of_parameters):
    parameters = list()

    try:
        for loop in range(nb_of_parameters):
            parameters.append(commands[iCommand+loop+1])
        error = False
    except IndexError:
        print("Not enough parameters for command {0}.".format(str(commands[iCommand])))
        error = True

    return error, parameters[0:nb_of_parameters]

main()