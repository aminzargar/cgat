'''
contigs2random_sample.py
=============================================

:Author: Nick Ilott
:Release: $Id$
:Date: |today|
:Tags: Python

Purpose
-------

When conducting a simulation study it is often useful to simulate contigs from the 
original genome/genomes from which your contigs have been derived. This can then 
provide an expectation dataset for downstream analyses.

Usage
-----

Example::

   python contigs2random_sample.py --help

Type::

   python contigs2random_sample_.py --help

for command line help.

Documentation
-------------

The script takes as input a multifasta set of contigs with arbitrary names as may have
been generated by any assembly algorithm. It also takes as input a map which maps the 
contig id to a genome id. The genomes that are referred to in the species-map file
are specified as a directory and these are where the samples are derived.

The contigs file is read from stdin and writes the result to stdout.

The species map MUST be in the format "contig" "species" and the species MUST be the 
contig identifier of the respective genome.

Command line options
--------------------

'''

import os
import sys
import optparse
import glob
import random
import CGAT.Experiment as E
import CGAT.FastaIterator as FastaIterator
import CGAT.IOTools as IOTools


def main(argv=None):
    """script main.

    parses command line options in sys.argv, unless *argv* is given.
    """

    if not argv:
        argv = sys.argv

    # setup command line parser
    parser = optparse.OptionParser(version="%prog version: $Id: contigs2random_sample.py 2871 2010-03-03 10:20:44Z nicki $",
                                   usage=globals()["__doc__"])

    parser.add_option("-m", "--species-map", dest="species_map", type="string",
                      help="text file specifying the mapping between contig and genome")

    parser.add_option("-g", "--genome-dir", dest="genome_dir", type="string",
                      help="specify directory where genome / genomes are stored")

    # add common options (-h/--help, ...) and parse command line
    (options, args) = E.Start(parser, argv=argv)

    # read in contig lengths into dictionary
    E.info("reading contigs file")
    c_contigs = 0
    contigs_lengths = {}
    for fasta in FastaIterator.iterate(options.stdin):
        c_contigs += 1

        # titles of fasta records must be single strings with no special
        # characters
        contigs_lengths[fasta.title.split(" ")[0]] = len(fasta.sequence)

    E.info("read %i contigs" % c_contigs)

    # read in mapping between spcies and contigs
    species_map = {}
    for line in open(options.species_map).readlines():
        data = line[:-1].split("\t")
        contig, species = data[0], data[1]
        species_map[contig] = species

    # read genomes into memory
    # NB this may need optimisin if using large
    # genomes or many genomes
    E.info("reading genomes from %s" % options.genome_dir)

    # The directory must ONLY contain genome files!!
    genomes_sequences = {}
    c_genomes = 0
    for genome_file in glob.glob(os.path.join(options.genome_dir, "*")):
        c_genomes += 1
        for fasta in FastaIterator.iterate(IOTools.openFile(genome_file)):
            genomes_sequences[fasta.title] = fasta.sequence
    E.info("read %i genomes from %s" % (c_genomes, options.genome_dir))

    # iterate over the contigs and sample from the respective genome
    E.info("iterating over contigs")
    c_contigs_output = 0
    for contig, length in contigs_lengths.iteritems():
        if contig not in species_map:
            E.warn("contig %s not in species map file" % contig)
        else:
            c_contigs_output += 1
            genome = species_map[contig]
            genome_length = len(genomes_sequences[genome])

            # get the start position from which to sample
            start = random.randint(1, genome_length)
            try:
                end = start + length - 1
            except ValueError:
                print "end of sampled contig extends beyond length of genome"

            sampled_seq = genomes_sequences[genome][start:end]
            options.stdout.write(
                ">%s_random\n%s\n" % (contig + "_%s" % species_map[contig], sampled_seq))

    E.info("written %i contigs" % c_contigs_output)
    # write footer and output benchmark information.
    E.Stop()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
