# Dados na Rede

Jogo educativo inspirado no Pac-Man sobre **coleta, armazenamento e uso de dados na internet**, desenvolvido como trabalho acadêmico (A3 — Exploração Digital).

O jogador navega por uma rede representada em estilo **Matrix** (verde neon sobre fundo escuro), coletando dados pessoais espalhados pelo mapa. Os inimigos personificam **ameaças digitais**: vírus, spyware, ransomware e hacker. O power-up **VPN** desconecta temporariamente os malwares, permitindo neutralizá-los.

## Integrantes

- Enrico
- Marcos
- Rafael
- Vinicius

## Tecnologias utilizadas

- Python 3.11.9
- Pygame 2.6.1

## Como rodar

1. Crie e ative um ambiente virtual (recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a partir da **pasta raiz** do projeto (`pacmanA3/`):

```bash
python main.py
```

## Controles

| Tecla | Ação |
|-------|------|
| Setas ou WASD | Mover o usuário na rede |
| ENTER | Iniciar / continuar após morte / próxima fase / voltar ao menu |

## Estrutura do projeto

```
pacmanA3/
├── main.py                 # Ponto de entrada: inicia ControleJogo
├── requirements.txt        # Dependência pygame
├── assets/
│   ├── sprites/
│   │   ├── inimigos/       # virus.png, spyware.png, ransomware.png, hacker.png
│   │   └── dados/          # powerup.png (VPN); ponto.png opcional
│   ├── sounds/             # Reservado para efeitos sonoros
│   
├── src/
│   ├── entities/           # Jogador, inimigos (malware), coletáveis, direções
│   ├── scenes/             # Menu, overlays de morte/game over, resultado de fase
│   ├── systems/            # Loop, colisão, exposição, HUD, sprites, distribuição
│   └── utils/              # Constantes (config.py) e desenho procedural
└── docs/
    └── README.md           # Este arquivo
```

### Descrição das pastas

| Pasta | Responsabilidade |
|-------|------------------|
| `assets/sprites/inimigos` | PNGs dos quatro tipos de malware |
| `assets/sprites/dados` | Sprites dos coletáveis (VPN em `powerup.png`) |
| `assets/sounds` | Áudios futuros (vazio por enquanto) |
| `src/entities` | Classes de entidade: movimento, IA, coleta |
| `src/scenes` | Telas que não dependem do estado do labirinto |
| `src/systems` | Regras transversais: colisão, pontuação visual, carregamento |
| `src/utils` | Valores fixos do jogo e geração de arte quando falta PNG |

## Mecânicas principais

- Colete **e-mails** (+10), **localizações** (+30) e **dados bancários** (+50)
- Ative o **VPN** para deixar inimigos vulneráveis por 8 segundos (+200 ao neutralizar)
- Evite a barra de **exposição** quando ameaças estiverem a menos de 3 células
- Complete a fase coletando todos os arquivos; ao final, leia o feedback educativo
- Morte por colisão ou exposição máxima: −100 pontos e perda de uma vida

## Assets

Coloque PNGs com fundo transparente em `assets/sprites/inimigos/` e `assets/sprites/dados/`.  
Se um arquivo não existir, o jogo usa sprites gerados por código automaticamente (sem alterar a jogabilidade).

Nomes esperados (definidos em `src/utils/config.py`):

- `virus.png`, `spyware.png`, `ransomware.png`, `hacker.png`
- `powerup.png` (VPN)
