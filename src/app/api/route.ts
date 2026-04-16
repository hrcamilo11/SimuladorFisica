import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    "message": "Bienvenido a la API del Simulador de Física en Next.js.",
    "categories": [
      {
        "name": "Cinemática",
        "path": "/cinematica",
        "simulations": [
          "movimiento-armonico-simple",
          "caida-libre",
          "pendulo-simple",
          "movimiento-circular-uniforme",
          "mruv",
          "mru",
          "tiro-parabolico"
        ]
      },
      {
        "name": "Colisiones",
        "path": "/colisiones",
        "simulations": [
          "colision-perfectamente-inelastica-1d",
          "colision-elastica-1d",
          "colision-perfectamente-inelastica-2d",
          "colision-elastica-3d",
          "colision-elastica-2d"
        ]
      },
      {
        "name": "Dinámica",
        "path": "/dinamica",
        "simulations": [
          "plano-inclinado",
          "leyes-newton",
          "plano-inclinado-polea"
        ]
      },
      {
        "name": "Energía",
        "path": "/energia",
        "simulations": [
          "energia-potencial-gravitatoria",
          "energia-potencial-elastica",
          "trabajo-energia"
        ]
      },
      {
        "name": "Electricidad y Magnetismo",
        "path": "/electricidad-y-magnetismo",
        "simulations": [
          "resistencia",
          "leyes-kirchhoff",
          "potencia-electrica",
          "calculos-circuitos",
          "magnetismo",
          "inductancia",
          "capacitancia",
          "ley-ohm"
        ]
      },
      {
        "name": "Ondas",
        "path": "/ondas",
        "simulations": [
          "ondas"
        ]
      }
    ]
  });
}
