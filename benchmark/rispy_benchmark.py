import timeit

import rispy  # noqa

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


def make_dataset(n=10000):
    return EXAMPLE_RECORD * n


if __name__ == "__main__":
    ristext = make_dataset()

    time_result = timeit.timeit("rispy.loads(ristext)", globals=globals(), number=100)
    print(f"Time: {time_result:.4f} s")
