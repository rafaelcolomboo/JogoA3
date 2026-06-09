"""Colisão entre jogador e inimigos."""
from utils.config import PENALIDADE_MORTE


def processar_colisoes(jogador, inimigos) -> tuple[str | None, str, tuple | None]:
    """
    Verifica colisão do jogador com cada inimigo.

    Returns:
        (novo_estado, nome_atacante, feedback_opcional)
    """
    for inimigo in inimigos:
        if not jogador.rect.colliderect(inimigo.rect):
            continue
        if inimigo.assustado:
            inimigo.resetar()
            jogador.pontuacao += 200
            feedback = ("+200 ameaca neutralizada", (0, 255, 200, 255),
                        inimigo.rect.centerx, inimigo.rect.centery)
            return None, "", feedback
        jogador.vidas -= 1
        jogador.pontuacao = max(0, jogador.pontuacao - PENALIDADE_MORTE)
        return "MORREU", inimigo.nome, None
    return None, "", None
