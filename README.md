# 🎮 Dados na Rede - A3

Um jogo educativo desenvolvido em Python com **Pygame** inspirado no Pac-Man sobre coleta, armazenamento e uso de dados na internet, desenvolvido como trabalho acadêmico (A3 — Exploração Digital).

## 📋 Sobre o Jogo

**Dados na Rede** o jogador navega por uma rede representada em estilo Matrix (verde neon sobre fundo escuro), coletando dados pessoais espalhados pelo mapa. Os inimigos personificam ameaças digitais: vírus, spyware, ransomware e hacker. O power-up VPN desconecta temporariamente os malwares, permitindo neutralizá-los.

## 🎯 Gameplay

- **Controles:** Setas ou WASD para mover
- **Objetivo:** Coletar todos os dados antes de ser atacado
- **Proteção:** Coletar VPN (escudo) para desconectar inimigos
- **Pontuação:** 
  - Email: +10 pontos
  - Localização: +30 pontos
  - Dados Bancários: +50 pontos

## 🚀 Como Baixar

### Opção 1: Download (ZIP)

Baixe `PacmanA3-release.zip` na raiz do repositório e extraia em uma pasta. O ZIP contém o executável pronto para Windows 64-bit.

Abra o PowerShell na pasta extraída e rode:

```powershell
.\PacmanA3.exe
```

### Opção 2: Código Fonte (Python)

1. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Execute o jogo:**
   ```powershell
   python pacmanA3/main.py
   ```

## 📦 Dependências

- Python 3.11+
- pygame-ce 2.5.7
- Windows 10/11

Todas as dependências estão em `requirements.txt`

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
pacmanA3/
├── main.py              # Ponto de entrada
├── assets/              # Sprites e sons
│   ├── sprites/
│   └── sounds/
├── src/
│   ├── entities/        # Jogador, Inimigos, Dados
│   ├── scenes/          # Telas do jogo
│   ├── systems/         # Lógica de jogo
│   └── utils/           # Configurações e utilitários
└── docs/                # Documentação
```

### Entidades
- **Jogador:** Personagem controlável
- **Inimigos:** Vírus, Ransomware, Spyware, Hackers
- **Dados:** Itens colecionáveis (Email, Localização, Dados Bancários, VPN)

### Sistemas
- **Controle de Jogo:** Gerencia estados e loop principal
- **Colisão:** Detecta colisões com inimigos
- **Exposição:** Sistema de risco baseado em proximidade
- **Render:** Renderização de cenário e HUD

## 👥 Colaboração

Se quiser contribuir:

1. **Faça um Fork** do projeto
2. **Crie uma branch** para sua feature:
   ```powershell
   git checkout -b feature/minha-feature
   ```
3. **Faça commit** das alterações:
   ```powershell
   git add .
   git commit -m "Descrição da alteração"
   ```
4. **Faça Push** e abra um **Pull Request**

## 📝 Licença

Projeto educativo - Livre para uso


