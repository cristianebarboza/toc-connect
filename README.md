# TOC-Connect

**Protótipo acadêmico em Python para investigar conectividade funcional em rs-fMRI de pessoas com Transtorno Obsessivo-Compulsivo (TOC), usando dados públicos estruturados em BIDS.**

> Este repositório é uma demonstração de escopo para uma possível pós-graduação. Não é software clínico, não diagnostica e não deve orientar tratamento.

## Ideia em linguagem simples

Imagens de ressonância em repouso permitem estimar se regiões do cérebro apresentam sinais que variam juntas ao longo do tempo. O TOC-Connect automatiza uma parte desse trabalho: recebe a imagem funcional, extrai o sinal de regiões selecionadas do circuito cortico-estriato-talâmico-cortical (CSTC), calcula a relação entre elas e produz um relatório visual reprodutível.

O projeto foi pensado para bases abertas como o dataset OpenNeuro `ds008110` (OCD Structural and Functional Connectivity Study), sempre respeitando a licença e a documentação da base.

## O que este MVP faz

- localiza imagens `*_bold.nii` ou `*_bold.nii.gz` num diretório BIDS;
- extrai séries temporais por região usando máscaras NIfTI;
- calcula uma matriz de correlação de Pearson e aplica transformação de Fisher-z;
- guarda matrizes em CSV e gera um mapa de calor em PNG;
- cria um resumo de execução em JSON, incluindo parâmetros e arquivos processados.

## Instalação

```bash
git clone https://github.com/SEU-USUARIO/toc-connect.git
cd toc-connect
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -e .
```

## Uso

Você precisa de dados de rs-fMRI pré-processados (por exemplo, saída de fMRIPrep) e máscaras NIfTI das regiões de interesse no mesmo espaço da imagem funcional.

```bash
toc-connect run \
  --bids-dir /caminho/para/dados_bids \
  --masks-dir /caminho/para/mascaras \
  --output-dir results \
  --tr 2.0
```

Exemplo de nomes de máscaras: `OFC.nii.gz`, `caudado.nii.gz`, `putamen.nii.gz`, `talamo.nii.gz`, `ACC.nii.gz`.

Saídas esperadas em `results/`:

```text
sub-01/
  connectivity_fisher_z.csv
  connectivity_heatmap.png
run_summary.json
```

## Fluxo científico proposto

1. Selecionar uma base pública BIDS e verificar termos de uso, variáveis clínicas e qualidade.
2. Pré-processar rs-fMRI com uma ferramenta validada, como fMRIPrep; incluir regressão de ruído e *scrubbing* segundo um plano pré-especificado.
3. Definir as ROIs CSTC antes da análise, usando atlas e referências científicas adequadas.
4. Executar o TOC-Connect para obter conectividade por participante.
5. Associar as métricas a fenótipos que estejam efetivamente disponíveis, controlando confundidores e corrigindo testes múltiplos.
6. Reproduzir os resultados em outra base compatível, quando possível.

## Limites importantes

- Uma correlação de rs-fMRI **não prova** que uma região causa sintomas.
- Bases abertas podem não ter controles saudáveis, escalas clínicas completas ou dados homogéneos entre locais.
- Este código é um ponto de partida. Para resultados publicáveis, são necessários plano estatístico, validação, versionamento dos dados e supervisão metodológica/clínica.

## Organização

```text
toc_connect/       código do pacote
examples/          demonstração com dados sintéticos
tests/             testes automatizados
```

## Licença

MIT. Ao reutilizar dados públicos, mantenha separadamente as citações e condições de licença do repositório de origem.
