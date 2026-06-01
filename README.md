# Simulador 3D: Par de Pontos Mais Proximos

Aplicacao didatica em Python para demonstrar o algoritmo do **Par de Pontos Mais Proximos** em um espaco 3D. A cena gera entre 20 e 50 pontos aleatorios, representa cada ponto como uma esfera e destaca automaticamente as duas esferas com menor distancia euclidiana entre si.

## Video da apresentacao

[Assistir ao video da apresentacao](https://drive.google.com/file/d/1eNSKGQj5EOOuopyaHCI-NOGbMmH4suMo/view?usp=sharing)

## Biblioteca escolhida

O projeto usa **VPython** porque e simples para visualizacao 3D, funciona bem em Windows e permite criar esferas, linhas, camera e textos com poucas linhas de codigo. Ao executar o programa, o VPython abre a visualizacao 3D no navegador.

## Instalar dependencias

Requisitos:

- Python 3.10 ou superior
- Windows, Linux ou macOS

No Windows, dentro da pasta do projeto, execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se a execucao de scripts do PowerShell estiver bloqueada, use:

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## Rodar o simulador

Com o ambiente virtual ativado:

```powershell
python closest_pair_3d.py
```

Ou sem ativar o ambiente:

```powershell
.\.venv\Scripts\python closest_pair_3d.py
```

## Controles

Na janela 3D aparecem dois botoes:

- `Forca bruta`: executa a busca O(n^2).
- `Dividir e conquistar`: executa a versao recursiva com divisao pela coordenada `x` e verificacao da faixa central.

## O que aparece

- Esferas azuis: pontos 3D gerados aleatoriamente.
- Esferas vermelhas: os dois pontos mais proximos encontrados.
- Linha amarela: ligacao entre o par mais proximo.
- Texto na cena: menor distancia encontrada.
- Console: quantidade de pontos, coordenadas dos dois pontos, distancia, quantidade de comparacoes e complexidade.

## Como o algoritmo funciona

A primeira versao usa **forca bruta O(n^2)**. Para cada ponto, o algoritmo compara sua distancia com todos os pontos seguintes da lista. A distancia entre dois pontos 3D e calculada por:

```text
distancia = sqrt((x2 - x1)^2 + (y2 - y1)^2 + (z2 - z1)^2)
```

Durante as comparacoes, o programa guarda o menor valor encontrado e os dois pontos associados a ele. Ao final, esse par e enviado para a parte visual do simulador.

A segunda estrategia usa **dividir e conquistar**. O conjunto e ordenado pela coordenada `x`, dividido em duas metades, resolvido recursivamente e depois combinado com uma faixa central para capturar pares que cruzam a divisao.

## Como o simulador demonstra a aplicabilidade

O simulador transforma um problema abstrato de geometria computacional em uma cena visual. Em vez de olhar apenas para uma lista de coordenadas, o usuario ve varios pontos no espaco 3D e observa claramente qual par esta mais proximo, reforcando aplicacoes como deteccao de proximidade, simulacoes fisicas, jogos, robotica, agrupamento de dados e analise espacial.

## Organizacao do codigo

- `Point3D`: estrutura que representa um ponto com `x`, `y` e `z`.
- `distance_3d`: calcula a distancia euclidiana 3D.
- `closest_pair_brute_force`: encontra o par mais proximo usando forca bruta.
- `closest_pair_divide_and_conquer`: encontra o par mais proximo por divisao e conquista.
- `find_closest_pair`: ponto de entrada para trocar o algoritmo no futuro.
- `create_base_point_graphics`: cria as esferas dos pontos uma unica vez.
- `apply_result_visuals`: destaca o resultado calculado na visualizacao.
- `register_controls`: cria os botoes da interface.

Essa separacao permite substituir futuramente a funcao de forca bruta por uma abordagem baseada em divisao e conquista sem reescrever a renderizacao.
