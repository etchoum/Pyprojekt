#!/bin/usr/env/python
import numpy as np

class Poly:
    def __init__(self, coeffs):
        if not isinstance(coeffs, np.ndarray):
            # Falls Listen übergeben werden, automatisch Array erzeugen
            self.coeffs = np.array(coeffs)
        else:
            # Andernfalls Kopie des Arrays verwenden
            self.coeffs = coeffs.copy()
        # Führende Null-Koeffizienten entfernen.
        self.coeffs = np.trim_zeros(self.coeffs, 'f')

    def degree(self):
        # Falls die Koeffizienten extern modifiziert wurden und führende Nullen
        # enthalten, liefert das hier das falsche Ergebnis. Der Einfachheit halber
        # wird das hier aber nicht abgefangen.
        return self.coeffs.size - 1

    def __repr__(self):
        return "Poly({})".format(self.coeffs)

    def __call__(self, x):
        # Horner-Schema
        val = 0
        for c in self.coeffs:
            val = val*x + c
        return val

    def __eq__(self, other):
        if self.coeffs.size != other.coeffs.size:
            return False
        return (self.coeffs == other.coeffs).all()

    def __add__(self, other):
        a = self.coeffs
        b = other.coeffs
        if a.size < b.size:
            # Dafür sorgen dass a ist mindestens so lang wie b ist
            a, b = b, a
        # Erstelle ein neues Polynom mit den gleichen Koeffizienten
        # a (dabei wird automatisch eine Kopie erzeugt).
        p = Poly(a)
        # Addiere b
        p.coeffs[-b.size:] += b
        return p

    def __neg__(self):
        return Poly(-self.coeffs)

    def __sub__(self, other):
        # Subtrahieren nutzt `__neg__` und `__add__`:
        return self + (-other)

    def __mul__(self, other):
        # Der k-te Koeffizient des Produkts zweier Polynome
        # ist
        #
        #     c[k] = sum_j a[j]*b[k-j],
        #
        # wobei a und b die Koeffizienten der Eingabe-Polynome
        # (self und other) sind und die Summe über alle j läuft,
        # so dass die jeweiligen Indizes nicht außerhalb der
        # Arrays liegen. Der einfachste (wenn auch nicht effizienteste)
        # Weg, Index-Probleme zu vermeiden, ist, a und b zuerst am
        # Ende mit Nullen aufzufüllen, bis ihre Länge gleich der von c
        # ist, und dann immer Blöcke der Länge k+1 vom Anfang zu nehmen,
        # einen davon umzudrehen und jeweils das Skalarprodukt zu
        # berechnen.

        # Anzahl der Elemente von c (Grad + 1)
        n = self.degree() + other.degree() + 1
        c = np.empty(n)

        # a und b mit 0 auffüllen
        a = np.zeros(n)
        a[:self.coeffs.size] = self.coeffs
        b = np.zeros(n)
        b[:other.coeffs.size] = other.coeffs

        for k in range(n):
            c[k] = a[:k+1] @ b[k::-1]

        return Poly(c)
print(Poly([1,2,3]) + Poly([4,5]))
print(Poly([1,2,3]) - Poly([4, 5]))
print(Poly([1,2,3]) * Poly([4,5]))
