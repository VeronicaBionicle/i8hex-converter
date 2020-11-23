from numpy import pi, sin, cos, savetxt

size_n = 63 #60 points for function generator

def glin(size_n):
    return [int(i*(255/size_n)) for i in range(size_n+1)]

def triangle(size_n):
    res = [i for i in range(0, 255, 2*255//size_n)]
    return res + [255] + res[1:][::-1]

def sinus(size_n):
    return [int(127.5-127.5*sin(i*(2*pi/size_n))) for i in range(size_n+1)]

def fantasy(size_n):
    return [int(127.5-127.5*sin(2.5*cos(i*(2*pi/size_n)))) for i in range(size_n+1)]

data = glin(size_n)+triangle(size_n)+sinus(size_n)+fantasy(size_n)

savetxt("D:/Python/intel_hex/input/input.txt", data, fmt = '%d', delimiter='', newline=',')