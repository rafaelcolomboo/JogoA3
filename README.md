# 🎮 Dados na Rede - Pacman A3

Um jogo educativo desenvolvido em Python com **Pygame** que ensina sobre segurança digital e coleta de dados na internet.

## 📋 Sobre o Jogo

**Dados na Rede** é um jogo de plataforma educativo onde o jogador controla um personagem que coleta diferentes tipos de dados (emails, localizações, dados bancários) enquanto evita ameaças de segurança como vírus, ransomware, spyware e hackers.

### Objetivos
- Aprender sobre privacidade e segurança digital
- Entender os diferentes tipos de ameaças cibernéticas
- Consciência sobre coleta de dados na internet

## 🎯 Gameplay

- **Controles:** Setas ou WASD para mover
- **Objetivo:** Coletar todos os dados antes de ser atacado
- **Proteção:** Coletar VPN (escudo) para desconectar inimigos
- **Pontuação:** 
  - Email: +10 pontos
  - Localização: +30 pontos
  - Dados Bancários: +50 pontos

## 🚀 Como Jogar

### Opção 1: Executável (Windows)
```powershell
C:\Users\Rafael Colombo\Desktop\pacmanA3 (2)\pacmanA3 (2)\pacmanA3\dist\PacmanA3.exe
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

## 📥 Download

Distribuição pronta (Windows 64-bit) disponível em `PacmanA3-release.zip` no diretório do projeto. O ZIP contém:

- `PacmanA3.exe` (executável)
- `README.md`
- `requirements.txt`

Como executar (PowerShell):

```powershell
cd "C:\caminho\para\pasta\onde\extraiu\o\ZIP"
.\PacmanA3.exe
```

Se o Windows bloquear o arquivo ao baixar, clique com o botão direito no `.exe`, escolha **Propriedades** e selecione **Desbloquear** se disponível. Se houver erro de DLL, instale o Microsoft Visual C++ Redistributable.
