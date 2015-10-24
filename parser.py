import os
import sys
import csv
from itertools import count

def parse(basename, ordinal, outfd):
    outcsv = csv.writer(outfd)

    for i in count(0):
        fname = "{}_{:08d}.vtk".format(basename, i)

        try:
            infd = open(fname, "r")
        except IOError:
            break

        print "Timestep {}".format(i)

        while True:
            line = infd.readline()
            if line.startswith("POINTS "):
                mark, point_count, datatype = line.split()
                if datatype != 'float':
                    raise ValueError("Got datatype '{}', expected 'float'".format(datatype))

                point_count = int(point_count)
                if i == 0:
                    total_points = point_count
                    if ordinal > total_points:
                        raise ValueError("Cannot extract point {}, only {} points available.".format(ordinal, total_points))
                    print "Extracting point {} of {}".format(ordinal, total_points)
                else:
                    if point_count != total_points:
                        raise ValueError("Number of points has changed from {} (timestep 0) to {} (timestep {})".format(total_points, point_count, i))
                break

        for local_ordinal in range(1, total_points + 1):
            line = infd.readline()
            if local_ordinal == ordinal:
                x, y, z = line.split()
                outcsv.writerow((i, x, y))
                break
    print "Processed {} time steps. Done.".format(i)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >>sys.stderr, "Usage: parser.py <basename> <ordinal> <outfile>"
        print >>sys.stderr, "Example: parser.py Swimmer1IBPts_time 1 Swimmer-head.csv"
        sys.exit(1)

    basename, ordinal, outfile = sys.argv[1:]
    ordinal = int(ordinal)
    outfd = open(outfile, "w")

    parse(basename, ordinal, outfd)
