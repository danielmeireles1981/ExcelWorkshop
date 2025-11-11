from django.core.management.base import BaseCommand
from django.db import transaction
from phases.models import Exercise, GuideStep, ExternalActivity, QuizQuestion

PHASE1 = [
    (1, "Operações Básicas — Soma", "operacoes-soma", """✅ SOMA(<strong>núm1</strong>; [<strong>núm2</strong>]; ...)<br><br><strong>Função:</strong> Soma todos os números em um intervalo de células.<br><strong>Exemplo de Uso:</strong> Para calcular o total da coluna 'Quantidade'.<br><strong>Fórmula:</strong> <code>=SOMA(E2:E11)</code><br><strong>Explicação:</strong> Adiciona todos os valores do intervalo de E2 a E11.""", "SOMA"),
    (2, "Operações Básicas — Subtração", "operacoes-subtracao", """✅ Subtração com Operador (-)<br><br><strong>Função:</strong> Calcula a diferença entre dois números.<br><strong>Exemplo de Uso:</strong> Se você tivesse uma coluna 'Desconto', poderia calcular 'Total Venda' - 'Desconto'.<br><strong>Fórmula:</strong> <code>=G2-100</code><br><strong>Explicação:</strong> Subtrai 100 do valor da célula G2.""", "-"),
    (3, "Operações Básicas — Multiplicação", "operacoes-multiplicacao", """✅ Multiplicação com Operador (*)<br><br><strong>Função:</strong> Multiplica números.<br><strong>Exemplo de Uso:</strong> Calcular o 'Total Venda' a partir da 'Quantidade' e 'Valor Unitário'.<br><strong>Fórmula:</strong> <code>=E2*F2</code><br><strong>Explicação:</strong> Multiplica o valor da célula E2 pelo valor da célula F2.""", "*"),
    (4, "Operações Básicas — Divisão", "operacoes-divisao", """✅ Divisão com Operador (/)<br><br><strong>Função:</strong> Divide um número por outro.<br><strong>Exemplo de Uso:</strong> Calcular o preço médio por unidade em um pacote.<br><strong>Fórmula:</strong> <code>=G2/E2</code><br><strong>Explicação:</strong> Divide o 'Total Venda' (G2) pela 'Quantidade' (E2) para encontrar o 'Valor Unitário'.""", "/"),
    (5, "MÉDIA — Média Aritmética", "media-aritmetica", """✅ MÉDIA(<strong>núm1</strong>; [<strong>núm2</strong>]; ...)<br><br><strong>Função:</strong> Retorna a média aritmética de seus argumentos.<br><strong>Exemplo de Uso:</strong> Calcular o valor médio de todas as vendas.<br><strong>Fórmula:</strong> <code>=MÉDIA(G2:G11)</code><br><strong>Explicação:</strong> Calcula a média de todos os valores no intervalo de G2 a G11.""", "MÉDIA"),
    (6, "MÁXIMO — Encontrar o Maior Valor", "maximo-maior-valor", """✅ MÁXIMO(<strong>núm1</strong>; [<strong>núm2</strong>]; ...)<br><br><strong>Função:</strong> Retorna o maior valor em um conjunto de valores.<br><strong>Exemplo de Uso:</strong> Descobrir qual foi a venda de maior valor.<br><strong>Fórmula:</strong> <code>=MÁXIMO(G2:G11)</code><br><strong>Explicação:</strong> Encontra o maior valor de 'Total Venda' no intervalo de G2 a G11.""", "MÁXIMO"),
    (7, "MÍNIMO — Encontrar o Menor Valor", "minimo-menor-valor", """✅ MÍNIMO(<strong>núm1</strong>; [<strong>núm2</strong>]; ...)<br><br><strong>Função:</strong> Retorna o menor valor em um conjunto de valores.<br><strong>Exemplo de Uso:</strong> Descobrir qual foi a venda de menor valor.<br><strong>Fórmula:</strong> <code>=MÍNIMO(G2:G11)</code><br><strong>Explicação:</strong> Encontra o menor valor de 'Total Venda' no intervalo de G2 a G11.""", "MÍNIMO"),
    (8, "SOMASE — Total de vendas por vendedora(o)", "somase-total-vendas", """✅ SOMASE(<strong>intervalo_critério</strong>; <strong>critério</strong>; <strong>intervalo_soma</strong>)<br><br>
<strong>Função:</strong> Soma valores que atendem a um único critério.<br><br>
<strong>Parâmetros:</strong><br>
- <strong>intervalo_critério</strong> (obrigatório): onde será feita a verificação do critério.<br>
- <strong>critério</strong> (obrigatório): o valor ou condição a ser comparado.<br>
- <strong>intervalo_soma</strong> (obrigatório): intervalo com os valores a somar.<br><br>

<strong>Exemplo:</strong> <code>=SOMASE(C2:C101; "SP"; G2:G101)</code><br><br>

<strong>Pergunta:</strong> Qual o total de vendas realizadas pela vendedora 'Fernanda’?<br>
<strong>Fórmula:</strong> <code>=SOMASE(B2:B11; "Fernanda"; G2:G11)</code><br>
<strong>Explicação:</strong> Soma os valores da coluna G (Total Venda) quando o nome da vendedora na coluna B for "Fernanda".""", "SOMASE"),
    (9, "SOMASES — Soma por múltiplos critérios", "somases-multiplos-criterios", """✅ SOMASES(<strong>intervalo_soma</strong>; <strong>intervalo1</strong>; <strong>critério1</strong>; [<strong>intervalo2</strong>; <strong>critério2</strong>]...)<br><br>
<strong>Função:</strong> Soma com múltiplos critérios.<br>
<strong>Parâmetros:</strong><br><br>
- <strong>intervalo_soma</strong> (obrigatório)<br>
- <strong>intervalo1</strong>, <strong>critério1</strong> (obrigatórios)<br>
- <strong>intervalo2</strong>, <strong>critério2</strong> (opcionais, podem ser vários)<br><br>
<strong>Exemplo:</strong> <code>=SOMASES(G2:G101; B2:B101;"Carlos"; C2:C101;"SP")</code><br><br>
<strong>Pergunta:</strong> Qual o total vendido por 'Marcos' na região 'SP’?<br>
<strong>Fórmula:</strong> <code>=SOMASES(G2:G11; B2:B11;"Marcos"; C2:C11;"SP")</code><br>
<strong>Explicação:</strong> Soma os valores da coluna G quando o vendedor na coluna B for 'Marcos' E a região na coluna C for 'SP'.""", "SOMASES"),
    (10, "CONT.SE — Contar ocorrências", "cont-se-ocorrencias", """✅ CONT.SE(<strong>intervalo</strong>; <strong>critério</strong>)<br><br>
<strong>Função:</strong> Conta quantas vezes um valor aparece.<br>
<strong>Parâmetros:</strong><br><br>
- <strong>intervalo</strong> (obrigatório): intervalo de dados a ser analisado.<br>
- <strong>critério</strong> (obrigatório): valor ou condição de contagem.<br><br>
<strong>Exemplo:</strong> <code>=CONT.SE(B2:B101; "Carlos")</code><br><br>
<strong>Pergunta:</strong> Quantas vezes o produto 'Monitor' aparece na base?<br>
<strong>Fórmula:</strong> <code>=CONT.SE(D2:D11;"Monitor")</code><br>
<strong>Explicação:</strong> Conta o número de células no intervalo D2:D11 que são exatamente iguais a "Monitor".""", "CONT.SE"),
    (11, "CONT.SES — Contagem com dois critérios", "cont-ses-dois-criterios", """✅ CONT.SES(<strong>intervalo1</strong>; <strong>critério1</strong>; [<strong>intervalo2</strong>; <strong>critério2</strong>]...)<br><br>
<strong>Função:</strong> Conta com vários critérios simultâneos.<br>
<strong>Parâmetros:</strong><br><br>
- <strong>intervalo1</strong>, <strong>critério1</strong> (obrigatórios)<br>
- <strong>intervalo2</strong>, <strong>critério2</strong> (opcionais)<br><br>
<strong>Exemplo:</strong> <code>=CONT.SES(B2:B101;"Carlos"; C2:C101;"SP")</code><br><br>
<strong>Pergunta:</strong> Quantas vendas foram feitas pela vendedora 'Ana' na região 'RJ'?<br>
<strong>Fórmula:</strong> <code>=CONT.SES(B2:B11;"Ana"; C2:C11;"RJ")</code><br>
<strong>Explicação:</strong> Conta as linhas onde o vendedor na coluna B é 'Ana' E a região na coluna C é 'RJ'.""", "CONT.SES"),
    (12, "MÉDIASE — Média com critério", "mediase-media-criterio", """✅ MÉDIASE(<strong>intervalo_critério</strong>; <strong>critério</strong>; [<strong>intervalo_média</strong>])<br><br>
<strong>Função:</strong> Calcula a média de valores que atendem a um único critério.<br>
<strong>Parâmetros:</strong><br><br>
- <strong>intervalo_critério</strong> (obrigatório): Onde será feita a verificação do critério.<br>
- <strong>critério</strong> (obrigatório): A condição a ser comparada.<br>
- <strong>intervalo_média</strong> (opcional): O intervalo com os valores para calcular a média. Se omitido, usa o `intervalo_critério`.<br><br>
<strong>Exemplo:</strong> <code>=MÉDIASE(C2:C11;"SP";G2:G11)</code><br><br>
<strong>Pergunta:</strong> Qual a média de vendas dos produtos na região 'SP'?<br>
<strong>Fórmula:</strong> <code>=MÉDIASE(C2:C11;"SP";G2:G11)</code><br>
<strong>Explicação:</strong> Calcula a média dos valores na coluna G (Total Venda) apenas para as linhas onde a Região na coluna C é 'SP'.""", "MÉDIASE"),
    (13, "SE — Teste lógico", "se-teste-logico", """✅ SE(<strong>teste_lógico</strong>; [<strong>valor_se_verdadeiro</strong>]; [<strong>valor_se_falso</strong>])<br><br>
<strong>Função:</strong> Verifica se uma condição é verdadeira e retorna um valor caso seja, ou outro valor caso seja falsa.<br>
<strong>Parâmetros:</strong><br><br>
- <strong>teste_lógico</strong> (obrigatório): A condição a ser avaliada.<br>
- <strong>valor_se_verdadeiro</strong> (opcional): O que retornar se a condição for verdadeira.<br>
- <strong>valor_se_falso</strong> (opcional): O que retornar se a condição for falsa.<br><br>
<strong>Exemplo:</strong> <code>=SE(G2>5000;"Meta Atingida";"Abaixo da Meta")</code><br><br>
<strong>Pergunta:</strong> Classifique as vendas em 'Meta Atingida' se o 'Total Venda' for maior que R$ 2.000,00, e 'Abaixo da Meta' caso contrário.<br>
<strong>Fórmula:</strong> <code>=SE(G2>2000;"Meta Atingida";"Abaixo da Meta")</code><br>
<strong>Explicação:</strong> Para cada linha, a fórmula verifica se o valor na coluna G é maior que 2000. Se for, exibe "Meta Atingida"; senão, exibe "Abaixo da Meta".""", "SE"),
    (14, "PROCV — Busca vertical", "procv-busca-vertical", """✅ PROCV(<strong>valor_procurado</strong>; <strong>matriz_tabela</strong>; <strong>núm_índice_coluna</strong>; [<strong>procurar_intervalo</strong>])<br><br>
<strong>Função:</strong> Procura um valor na primeira coluna de uma tabela e retorna um valor na mesma linha de uma coluna especificada.<br>
<strong>Parâmetros:</strong><br><br>
- <strong>valor_procurado</strong> (obrigatório): O valor a ser procurado.<br>
- <strong>matriz_tabela</strong> (obrigatório): O intervalo de células da tabela.<br>
- <strong>núm_índice_coluna</strong> (obrigatório): O número da coluna na tabela da qual o valor será retornado (a 1ª coluna é 1).<br>
- <strong>procurar_intervalo</strong> (opcional): `FALSO` para correspondência exata (mais comum); `VERDADEIRO` para aproximada.<br><br>
<strong>Pergunta:</strong> A partir do nome de um produto, como 'Mouse', qual o seu 'Valor Unitário'?<br>
<strong>Fórmula:</strong> <code>=PROCV("Mouse"; D2:G11; 3; FALSO)</code><br>
<strong>Explicação:</strong> Procura por "Mouse" na coluna D, e quando encontra, retorna o valor da 3ª coluna do intervalo (coluna F, 'Valor Unitário'). O `FALSO` garante uma busca exata.""", "PROCV"),
    (15, "SEERRO — Tratamento de Erros", "seerro-tratamento-erros", """✅ SEERRO(<strong>valor</strong>; <strong>valor_se_erro</strong>)<br><br>
<strong>Função:</strong> Retorna um valor que você especifica se uma fórmula gerar um erro; caso contrário, retorna o resultado da fórmula.<br>
<strong>Parâmetros:</strong><br><br>
- <strong>valor</strong> (obrigatório): A fórmula ou valor a ser verificado.<br>
- <strong>valor_se_erro</strong> (obrigatório): O valor a ser retornado se 'valor' resultar em erro.<br><br>
<strong>Pergunta:</strong> Como usar o PROCV para buscar um produto que não existe, como 'Cadeira', sem mostrar um erro feio?<br>
<strong>Fórmula:</strong> <code>=SEERRO(PROCV("Cadeira"; D2:G11; 3; FALSO); "Produto não encontrado")</code><br>
<strong>Explicação:</strong> A fórmula tenta executar o PROCV. Como 'Cadeira' não será encontrada, o PROCV retornaria um erro. O SEERRO captura esse erro e, em vez dele, exibe a mensagem "Produto não encontrado".""", "SEERRO"),
]

PHASE2_STEPS = [
    (1, 2, "Criar a Tabela", "Recrie a tabela de 'Controle de Estoque' que é exibida na página da Fase 02 em sua planilha."),
    (2, 2, "Calcular Saldo Atual", "Crie uma nova coluna chamada 'Saldo Atual'. Nesta coluna, calcule o estoque final de cada item usando a fórmula: Anterior + Entrada - Saída."),
    (3, 2, "Analisar Necessidade de Compra", "Crie outra coluna chamada 'Status'. Use a função SE para verificar se o 'Saldo Atual' é menor ou igual ao 'Estoque Mínimo'. Se for, a célula deve exibir \"Comprar\". Caso contrário, deve exibir \"OK\"."),
    (4, 2, "Calcular Totais", "Na linha abaixo da tabela, use a função SOMA para calcular os totais das colunas 'Anterior', 'Entrada', 'Saída' e 'Saldo Atual'."),
]

PHASE3_STEPS = [
    (1, 3, "Calcular Percentual de Abono", "Na coluna 'PERCENTUAL', use a função PROCV para buscar o percentual correspondente a cada salário na 'TABELA DE ABONO'. Dica: use a correspondência aproximada (VERDADEIRO no último argumento do PROCV)."),
    (2, 3, "Calcular Valor do Abono", "Na coluna 'ABONO (R$)', calcule o valor do abono multiplicando o 'SALÁRIO(R$)' pelo 'PERCENTUAL' encontrado."),
    (3, 3, "Calcular Salário Final", "Na coluna 'SALÁRIO FINAL', some o 'SALÁRIO(R$)' com o 'ABONO (R$)' para encontrar o valor final a ser recebido por cada funcionário."),
]

PHASE4_STEPS = [
    (1, 4, "Estrutura e Configuração", "Crie 3 abas: 'Dashboard', 'Receitas', 'Despesas'. Na aba 'Dashboard', crie uma área de 'Configurações' com: 'Mês/Ano de Referência' e 'Meta de Poupança (%)'."),
    (2, 4, "Categorias de Despesas", "Ainda na aba 'Dashboard', crie uma lista com suas categorias de despesas (Ex: Moradia, Transporte, Alimentação, Lazer, Saúde, Educação)."),
    (3, 4, "Registro de Receitas e Despesas", "Na aba 'Receitas', crie colunas: 'Data', 'Descrição', 'Valor'. Faça o mesmo na aba 'Despesas', adicionando uma coluna 'Categoria'. Use 'Validação de Dados' na coluna 'Categoria' para criar uma lista suspensa com as categorias que você definiu no Dashboard."),
    (4, 4, "Cálculos Principais no Dashboard", "No Dashboard, use 'SOMASES' para calcular: 'Total de Receitas' e 'Total de Despesas' do mês. Calcule o 'Saldo do Mês' (Receitas - Despesas)."),
    (5, 4, "Indicadores Visuais (KPIs)", "Crie um indicador de 'Status' com a função 'SE': se o Saldo for positivo, mostrar 'Superávit'; senão, 'Déficit'. Use formatação condicional para colorir a célula (verde para superávit, vermelho para déficit)."),
    (6, 4, "Gráfico de Despesas por Categoria", "Crie uma pequena tabela de resumo no Dashboard que some os gastos por categoria. Use esses dados para criar um Gráfico de Pizza que mostre para onde seu dinheiro está indo."),
    (7, 4, "Gráfico de Evolução Financeira", "Crie um Gráfico de Colunas simples comparando o 'Total de Receitas', 'Total de Despesas' e o 'Saldo do Mês' lado a lado."),
]

QUIZ_QUESTIONS = [
    # Fase 01
    (1, "Referências absolutas usam o símbolo $ (ex.: $B$3).", "Verdadeiro"),
    (1, "CONT.VALORES conta apenas células com números.", "Falso"),
    (1, "SOMASE pode somar um intervalo diferente do intervalo de critérios.", "Verdadeiro"),
    (1, "A média considera células vazias como zero por padrão.", "Falso"),
    (1, "Ctrl+; insere a data atual na célula.", "Verdadeiro"),
    (1, "Não é possível classificar uma lista que contém células mescladas.", "Verdadeiro"),
    (1, "Preenchimento Relâmpago detecta padrões e preenche automaticamente.", "Verdadeiro"),
    (1, "Formatação condicional altera o valor da célula.", "Falso"),
    (1, "Converter um intervalo em Tabela (Ctrl+T) habilita filtros automáticos.", "Verdadeiro"),
    (1, "A função SOMA ignora números armazenados como texto (ex.: \"10\").", "Verdadeiro"),
    # Fase 02
    (2, "Saldo atual pode ser calculado como Anterior + Entrada − Saída.", "Verdadeiro"),
    (2, "É possível sinalizar estoque abaixo do mínimo com SE.", "Verdadeiro"),
    (2, "Os formatos Contábil e Moeda são exatamente iguais.", "Falso"),
    (2, "Validação de Dados pode impedir entradas negativas na coluna Entrada.", "Verdadeiro"),
    (2, "SOMASES permite somar por produto e região ao mesmo tempo.", "Verdadeiro"),
    (2, "PROCV pode retornar valores de colunas à esquerda do valor procurado.", "Falso"),
    (2, "Formatar como Tabela permite ativar a Linha de Totais com SOMA automática.", "Verdadeiro"),
    (2, "Filtros automáticos não funcionam quando a lista é uma Tabela.", "Falso"),
    (2, "É possível ordenar por múltiplas colunas, como Produto e Código.", "Verdadeiro"),
    (2, "SOMASE não aceita critérios com operadores como \">=100\".", "Falso"),
    # Fase 03
    (3, "PROCV com correspondência exata usa o quarto argumento FALSO.", "Verdadeiro"),
    (3, "PROCV aproximado requer a primeira coluna do intervalo ordenada.", "Verdadeiro"),
    (3, "No PROCV, o índice da coluna começa em 0.", "Falso"),
    (3, "ÍNDICE+CORRESP pode substituir PROCV com mais flexibilidade.", "Verdadeiro"),
    (3, "Quando não encontra o valor, PROCV retorna #N/D.", "Verdadeiro"),
    (3, "Se houver duplicatas, PROCV retorna todas as correspondências.", "Falso"),
    (3, "SEERRO pode exibir um texto amigável quando PROCV falha.", "Verdadeiro"),
    (3, "PROCV diferencia maiúsculas de minúsculas.", "Falso"),
    (3, "Misturar números e texto (ex.: \"101\" vs 101) pode causar #N/D no PROCV.", "Verdadeiro"),
    (3, "PROCX consegue procurar à esquerda, ao contrário do PROCV.", "Verdadeiro"),
    # Fase 04
    # Fase 01
    (1, "Referências absolutas usam o símbolo $ (ex.: $B$3).", "Verdadeiro"),
    (1, "CONT.VALORES conta apenas células com números.", "Falso"),
    (1, "SOMASE pode somar um intervalo diferente do intervalo de critérios.", "Verdadeiro"),
    (1, "A média considera células vazias como zero por padrão.", "Falso"),
    (1, "Ctrl+; insere a data atual na célula.", "Verdadeiro"),
    (1, "Não é possível classificar uma lista que contém células mescladas.", "Verdadeiro"),
    (1, "Preenchimento Relâmpago detecta padrões e preenche automaticamente.", "Verdadeiro"),
    (1, "Formatação condicional altera o valor da célula.", "Falso"),
    (1, "Converter um intervalo em Tabela (Ctrl+T) habilita filtros automáticos.", "Verdadeiro"),
    (1, "A função SOMA ignora números armazenados como texto (ex.: \"10\").", "Verdadeiro"),
    # Fase 04
    (4, "SOMASES pode somar gastos por Categoria e por Mês simultaneamente.", "Verdadeiro"),
    (4, "Gráfico de pizza é ideal para 25–30 categorias distintas.", "Falso"),
    (4, "Referências estruturadas de Tabela permitem usar [@Valor] nas fórmulas.", "Verdadeiro"),
    (4, "A função MÊS devolve um número de 1 a 12 a partir de uma data.", "Verdadeiro"),
    (4, "Formatos personalizados permitem mostrar negativos em vermelho.", "Verdadeiro"),
    (4, "SE aninhados podem calcular faixas de desconto por valor.", "Verdadeiro"),
    (4, "Proteger planilha impede qualquer edição sem senha em todas as células.", "Falso"),
    (4, "Segmentação de Dados (Slicer) pode filtrar Tabelas e Tabelas Dinâmicas.", "Verdadeiro"),
    (4, "HOJE() atualiza automaticamente na abertura da planilha.", "Verdadeiro"),
    (4, "Não é possível criar listas suspensas com Validação de Dados.", "Falso"),
]

PHASE5_ACTIVITIES = [
    ("kahoot", "Quiz Final de Excel", "https://www.kahoot.it", "<iframe src='https://kahoot.it/embed/your-quiz-id' width='980' height='600'></iframe>"),
    
]

class Command(BaseCommand):
    help = "Popula exercícios da Fase 01 e passos da Fase 02"

    @transaction.atomic
    def handle(self, *args, **options):
        Exercise.objects.all().delete()
        GuideStep.objects.all().delete()
        QuizQuestion.objects.all().delete() # Limpa as perguntas do quiz
        ExternalActivity.objects.all().delete()
        self.stdout.write("Modelos antigos de Exercícios, Passos, Questões de Quiz e Atividades Externas deletados.")
        
        exercises_to_create = [
            Exercise(order=order, title=title, slug=slug, description=description, reference_formula=formula)
            for order, title, slug, description, formula in PHASE1
        ]
        Exercise.objects.bulk_create(exercises_to_create)
        self.stdout.write(self.style.SUCCESS("Fase 01 populada."))

        all_steps = PHASE2_STEPS + PHASE3_STEPS + PHASE4_STEPS
        steps_to_create = [
            GuideStep(order=order, phase=phase, title=title, instructions=instructions)
            for order, phase, title, instructions in all_steps
        ]
        GuideStep.objects.bulk_create(steps_to_create, batch_size=100)
        self.stdout.write(self.style.SUCCESS("Fases 02, 03 e 04 populadas."))
        
        quiz_questions_to_create = [
            QuizQuestion(phase_number=phase_number, question_text=question, answer_text=answer)
            for phase_number, question, answer in QUIZ_QUESTIONS
        ]
        QuizQuestion.objects.bulk_create(quiz_questions_to_create)
        self.stdout.write(self.style.SUCCESS("Questões do Quiz populadas."))

        activities_to_create = [
            ExternalActivity(provider=provider, title=title, url=url, embed_html=embed_html)
            for provider, title, url, embed_html in PHASE5_ACTIVITIES
        ]
        ExternalActivity.objects.bulk_create(activities_to_create)
        self.stdout.write(self.style.SUCCESS("Fase 05 (Atividades Externas) populada."))
