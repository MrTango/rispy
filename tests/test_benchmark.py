import rispy

EXAMPLE_RECORD = """
42.
TY  - JOUR
ID  - 12345
T1  - The title of the reference
A1  - Marxus, Karlus
A1  - Lindgren, Astrid
A2  - Glattauer, Daniel
Y1  - 2006//
N2  - BACKGROUND: Lorem dammed ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.
KW  - Pippi Langstrumpf
KW  - Nordwind
KW  - Piraten
KW  - Seeräuber
KW  - Kinderbuch
KW  - Astrid Lindgren
JF  - Lorem ipsum dolor sit amet
JA  - lorem ipsum dolor sit amet
VL  - 6
IS  - 3
SP  - e0815341
CY  - Germany
PB  - Dark Factory
SN  - 1732-4208
M1  - 1228150341
L2  - http://example2.com
UR  - http://example.com/1
UR  - http://example.com/2
UR  - http://example.com/3
DO  - 10.1371/journal.pone.0081534
ER  -

"""  # noqa


EXAMPLE_RECORD_MULTILINE = """
42.
TY  - JOUR
ID  - 12345
T1  - The title of the reference
A1  - Marxus, Karlus
A1  - Lindgren, Astrid
A2  - Glattauer, Daniel
Y1  - 2006//
N2  - BACKGROUND: Lorem dammed ipsum dolor sit amet,
consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.
    - Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus
    - mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem.
      Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet
nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam
dictum felis eu pede mollis pretium.
KW  - Pippi Langstrumpf
KW  - Nordwind
KW  - Piraten
KW  - Seeräuber
KW  - Kinderbuch
KW  - Astrid Lindgren
JF  - Lorem ipsum dolor sit amet
JA  - lorem ipsum dolor sit amet
VL  - 6
IS  - 3
SP  - e0815341
CY  - Germany
PB  - Dark Factory
SN  - 1732-4208
M1  - 1228150341
L2  - http://example2.com
UR  - http://example.com/1
UR  - http://example.com/2
UR  - http://example.com/3
DO  - 10.1371/journal.pone.0081534
ER  -

"""


def test_benchmark_rispy_large(benchmark):
    benchmark_dataset = EXAMPLE_RECORD * 10000

    benchmark(rispy.loads, benchmark_dataset)


def test_benchmark_rispy_large_multiline(benchmark):
    benchmark_dataset = EXAMPLE_RECORD_MULTILINE * 10000

    benchmark(rispy.loads, benchmark_dataset)
