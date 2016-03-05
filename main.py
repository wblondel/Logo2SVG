# square.logo -> OK



from math import pi, cos, sin, radians
import sys

def main():
    global LOGO_STROKES
    LOGO_STROKES = ["black", "blue", "green", "cyan", "red", "magenta", "yellow", "white", "brown", "tan", "green", "aqua",
                   "salmon", "purple", "orange", "grey"]

    filename_LOGO = "LOGO-ELDLC.logo"   # Nom du fichier LOGO
    filename_SVG = "LOGO-ELDLC.svg"     # Nom du fichier SVG

    global repeat_start
    global nb_left_repeat

    repeat_start = [] # liste contenant l'indice du premier token de chaque REPEAT
    nb_left_repeat = [] # liste contenant le nombre de répétitions restantes pour chaque REPEAT

    segments = []  # Liste des segments [ ((x1, y1), (x2, y2), stroke, stroke-width, writing), (...), (...) ]

    instructions = read_logo(filename_LOGO)   # Liste des instructions
    process_instructions(instructions, segments)
    write_svg(segments, filename_SVG)


def read_logo(filename):
    with open(filename) as READER_LOGO:
        return READER_LOGO.read().replace("[", " [ ").replace("]", " ] ").split()


def process_instructions(instructions, segments, angle=0, stroke="black", stroke_width=1, writing=True, iInstruction=0, iPoint=0,
                         iRepeat=-1, test=1):
    test += 1


    if iInstruction < len(instructions):
        commande = instructions[iInstruction].upper()

        if iRepeat > -1 and commande == "]":
            nb_left_repeat[iRepeat] -= 1

            if nb_left_repeat[iRepeat] == 0:
                iInstruction += 1
                iRepeat -= 1
                nb_left_repeat.pop()
                repeat_start.pop()
            else:
                iInstruction = repeat_start[iRepeat]

        else:
            parametre = instructions[iInstruction+1]
            print("{0} : {1} {2}".format(str(test), str(commande), str(parametre)))

            if commande == "FORWARD" or commande == "FD":
                parametre = float(parametre)

                if len(segments) == 0:
                    segments.append((
                                     (100,100),
                                     (100+parametre*cos(angle), 100+parametre*sin(angle)),
                                     stroke,
                                     stroke_width,
                                     writing
                                    ))
                else:
                    segments.append((
                                     (segments[iPoint-1][1][0], segments[iPoint-1][1][1]),
                                     (segments[iPoint-1][1][0]+parametre*cos(angle), segments[iPoint-1][1][1]+parametre*sin(angle)),
                                     stroke,
                                     stroke_width,
                                     writing
                                    ))

                iPoint += 1
                iInstruction += 2

            elif commande == "LEFT" or commande == "LT":
                angle -= radians(float(parametre))
                iInstruction += 2

            elif commande == "RIGHT" or commande == "RT":
                angle += radians(float(parametre))
                iInstruction += 2

            elif commande == "PENCOLOR":
                if parametre.lower() in LOGO_STROKES:
                    stroke = parametre
                iInstruction += 2

            elif commande == "PENDOWN" or commande == "PD":
                writing = True
                iInstruction += 1

            elif commande == "PENUP" or commande == "PU":
                writing = False
                iInstruction += 1

            elif commande == "REPEAT":
                nb_left_repeat.append(int(parametre))
                iInstruction += 3
                repeat_start.append(iInstruction)
                iRepeat += 1

            else:
                print("Syntax error : {0} is not a valid command.".format(str(commande)))

        process_instructions(instructions, segments, angle, stroke, stroke_width, writing, iInstruction, iPoint, iRepeat, test)


def write_svg(segments, filename):
    with open(filename, "w") as WRITER_SVG:
        WRITER_SVG.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        WRITER_SVG.write("<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"20000\" height=\"20000\">\n")
        WRITER_SVG.write("<title>Exemple LOGO</title>\n")
        WRITER_SVG.write("<desc>Du LOGO.</desc>\n")

        for segment in segments:
            if segment[4]:
                WRITER_SVG.write(
                    "<line x1=\"{0}\" y1=\"{1}\" x2=\"{2}\" y2=\"{3}\" stroke=\"{4}\" stroke-width=\"{5}\"/>\n".format(str(segment[0][0]),
                                                                                                str(segment[0][1]),
                                                                                                str(segment[1][0]),
                                                                                                str(segment[1][1]),
                                                                                                str(segment[2]),
                                                                                                str(segment[3]))
                    )
        WRITER_SVG.write("</svg>")

main()