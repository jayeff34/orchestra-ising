### Everything is taken from:
### https://github.com/qiskit-community/qiskit-community-tutorials/blob/master/awards/teach_me_qiskit_2018/exact_ising_model_simulation/Ising_time_evolution.ipynb
### in order to replicate the paper https://quantum-journal.org/papers/q-2018-12-21-114/

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

from math import pi
import numpy as np


def digit_sum(n):
    num_str = str(n)
    sum = 0
    for i in range(0, len(num_str)):
        sum += int(num_str[i])
    return sum

# CZ (Controlled-Z)
# control qubit: q0
# target qubit: q1
def CZ(qp,q0,q1):
    qp.h(q1)
    qp.cx(q0,q1)
    qp.h(q1)
# f-SWAP
# taking into account the one-directionality of CNOT gates in the available devices
def fSWAP(qp,q0,q1):
    qp.cx(q0,q1)
    qp.h(q0)
    qp.h(q1)
    qp.cx(q0,q1)
    qp.h(q0)
    qp.h(q1)
    qp.cx(q0,q1)
    CZ(qp,q0,q1)

# CH (Controlled-Haddamard)
# control qubit: q1
# target qubit: q0
def CH2(qp,q0,q1):
    RZ(qp,-pi/2.,q0)
    qp.h(q0)
    RZ(qp,-pi/4.,q0)
    qp.h(q0)
    qp.h(q1)
    qp.cx(q0,q1)
    qp.h(q0)
    qp.h(q1)
    qp.t(q0)
    qp.h(q0)
    qp.s(q0)

# Fourier transform gates
def F2(qp,q0,q1):
    qp.cx(q0,q1)
    CH2(qp,q0,q1)
    qp.cx(q0,q1)
    CZ(qp,q0,q1) 

def F0(qp,q0,q1):
    F2(qp,q0,q1)

def F1(qp,q0,q1):
    F2(qp,q0,q1)
    RZ(qp,-pi/2.,q0)


# ROTATIONAL GATES
def RZ(qp,th,q0):
    qp.rz(-th,q0)
def RY(qp,th,q0):
    qp.ry(th,q0)
def RX(qp,th,q0):
    qp.rx(th,q0)

# CRX (Controlled-RX)
# control qubit: q0
# target qubit: q1
def CRX(qp,th,q0,q1):
    RZ(qp,pi/2.0,q1)
    RY(qp,th/2.0,q1)
    qp.cx(q0,q1)
    RY(qp,-th/2.0,q1)
    qp.cx(q0,q1)
    RZ(qp,-pi/2.0,q1)
# Bogoliubov B_1
def B(qp,thk,q0,q1):
    qp.x(q1)
    qp.cx(q1,q0)
    CRX(qp,thk,q0,q1)
    qp.cx(q1,q0)
    qp.x(q1)

# It can also be implemented between other qubits or in ibqmx2 and ibqmx4 using fermionic SWAPS
# For instance, the lines commented correspond to the implementations:
# ibmqx2 (q0,q1,q2,q3)=(4,2,0,1)
# ibmqx4 (q0,q1,q2,q3)=(3,2,1,0)
def Udisg(Udis,lam,q0,q1,q2,q3):
    k=1
    n=4
    th1=-np.arccos((lam-np.cos(2*pi*k/n))/np.sqrt((lam-np.cos(2*pi*k/n))**2+np.sin(2*pi*k/n)**2))
    B(Udis,th1,q0,q1)
    F1(Udis,q0,q1)
    F0(Udis,q2,q3)
    #fSWAP(Udis,q2,q1) # for ibmqx2
    #fSWAP(Udis,q1,q2) # for ibmqx4
    F0(Udis,q0,q2)
    F0(Udis,q1,q3)
    #fSWAP(Udis,q2,q1) # for ibmqx2
    #fSWAP(Udis,q1,q2) # for ibmqx4

def Initial(qc,lam,q0,q1,q2,q3):
    if lam <1:
        qc.x(q3)

def Ising(qc,lam,q0,q1,q2,q3,c0,c1,c2,c3):
    Initial(qc,lam,q0,q1,q2,q3)
    Udisg(qc,lam,q0,q1,q2,q3)
    qc.measure(q0,c0)
    qc.measure(q1,c1)
    qc.measure(q2,c2)
    qc.measure(q3,c3)


def get_ising(lam=0.5):
    q = QuantumRegister(4)
    c = ClassicalRegister(4)
    qc = QuantumCircuit(q,c)
    
    Ising(qc,lam,q[0],q[1],q[2],q[3],c[0],c[1],c[2],c[3])
    return qc