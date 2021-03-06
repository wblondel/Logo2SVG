# !/usr/bin/python
# -*- coding: utf-8 -*-

# Logo2SVG  Copyright (C) 2017    William Gerald Blondel
# contact@williamblondel.fr
# Last modified 3rd May 2017

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# I don't use recursive function because of the maximum recursion depth
# Please read COMMANDS.md

# TODO: Set turtle position
# TODO: Support parameters in procedures
# TODO: Securely evaluate mathematical expressions in parameters (eval is EVIL)
# TODO: Optimize SVG
# TODO: Variable Assignment


from math import cos, sin, radians
from random import randrange
import sys
import getopt


def main(argv):
    LOGO_STROKES = ["BLACK", "BLUE", "GREEN", "CYAN", "RED", "MAGENTA", "YELLOW", "WHITE", "BROWN", "TAN", "GREEN",
                    "AQUA", "SALMON", "PURPLE", "ORANGE", "GREY"]

    LOGO_COMMANDS = ["FORWARD", "FD", "FW", "BACKWARD", "BK", "LEFT", "LT", "RIGHT", "RT", "SETPENCOLOR", "SETWIDTH",
                     "PENDOWN", "PD", "PENUP", "PU", "REPEAT", "RANDOM", "TO"]

    FILENAME_LOGO = None
    FILENAME_SVG = None

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            FILENAME_LOGO = arg
        elif opt in ("-o", "--ofile"):
            FILENAME_SVG = arg

    repeat_start = []  # liste contenant l'indice du premier token de chaque REPEAT
    nb_left_repeat = []  # liste contenant le nombre de répétitions restantes pour chaque REPEAT
    segments = []  # Liste des segments [ ((x1, y1), (x2, y2), stroke, stroke-width, writing), (...), (...) ]
    procedures = dict()  # List of procedures (TO ...) et de leur point de départ
    where_to_go_after_procedures = []  # Liste content l'indice de la commande à exécuter après la procédure finie

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
    iProcedure = -1

    #########################
    # WE READ THE LOGO FILE #
    #########################

    commands = read_logo(FILENAME_LOGO)  # Liste des commands

    ############################
    # WE PROCESS THE LOGO FILE #
    ############################
    toexecute = True

    while True:
        add = True
        if iCommand < len(commands):
            command = commands[iCommand]

            if iRepeat > -1:  # Si on est dans un REPEAT
                if command == "]":  # Si on arrive à la fin du REPEAT
                    nb_left_repeat[iRepeat] -= 1

                    if nb_left_repeat[iRepeat] <= 0:
                        iRepeat -= 1
                        nb_left_repeat.pop()
                        repeat_start.pop()
                        toexecute = True
                    else:
                        iCommand = repeat_start[iRepeat]
                        add = False
                elif nb_left_repeat[iRepeat] <= 0:
                    toexecute = False

            if toexecute:
                if command in ["FORWARD", "FD", "FW", "BACKWARD", "BK"]:
                    error, parameter, random_switch = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = float(eval(parameter[0]))
                            if "B" in command:
                                parameter = -parameter

                            if len(segments) == 0:
                                segments.append((
                                    [0, 0],
                                    [0 + parameter * cos(angle), 0 + parameter * sin(angle)],
                                    stroke,
                                    stroke_width,
                                    writing
                                ))
                            else:
                                segments.append((
                                    [segments[iPoint - 1][1][0], segments[iPoint - 1][1][1]],
                                    [segments[iPoint - 1][1][0] + parameter * cos(angle),
                                     segments[iPoint - 1][1][1] + parameter * sin(angle)],
                                    stroke,
                                    stroke_width,
                                    writing
                                ))

                            iPoint += 1
                        except:
                            print("Invalid parameter {0} for command {1}. Turtle did not move.".format(str(parameter),
                                                                                                       str(command)))

                        iCommand += 2 + random_switch
                    else:
                        iCommand += 1 + random_switch

                elif command in ["LEFT", "LT", "RIGHT", "RT"]:
                    error, parameter, random_switch = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = float(eval(parameter[0]))

                            if "R" in command:
                                parameter = -parameter
                            angle -= radians(parameter)
                        except:
                            print("Invalid parameter {0} for command {1}. Angle did not change.".format(str(parameter),
                                                                                                        str(command)))

                        iCommand += 2 + random_switch
                    else:
                        iCommand += 1 + random_switch

                elif command in ["SETPENCOLOR", "SETCOLOR"]:
                    error, parameter, random_switch = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = int(eval(parameter[0]))

                            if 0 <= parameter < len(LOGO_STROKES):
                                stroke = LOGO_STROKES[parameter]
                            else:
                                print("Invalid parameter {0} for command {1}. Color did not change.".format(
                                    str(parameter), str(command)))
                        except:
                            parameter = parameter[0]
                            if parameter.count(",") == 2:
                                try:
                                    r, g, b = map(int, parameter.split(","))
                                    stroke = "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))
                                    print(stroke)
                                except ValueError:
                                    print("Invalid parameter {0} for command {1}. Color did not change.".format(
                                        str(parameter), str(command)))
                            else:
                                if parameter in LOGO_STROKES:
                                    stroke = parameter
                                else:
                                    print("Invalid parameter {0} for command {1}. Color did not change.".format(
                                        str(parameter), str(command)))

                        iCommand += 2 + random_switch
                    else:
                        iCommand += 1 + random_switch

                elif command == "SETWIDTH":
                    error, parameter, random_switch = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            stroke_width = int(eval(parameter[0]))
                        except:
                            print("Invalid parameter {0} for command {1}. Line width did not change.".format(
                                str(parameter), str(command)))

                        iCommand += 2 + random_switch
                    else:
                        iCommand += 1 + random_switch

                elif command in ["PENDOWN", "PD"]:
                    writing = True
                    iCommand += 1

                elif command in ["PENUP", "PU"]:
                    writing = False
                    iCommand += 1

                elif command == "REPEAT":
                    error, parameter, random_switch = get_parameters(commands, iCommand, 1)

                    if not error:
                        try:
                            parameter = int(eval(parameter[0]))
                        except:
                            print("Invalid parameter {0} for command {1}. Repeat ignored.".format(str(parameter),
                                                                                                  str(command)))
                            iCommand += 1 + random_switch
                        else:
                            nb_left_repeat.append(parameter)
                            iCommand += 3 + random_switch
                            repeat_start.append(iCommand)
                            iRepeat += 1
                    else:
                        iCommand += 1 + random_switch

                elif command == "TO":
                    error, parameter, random_switch = get_parameters(commands, iCommand, 1)

                    if not error:
                        parameter = parameter[0]

                        if parameter in LOGO_COMMANDS:
                            print("Invalid procedure name. {0} is a reserved keyword.".format(str(parameter)))
                            iCommand += 2
                        else:
                            procedures[parameter] = iCommand + 2

                            try:
                                stop = commands.index("END", iCommand) + 1
                                iCommand = stop
                            except ValueError:
                                print("Procedure {0} started but no END found.".format(str(parameter)))
                                iCommand += 2

                elif command in procedures:
                    where_to_go_after_procedures.append(iCommand + 1)
                    iProcedure += 1
                    iCommand = procedures[command]

                elif command == "END":
                    iCommand = where_to_go_after_procedures[iProcedure]
                    where_to_go_after_procedures.pop()
                    iProcedure -= 1

                elif command == "]":
                    if add:
                        iCommand += 1
                        add = False

                else:
                    print("Syntax error : {0} is not a valid command.".format(str(command)))
                    iCommand += 1
            else:
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

    write_svg(segments, get_max(segments), FILENAME_SVG)


def read_logo(FILENAME_LOGO=None):
    READER_LOGO = None

    while READER_LOGO is None:
        if FILENAME_LOGO is None:
            FILENAME_LOGO = input("Which *.logo file do you want to open ? ")
        try:
            with open(FILENAME_LOGO) as READER_LOGO:
                content = READER_LOGO.read()  # We read the file
                content = content.replace("[", " [ ").replace("]", " ] ")  # We replace [ by " [ "

                while ", " in content:
                    content = content.replace(", ", ",")  # We replace ", " by ","
                while " ," in content:
                    content = content.replace(" ,", ",")  # We replace " ," by ","

                content = content.upper().split()  # We UP everything and split
                content[0:0] = ["LEFT", "90"]  # Temporary fix for the Turtle to look UP at the beginning

                return content
        except EnvironmentError as e:
            FILENAME_LOGO = None
            print(e.strerror)
        except UnicodeDecodeError as e:
            FILENAME_LOGO = None
            print(e.reason)


def get_min(segments):
    minx = 100
    miny = 100

    for segment in segments:
        currentx1, currentx2 = segment[0][0], segment[1][0]
        currenty1, currenty2 = segment[0][1], segment[1][1]

        if currentx1 < minx or currentx2 < minx:
            minx = min(currentx1, currentx2)

        if currenty1 < miny or currenty2 < miny:
            miny = min(currenty1, currenty2)

    return minx, miny


def get_max(segments):
    maxx = 0
    maxy = 0

    for segment in segments:
        currentx1, currentx2 = segment[0][0], segment[1][0]
        currenty1, currenty2 = segment[0][1], segment[1][1]

        if currentx1 > maxx or currentx2 > maxx:
            maxx = max(currentx1, currentx2)
        if currenty1 > maxy or currenty2 > maxy:
            maxy = max(currenty1, currenty2)

    return maxx, maxy


def translate(coordinates, segments):
    for segment in segments:
        segment[0][0] += -coordinates[0] + 25
        segment[1][0] += -coordinates[0] + 25

        segment[0][1] += -coordinates[1] + 25
        segment[1][1] += -coordinates[1] + 25


def clamp(x):
    return max(0, min(x, 255))


def write_svg(segments, maxi, FILENAME_SVG=None):
    WRITER_SVG = None

    while WRITER_SVG is None:
        if FILENAME_SVG is None:
            FILENAME_SVG = input("Name of svg file : ")
        try:
            with open(FILENAME_SVG, "w") as WRITER_SVG:
                WRITER_SVG.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
                WRITER_SVG.write(
                    "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"{0}\" height=\"{1}\">\n".format(
                        str(maxi[0]+25), str(maxi[1]+25)))
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

                break
        except EnvironmentError as e:
            FILENAME_SVG = None
            print(e.strerror)
        except UnicodeDecodeError as e:
            FILENAME_SVG = None
            print(e.reason)

        choix = input("Réessayer (Y/N) ? ")
        if choix in "nN":
            break


def get_parameters(commands, iCommand, nb_of_parameters):
    parameters = list()
    random_switch = 0

    try:
        error = False
        for loop in range(nb_of_parameters):
            tmp = commands[iCommand + loop + 1]

            if tmp == "RANDOM":
                try:
                    tmp = commands[iCommand + loop + 2]
                    tmp = str(randrange(int(tmp)))
                    random_switch += 1
                except ValueError:
                    print("Invalid subparameter {0} for parameter RANDOM in command {1}.".format(str(tmp), str(
                        commands[iCommand])))
                    random_switch += 2
                    error = True
                except IndexError:
                    print("No subparameter for parameter RANDOM in command {0}.".format(str(commands[iCommand])))
                    random_switch += 2
                    error = True

            parameters.append(tmp)

    except IndexError:
        print("Not enough parameters for command {0}.".format(str(commands[iCommand])))
        error = True

    return error, parameters[0:nb_of_parameters], random_switch


if __name__ == "__main__":
    main(sys.argv[1:])
