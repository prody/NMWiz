#!/bin/env python
import sys, getopt, os, re, cStringIO

filename=sys.argv[1]
if filename=="":
    exit("ERROR: INPUT FILE NEEDED.")
f=open(filename)
lines=f.readlines()

xyzstart=0
nmstart=0
nmistart=0
nmlstart=0

xyzend=len(lines)
nmend=len(lines)
nmiend=len(lines)
nmlend=len(lines)
for i in range(0,len(lines)):
    if lines[i]== " Current geometry (xyz format, in Angstrom)\n": 
        xyzstart=i
        break
else:
    exit()
for i in range(xyzstart,len(lines)):
    if lines[i]== " Normal Modes\n": 
        nmstart=i
        break
else:
    exit()
for i in range(xyzstart,len(lines)):
    if lines[i]== " Normal Modes of imaginary frequencies\n": 
        nmistart=i
        nmend=i
        break
for i in range(xyzstart,len(lines)):
    if lines[i]== " Normal Modes of low/zero frequencies\n": 
        nmlstart=i
        nmiend=i
        if nmistart==0 : 
            nmend=i
        break
for i in range(xyzstart,len(lines)):
    if lines[i].find("Zero point energy:")!=-1:
        nmlend=i
        break
#print xyzstart, nmstart, nmistart, nmlstart

natoms=int(lines[xyzstart+2].split()[0])
atoms=[]
coord=[]
for line in lines[xyzstart+4:xyzstart+4+natoms]:
    words=line.split()
    #print line
    atoms.append(line.split()[0])
    coord.append(words[1])
    coord.append(words[2])
    coord.append(words[3])

modes=[]
for i in range(0,natoms*natoms*9):
    modes.append("")

#while True:
j=0
if nmistart!=0:
    for i in range(nmistart, nmiend):
    #for m in range(1,10):
        line=lines[i]
        if not line: break
        if line[0]!="\n":
            words=line[:-1].split()
            if words[0].find("G")!=-1:
                if words[0]=="GX1":
                    k=0
                for l in range(1,len(words)):
                    #print j ,l ,k 
                    modes[(j+l-1)*natoms*3+k]=words[l]
                k=k+1
                if words[0]=="GZ"+"%d"%natoms:
                    j=j+len(words)-1


#print nmlstart, nmlend, j, natoms
for i in range(nmlstart, nmlend):
#for m in range(1,10):
    line=lines[i]
    if not line: break
    if line[0]!="\n":
        words=line[:-1].split()
        if words[0].find("G")!=-1:
            if words[0]=="GX1":
                k=0
            for l in range(1,len(words)):
                #print j ,l ,k 
                modes[(j+l-1)*natoms*3+k]=words[l]
            k=k+1
            if words[0]=="GZ"+"%d"%natoms:
                j=j+len(words)-1

for i in range(nmstart, nmend):
#for m in range(1,10):
    line=lines[i]
    if not line: break
    if line[0]!="\n":
        words=line[:-1].split()
        if words[0].find("G")!=-1:
            if words[0]=="GX1":
                k=0
            for l in range(1,len(words)):
                modes[(j+l-1)*natoms*3+k]=words[l]
            k=k+1
            if words[0]=="GZ"+"%d"%natoms:
                j=j+len(words)-1
# print j
#quit()
print "coordinates ",
for i in range(0,natoms*3):
    print coord[i],
print

print "atomnames",
for i in range(0,natoms):
    print atoms[i],
print

for i in range(0,natoms*3):
    print "mode ",i,
    for j in range(0,natoms):
        print modes[i*natoms*3+j*3+0], modes[i*natoms*3+j*3+1], modes[i*natoms*3+j*3+2],
    print
