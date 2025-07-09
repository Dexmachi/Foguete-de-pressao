# Foguete de Pressão - Projeto Integrador 1

Um sistema completo de análise de lançamento de foguete de pressão d'água com medição automática de trajetória e análise de dados em tempo real.

## 📋 Sobre o Projeto

Este projeto foi desenvolvido para a disciplina de **Projeto Integrador 1** e consiste em:

- **Foguete de pressão d'água**: Sistema de lançamento automático
- **Medição de trajetória**: Coleta de dados GPS e altitude em tempo real
- **Análise de dados**: Cálculos de velocidade, aceleração e plotagem de gráficos
- **Interface web**: Dashboard para visualização dos resultados
- **Histórico**: Armazenamento e consulta de lançamentos anteriores

### 🎯 Funcionalidades

- ✅ Coleta automática de dados GPS durante o voo
- ✅ Cálculo de velocidade instantânea e média
- ✅ Cálculo de aceleração instantânea e média
- ✅ Geração de gráficos interativos (distância x tempo, velocidade x tempo, etc.)
- ✅ Mapeamento da trajetória do foguete
- ✅ Interface web responsiva para monitoramento
- ✅ Sistema de histórico de lançamentos
- ✅ API para simulação de dados de teste

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask**: Framework web principal
- **Flask-SocketIO**: Comunicação em tempo real
- **NumPy**: Cálculos matemáticos e análise numérica
- **Pandas**: Manipulação e análise de dados
- **Matplotlib**: Geração de gráficos estáticos

### Frontend
- **HTML5/CSS3**: Interface do usuário
- **JavaScript**: Interatividade e comunicação com backend
- **Tailwind CSS**: Framework de estilização
- **Plotly**: Gráficos interativos
- **Folium**: Mapas de trajetória

### Dados e Comunicação
- **JSON**: Formato de dados para comunicação
- **CSV**: Armazenamento de dados brutos
- **REST API**: Endpoints para coleta de dados

## 📦 Estrutura do Projeto

```
src/
├── app/                    # Aplicação principal
│   ├── main.py            # Processamento principal dos dados
│   ├── servidor.py        # Servidor Flask e rotas
│   ├── graficos.py        # Geração de gráficos
│   ├── movimento.py       # Cálculos de física
│   └── __init__.py
├── data/                  # Dados coletados
│   ├── dadosRecebidos.json    # Dados em tempo real
│   ├── dados_brutos.csv       # Dados históricos
│   └── dados*.json            # Dados de teste
├── scripts/               # Scripts auxiliares
│   └── API_teste.py       # Simulador de dados GPS
├── templates/             # Templates HTML
│   ├── Frontend.html      # Interface principal
│   └── historico.html     # Página de histórico
├── static/               # Arquivos estáticos
├── tests/               # Testes do sistema
├── requirements.txt     # Dependências Python
└── run.py              # Inicializador do projeto
```

## 🚀 Como Inicializar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd Foguete-de-pressao
```

### 2. Crie um Ambiente Virtual (Recomendado)

```bash
python -m venv venv

# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
cd src
pip install -r requirements.txt
```

### 4. Execute o Projeto

```bash
python run.py
```

O servidor será iniciado em `http://localhost:5000`

### 5. Teste com Dados Simulados (Opcional)

Em outro terminal, execute o simulador de dados:

```bash
cd src/scripts
python API_teste.py
```

## 📊 Como Usar

### 1. Interface Principal
- Acesse `http://localhost:5000`
- Selecione a distância de lançamento
- Clique em "Iniciar Medição" para começar a coleta
- Clique em "Plotar Gráficos" para finalizar e gerar análises

### 2. Visualização de Resultados
- **Gráficos**: Distância x Tempo, Velocidade x Tempo, Aceleração x Tempo
- **Trajetória**: Mapa interativo da rota do foguete
- **Métricas**: Velocidade média, aceleração média, distância total

### 3. Histórico
- Acesse a aba "Histórico" para ver lançamentos anteriores
- Visualize detalhes e gráficos de cada teste
- Compare resultados entre diferentes lançamentos

## 🧪 Estrutura dos Dados

### Formato de Entrada (GPS)
```json
{
    "data": "15/06/2023",
    "hora": "14:30:22",
    "latitude": -23.55052,
    "longitude": -46.633308,
    "altitude": 760.5
}
```

### Dados Calculados
- **Velocidade instantânea**: Derivada da distância pelo tempo
- **Aceleração instantânea**: Derivada da velocidade pelo tempo
- **Velocidade média**: Distância total / tempo total
- **Trajetória**: Coordenadas GPS plotadas em mapa

## 🔧 Scripts Disponíveis

- `python run.py`: Inicia o servidor principal
- `python scripts/API_teste.py`: Simula dados de lançamento
- `python app/main.py --process`: Processa dados manualmente

## 📈 Análises Geradas

1. **Gráfico Distância x Tempo**: Mostra o deslocamento do foguete
2. **Gráfico Velocidade x Tempo**: Velocidade instantânea e média
3. **Gráfico Aceleração x Tempo**: Aceleração instantânea e média
4. **Trajetória Física**: Espaço horizontal x altura relativa
5. **Mapa GPS**: Trajetória real plotada em mapa interativo

## 🎓 Contexto Acadêmico

Este projeto integra conhecimentos de:
- **Física**: Cinemática, dinâmica e análise de movimento
- **Programação**: Python, desenvolvimento web, APIs
- **Matemática**: Cálculo diferencial, análise de dados
- **Engenharia**: Sistemas embarcados, coleta de dados
- **Interface**: Design de experiência do usuário

## 👥 Membros da Equipe

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Dexmachi">
        <img src="https://github.com/Dexmachi.png" width="100px;" alt="Caio Rocha"/>
        <br />
        <sub><b>Caio Rocha de Oliveira</b></sub>
        <br />
        <sub>Matrícula: 232001371</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/enzo-fb">
        <img src="https://github.com/enzo-fb.png" width="100px;" alt="Enzo Fernandes"/>
        <br />
        <sub><b>Enzo Fernandes Borges</b></sub>
        <br />
        <sub>Matrícula: 202017361</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/fhenrique77">
        <img src="https://github.com/fhenrique77.png" width="100px;" alt="Felipe Henrique"/>
        <br />
        <sub><b>Felipe Henrique Oliveira Sousa</b></sub>
        <br />
        <sub>Matrícula: 231012100</sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/LuizFarias21">
        <img src="https://github.com/LuizFarias21.png" width="100px;" alt="Luiz Claudio"/>
        <br />
        <sub><b>Luiz Claudio Barbosa de Farias</b></sub>
        <br />
        <sub>Matrícula: 232014487</sub>
      </a>
    </td>
    <td align="center">
      <img src="https://via.placeholder.com/100x100/cccccc/666666?text=GB" width="100px;" alt="Guilherme Augusto"/>
      <br />
      <sub><b>Guilherme Augusto da Silva Braz</b></sub>
      <br />
      <sub>Matrícula: 222006740</sub>
    </td>
    <td></td>
  </tr>
</table>

