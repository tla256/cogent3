Map protein alignment gaps to DNA alignment gaps
================================================

.. sectionauthor:: Gavin Huttley

Although Cogent3 provides a means for directly aligning codon sequences, you may want to use a different approach based on the translate-align-introduce gaps into the original paradigm. After you've translated your codon sequences, and aligned the resulting amino acid sequences, you want to introduce the gaps from the aligned protein sequences back into the original codon sequences. Here's how.

.. doctest::

    >>> from cogent3 import make_unaligned_seqs, make_aligned_seqs

First I'm going to construct an artificial example, using the seqs dict as a means to get the data into the Alignment object. The basic idea, however, is that you should already have a set of DNA sequences that are in frame (i.e. position 0 is the 1st codon position), you've translated those sequences and aligned these translated sequences. The result is an alignment of aa sequences and a set of unaligned DNA sequences from which the aa seqs were derived. If your sequences are not in frame you can adjust it by either slicing, or adding N's to the beginning of the raw string.

.. doctest::

    >>> seqs = {
    ... 'hum': 'AAGCAGATCCAGGAAAGCAGCGAGAATGGCAGCCTGGCCGCGCGCCAGGAGAGGCAGGCCCAGGTCAACCTCACT',
    ... 'mus': 'AAGCAGATCCAGGAGAGCGGCGAGAGCGGCAGCCTGGCCGCGCGGCAGGAGAGGCAGGCCCAAGTCAACCTCACG',
    ... 'rat': 'CTGAACAAGCAGCCACTTTCAAACAAGAAA'}
    >>> unaligned_DNA = make_unaligned_seqs(seqs, moltype="dna")
    >>> print(unaligned_DNA.to_fasta())  # doctest: +SKIP
    >hum
    AAGCAGATCCAGGAAAGCAGCGAGAATGGCAGCCTGGCCGCGCGCCAGGAGAGGCAGGCCCAGGTCAACCTCACT
    >mus
    AAGCAGATCCAGGAGAGCGGCGAGAGCGGCAGCCTGGCCGCGCGGCAGGAGAGGCAGGCCCAAGTCAACCTCACG
    >rat
    CTGAACAAGCAGCCACTTTCAAACAAGAAA

In order to ensure the alignment algorithm preserves the coding frame, we align the translation of the sequences. We need to translate them first, but note that because the seqs are unaligned they we have to set ``aligned=False``, or we'll get an error.

.. doctest::

    >>> unaligned_aa = unaligned_DNA.get_translation()
    >>> print(unaligned_aa.to_fasta())  # doctest: +SKIP
    >hum
    KQIQESSENGSLAARQERQAQVNLT
    >mus
    KQIQESGESGSLAARQERQAQVNLT
    >rat
    LNKQPLSNKK

The translated seqs can then be written to file, using the method ``write``. That file then serves as input for an alignment program. The resulting alignment file can be read back in. (We won't write to file in this example.) For this example we will specify the aligned sequences in the dict, rather than from file.

.. doctest::

    >>> aligned_aa_seqs = {'hum': 'KQIQESSENGSLAARQERQAQVNLT',
    ... 'mus': 'KQIQESGESGSLAARQERQAQVNLT',
    ... 'rat': 'LNKQ------PLS---------NKK'}
    >>> aligned_aa = make_aligned_seqs(aligned_aa_seqs, moltype="protein")
    >>> aligned_DNA = aligned_aa.replace_seqs(unaligned_DNA)

Just to be sure, we'll check that the DNA sequence has gaps in the right place.

.. doctest::

    >>> print(aligned_DNA)  # doctest: +SKIP
    >hum
    AAGCAGATCCAGGAAAGCAGCGAGAATGGCAGCCTGGCCGCGCGCCAGGAGAGGCAGGCCCAGGTCAACCTCACT
    >rat
    CTGAACAAGCAG------------------CCACTTTCA---------------------------AACAAGAAA
    >mus
    AAGCAGATCCAGGAGAGCGGCGAGAGCGGCAGCCTGGCCGCGCGGCAGGAGAGGCAGGCCCAAGTCAACCTCACG
    <BLANKLINE>
