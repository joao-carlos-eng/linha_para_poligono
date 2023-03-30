from math import cos
from math import sin
from math import radians
from agrupador.Funcs import ang1
from agrupador.Funcs import distancia3 as dist
import simplekml


def circun(centro, raio):
    c = centro.split(',')
    co = [float(c[1]), float(c[0])]
    K = 1852 * 60
    k = raio / K
    fatias = 36
    ang = 360 / fatias
    cos0 = cos(radians(ang))
    sin0 = sin(radians(ang))

    dY = sin0 * raio / K
    dX = (raio - (cos0 * raio)) / K

    circ = ''
    for f in range(2, fatias + 3):
        circ = circ + f'{co[1] + dX - k},{co[0] - dY},0\n'
        cos0 = cos(radians(ang * f))
        sin0 = sin(radians(ang * f))
        dY = sin0 * raio / K
        dX = (raio - (cos0 * raio)) / K  # print(dX, dY,'\n')
    return circ


def poligono_regular(centro, raio, lados, rotacao=0):
    """

    :param centro: string
    :param raio: int ou float
    :param lados: int
    :param rotacao: angulo
    :return: string de cordenadas
    """
    c = centro.split(',')
    co = [float(c[1]), float(c[0])]
    K = 1852 * 60
    k = raio / K
    fatias = lados
    ang = 360 / fatias

    poli = ''
    for f in range(0, fatias + 1):
        cos0 = cos(radians((ang * f) + rotacao))
        sin0 = sin(radians((ang * f) + rotacao))
        dY = sin0 * raio / K
        dX = (raio + (cos0 * raio)) / K
        poli += f'{co[1] + dX - k},{co[0] + dY},0 '

    return poli


def orientacao(linha):
    rosa = {'N': 0, 'D': 0, 'S': 0, 'E': 0}
    rotacao = 0

    reta = linha.strip().split()

    raio = int(dist(reta[0], reta[1]))
    c = reta[0].split(',')
    co = [float(c[1]), float(c[0])]
    K = 1852 * 60
    k = raio / K
    ang = 90

    pontos = []
    for f in range(1, 5):
        cos0 = cos(radians((ang * f) + rotacao))
        sin0 = sin(radians((ang * f) + rotacao))
        dY = sin0 * raio / K
        dX = (raio + (cos0 * raio)) / K
        pontos.append(f'{co[1] - (dX - k)},{co[0] + dY},0')

    a = reta[1]
    centro = reta[0]
    for (b, ch) in zip(pontos, rosa.keys()):
        rosa[ch] = ang1(a, centro, b)
    # print(rosa)

    for ky, v in rosa.items():
        if min(rosa.values()) == v:
            return ky


def rosa_dos_ventos(linha):
    rosa = {'N': 0, 'D': 0, 'S': 0, 'E': 0}
    rotacao = 0

    reta = linha.strip().split()

    raio = int(dist(reta[0], reta[1]))
    c = reta[0].split(',')
    co = [float(c[1]), float(c[0])]
    K = 1852 * 60
    k = raio / K
    ang = 90

    pontos = []
    for f in range(1, 5):
        cos0 = cos(radians((ang * f) + rotacao))
        sin0 = sin(radians((ang * f) + rotacao))
        dY = sin0 * raio / K
        dX = (raio + (cos0 * raio)) / K
        pontos.append(f'{co[1] - (dX - k)},{co[0] + dY},0')

    a = reta[1]
    centro = reta[0]
    for (b, ch) in zip(pontos, rosa.keys()):
        rosa[ch] = ang1(a, centro, b)
    # print(rosa)

    return rosa


def quadrante(arg, method='str'):
    """
    :param arg: coordenadas da reta.
    :param method: 'str' para coordenadas como string, P2P para coordenadas como lista.
    :return: int, referente ao quadrante da reta.
    """
    rosa = {'N': 0, 'D': 0, 'S': 0, 'E': 0}
    rotacao = 0

    if method == 'str':
        reta = arg[0].strip().split()
    else:
        reta = [arg[0], arg[1]]

    raio = int(dist(reta[0], reta[1]))
    c = reta[0].split(',')
    co = [float(c[1]), float(c[0])]
    K = 1852 * 60
    k = raio / K
    ang = 90

    pontos = []
    for f in range(1, 5):
        cos0 = cos(radians((ang * f) + rotacao))
        sin0 = sin(radians((ang * f) + rotacao))
        dY = sin0 * k
        dX = (raio + (cos0 * raio)) / K
        pontos.append(f'{co[1] - (dX - k)},{co[0] + dY},0')

    a = reta[1]
    centro = reta[0]
    for (b, ch) in zip(pontos, rosa.keys()):
        rosa[ch] = ang1(a, centro, b)
    # print(rosa)

    r = ''
    if rosa['E'] < rosa['D']:
        r += 'E'
    else:
        r += 'D'
    if rosa['N'] < rosa['S']:
        r += 'N'
    else:
        r += 'S'

    # print(inclinacaoX(reta[0], reta[1]))
    # print(inclinacaoY(reta[0], reta[1]))
    quadrantes = {'DN': 1, 'EN': 2, 'ES': 3, 'DS': 4}
    return quadrantes[r]


def inclinacaoX(pA, pB):
    """
    inclinação com base no eixo X
    :param pA: string
    :param pB: string
    :return: float
    """
    p1 = pA.split(',')
    # print(p1)
    d = float(dist(pA, pB))
    K = 1852 * 60
    k = d / K

    eixo = [f'{p1[0]},{p1[1]},0', f'{float(p1[0]) + k},{float(p1[1])},0']

    return ang1(pB, eixo[0], eixo[1])


def inclinacaoY(pA, pB):
    """
    inclinação com base no eixo Y
    :param pA: string
    :param pB: string
    :return: float
    """
    p1 = pA.split(',')
    # print(p1)
    d = float(dist(pA, pB))
    K = 1852 * 60
    k = d / K

    eixo = [f'{p1[0]},{p1[1]},0', f'{float(p1[0])},{float(p1[1]) + k},0']

    return ang1(pB, eixo[0], eixo[1])


def baricentro(reta_1, reta_2):
    """ "
    retorna uma linha que corresponde a mediana de duas retas ou
    erro se essa retas não tiverem ponto em comum
    :param reta_1: lista ou tupla
    :param reta_2: lista ou tupla
    :return: lista de strings
    """
    # v = ponto em comun entre as duas retas (vertice)
    if reta_1[0] == reta_2[0]:
        # print('if 1')
        v = reta_1[0]
        p1 = reta_1[1]
        p2 = reta_2[1]
    elif reta_1[0] == reta_2[1]:
        # print('if 2')
        v = reta_1[0]
        p1 = reta_1[1]
        p2 = reta_2[0]
    elif reta_1[1] == reta_2[0]:
        # print('if 3')
        v = reta_1[1]
        p1 = reta_1[0]
        p2 = reta_2[1]
    elif reta_1[1] == reta_2[1]:
        # print('if 4')
        v = reta_1[1]
        p1 = reta_1[0]
        p2 = reta_2[0]
    else:
        return print('retas não possuem um vertice em comum')
    #   print(p1, v, p2)

    a = p1.split(',')
    b = v.split(',')
    c = p2.split(',')

    xg = (float(a[0]) + float(b[0]) + float(c[0])) / 3
    yg = (float(a[1]) + float(b[1]) + float(c[1])) / 3

    return xg, yg


def bissetriz(reta_1, reta_2):
    """ "
    retorna uma linha que corresponde a mediana de duas retas ou
    erro se essa retas não tiverem ponto em comum
    :param reta_1: lista ou tupla
    :param reta_2: lista ou tupla
    :return: lista de strings
    """
    # v = ponto em comun entre as duas retas (vertice)
    if reta_1[0] == reta_2[0]:
        # print('if 1')
        v = reta_1[0]
        p1 = reta_1[1]
        p2 = reta_2[1]
    elif reta_1[0] == reta_2[1]:
        # print('if 2')
        v = reta_1[0]
        p1 = reta_1[1]
        p2 = reta_2[0]
    elif reta_1[1] == reta_2[0]:
        # print('if 3')
        v = reta_1[1]
        p1 = reta_1[0]
        p2 = reta_2[1]
    elif reta_1[1] == reta_2[1]:
        # print('if 4')
        v = reta_1[1]
        p1 = reta_1[0]
        p2 = reta_2[0]
    else:
        return print('retas não possuem um vertice em comum')
    beta1 = inclinacaoX(
        p1, v
    )  # inclinação de uma das retas em relação ao eixo X
    beta2 = inclinacaoX(
        p2, v
    )  # inclinação de uma das retas em relação ao eixo X

    if beta1 < beta2:
        if 'E' in quadrante(f'{v}, {p1}'):
            # print(quadrante(f'{v}, {p1}'))
            teta = 180 + (beta2 + beta1) / 2
        else:
            # print(quadrante(f'{v}, {p1}'))
            teta = 180 - (beta2 - beta1) / 2
    else:
        ##########################
        teta = (beta1 - beta2) / 2
        ##########################

    reta = poligono_regular(v, 15, 1, teta)

    ponto_b = reta.split(' ')[1]

    return ponto_b


def angulo_bissetriz(reta_1, reta_2):
    """ "
    retorna o angulo da mediana de duas retas em relação ao eixo X ou
    erro se essa retas não tiverem ponto em comum
    :param reta_1: lista ou tupla
    :param reta_2: lista ou tupla
    :return: angulo do tipo float
    """
    # v = ponto em comun entre as duas retas (vertice)
    if reta_1[0] == reta_2[0]:
        # print('if 1')
        v = reta_1[0]
        p1 = reta_1[1]
        p2 = reta_2[1]
    elif reta_1[0] == reta_2[1]:
        # print('if 2')
        v = reta_1[0]
        p1 = reta_1[1]
        p2 = reta_2[0]
    elif reta_1[1] == reta_2[0]:
        # print('if 3')
        v = reta_1[1]
        p1 = reta_1[0]
        p2 = reta_2[1]
    elif reta_1[1] == reta_2[1]:
        # print('if 4')
        v = reta_1[1]
        p1 = reta_1[0]
        p2 = reta_2[0]
    else:
        return print('retas não possuem um vertice em comum')
    beta1 = inclinacaoX(
        v, p1
    )  # inclinação de uma das retas em relação ao eixo X
    print(quadrante([v, p1], method='P2P'))
    beta2 = inclinacaoX(
        v, p2
    )  # inclinação de uma das retas em relação ao eixo X
    print(quadrante([v, p2], method='P2P'))
    bs = (beta1 - beta2) / 2

    if bs < 0:
        bs = -bs

    print(f'B1:{beta1} B2:{beta2} bs:{bs}')
    if (
        quadrante([v, p1], method='P2P') == 1
        and quadrante([v, p2], method='P2P') == 2
    ):
        teta = 180 - bs
    elif (
        quadrante([v, p1], method='P2P') == 1
        and quadrante([v, p2], method='P2P') == 3
    ):
        teta = 180 - bs
    elif (
        quadrante([v, p1], method='P2P') == 1
        and quadrante([v, p2], method='P2P') == 4
    ):
        teta = 180 - bs
    elif (
        quadrante([v, p1], method='P2P') == 2
        and quadrante([v, p2], method='P2P') == 1
    ):
        teta = 180 + bs
    elif (
        quadrante([v, p1], method='P2P') == 2
        and quadrante([v, p2], method='P2P') == 2
    ):
        teta = 180 - (beta1 - bs)
    elif (
        quadrante([v, p1], method='P2P') == 2
        and quadrante([v, p2], method='P2P') == 3
    ):
        teta = 180 + bs
    elif (
        quadrante([v, p1], method='P2P') == 2
        and quadrante([v, p2], method='P2P') == 4
    ):
        teta = 180 + bs
    elif (
        quadrante([v, p1], method='P2P') == 3
        and quadrante([v, p2], method='P2P') == 1
    ):
        teta = -bs
    elif (
        quadrante([v, p1], method='P2P') == 3
        and quadrante([v, p2], method='P2P') == 2
    ):
        teta = -bs
    elif (
        quadrante([v, p1], method='P2P') == 3
        and quadrante([v, p2], method='P2P') == 4
    ):
        teta = -(beta1 - bs)
    elif (
        quadrante([v, p1], method='P2P') == 4
        and quadrante([v, p2], method='P2P') == 3
    ):
        teta = 180 - (beta1 + bs)
    elif quadrante([v, p1], method='P2P') == quadrante([v, p2], method='P2P'):
        teta = -(beta1 - bs)
    else:
        teta = bs

    return teta


if __name__ == '__main__':
    import xml.etree.ElementTree as Et

    # ponto = Et.parse('ponto.kml')
    # doc = ponto.getroot()
    # #
    # for co in doc.iter('{http://www.opengis.net/kml/2.2}coordinates'):
    #     c = co.text
    #     p = poligono_regular(c, 3, 4)
    #     cord = []
    #     co = p.split()
    #     co.pop()
    #     for i in co:
    #         x, y, z = i.split(',')
    #         cord.append((float(x), float(y)))
    #     kml = simplekml.Kml(open=1)
    #     poli = kml.newlinestring(name='quadrado')
    #     poli.coords = cord
    #     print(cord)
    #     cnt = 0
    #     for i in cord:
    #         cnt += 1
    #         ponto = kml.newpoint(name=f'P{cnt}', coords=[i])
    #     kml.save('quadrado.kml')
    # Criar um hexagono com o dobro do raio do anterior
    #   Coletar os pontos desse novo Hexa e fazer outros padroes com esses centros.

    linha = Et.parse('testQ.kml')
    doc = linha.getroot()
    for co in doc.iter('{http://www.opengis.net/kml/2.2}coordinates'):
        c = co.text.split()
        print(quadrante(co.text))
        # kml = simplekml.Kml(open=1)
        # for i in range(1, len(c) - 1):
        #     long, lat, alt = c[i].split(",")
        #     b = quadrante(co.text)
        # r = b.split(',')
        # cord = (float(r[0]), float(r[1]))
        # linha = kml.newlinestring(name=f'{i}', coords=[(float(long), float(lat)), cord])
        # linha.style.linestyle.width = 3
        # linha.style.linestyle.color = simplekml.Color.blue
        # kml.save('Bissetriz.kml')
        #   kml = simplekml.Kml(open=1, name='90g')
        # cnt = 0
        # for i in range(1, len(c) - 1):
        #     cnt += 1
        #     ab = angulo_bissetriz([c[i], c[i - 1]], [c[i], c[i + 1]])
        #     co = poligono_regular(c[i], 15, 1, ab)
        #     try:
        #         x, y, z = co.split(',')
        #         ponto = kml.newpoint(name=f'P{cnt}', coords=[(float(x), float(y))])
        #     except:
        #         pass
        # kml.save('90g.kml')
