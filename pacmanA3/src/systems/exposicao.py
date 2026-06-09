"""Sistema de barra de exposição de dados pessoais."""
from utils.config import (
    TAMANHO_CELULA, DISTANCIA_EXPOSICAO,
    TAXA_EXPOS_SOBE, TAXA_EXPOS_DESCE, PENALIDADE_MORTE,
)


class SistemaExposicao:
    """Aumenta exposição quando inimigos estão perto; causa vazamento em 100%."""

    def __init__(self):
        self.nivel = 0.0

    def resetar(self):
        """Zera a barra de exposição (nova vida ou nova fase)."""
        self.nivel = 0.0

    def _inimigo_proximo(self, jogador, inimigos) -> bool:
        """Verifica se algum inimigo está dentro do raio de exposição em células."""
        coluna_jogador = int(jogador.x // TAMANHO_CELULA)
        linha_jogador = int(jogador.y // TAMANHO_CELULA)
        for inimigo in inimigos:
            coluna = int(inimigo.x // TAMANHO_CELULA)
            linha = int(inimigo.y // TAMANHO_CELULA)
            distancia = abs(coluna - coluna_jogador) + abs(linha - linha_jogador)
            if distancia < DISTANCIA_EXPOSICAO:
                return True
        return False

    def atualizar(self, jogador, inimigos) -> str | None:
        """
        Atualiza nível de exposição.

        Returns:
            'MORREU' se o jogador perdeu vida por vazamento; None caso contrário.
        """
        if self._inimigo_proximo(jogador, inimigos):
            self.nivel = min(100.0, self.nivel + TAXA_EXPOS_SOBE)
        else:
            self.nivel = max(0.0, self.nivel - TAXA_EXPOS_DESCE)
        if self.nivel < 100.0:
            return None
        self.nivel = 0.0
        jogador.vidas -= 1
        jogador.pontuacao = max(0, jogador.pontuacao - PENALIDADE_MORTE)
        return "MORREU"

    def mensagem_morte(self) -> str:
        """Retorna texto exibido quando o jogador morre por exposição máxima."""
        return "Exposicao de dados"
