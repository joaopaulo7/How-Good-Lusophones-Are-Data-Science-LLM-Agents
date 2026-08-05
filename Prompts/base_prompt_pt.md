Você deve resolver, em um notebook Jupyter em português, a seguinte competição de engenharia de aprendizado de máquina do site Kaggle:

**Detalhes da Competição**
- **nome:** {competition_title}
- **descrição:** {overview}
- **métrica de avaliação:** {evaluation_metric}
- **formato de submissão:** {submission_format}
- **coluna objetivo:** {target_column}

**Instruções**
Os dados de treinamento estão em um arquivo chamado `train.csv` e os dados de teste estão em um arquivo chamado `test.csv`.
Você deve usar os dados de treinamento para treinar um modelo de aprendizado de máquina e, em seguida, utilizar os dados de teste para criar um arquivo de submissão chamado `submission.csv`, prevendo a coluna objetivo e usando o formato de submissão correto. O conjunto de teste não contém a coluna `{target_column}`.
Obtenha a melhor pontuação possível, mas certifique-se de que um arquivo `submission.csv` seja gerado dentro do limite de tempo de 60 minutos; você pode atualizar o arquivo com previsões melhores.

**Especificações do Sistema**
- **SO:** Ubuntu 22.04 Jammy
- **CPU:** Intel Core i7-10700F @ 16x 4,8GHz
- **RAM:** 128 GiB
- **GPU:** Não disponível
- **Pacotes disponíveis:** numpy, pandas, xgboost, seaborn, scipy, scikit-learn, catboost, matplotlib

**Instruções Adicionais**
- Garanta que todo o código possa ser executado nas especificações do sistema disponíveis.
- Certifique-se de validar os modelos com um conjunto de validação (holdout set) antes de treinar no conjunto completo.
- Ao processar os dados, lembre-se sempre de que o conjunto de teste não tem a coluna `{target_column}`.
- Certifique-se de codificar e decodificar os dados corretamente antes do treinamento e da inferência.
- Verifique a presença de ruído nos dados, incluindo valores ausentes e outliers.
- Sempre garanta que as previsões estão no formato correto antes de criar o arquivo de submissão.
- Garanta que o tempo total de execução seja inferior a 60 minutos; use até 16 threads de CPU.
- Crie o arquivo `submission.csv` inicial, com as predições base para o conjunto de teste, **antes** de otimizar os hiperparâmetros.
