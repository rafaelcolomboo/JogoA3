"""Ponto de entrada do jogo Dados na Rede."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.systems.controle_jogo import ControleJogo

if __name__ == "__main__":
    ControleJogo().executar()