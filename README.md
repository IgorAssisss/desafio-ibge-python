# desafio-ibge-python
O objetivo principal é processar uma lista de entrada contendo nomes de cidades e suas populações, cruzando essas informações com a base de dados oficial do IBGE para validar os dados e gerar estatísticas precisas.

Extração e Limpeza: Ler um arquivo CSV com erros de digitação e normalizar os nomes para comparação.

Enriquecimento via API: Consultar a API de localidades do IBGE para obter informações oficiais como UF, Região e o ID do município.

Tratamento de Dados: Utilizar lógica de busca aproximada (como o difflib) para corrigir grafias incorretas (ex: "Curitba" para "Curitiba").

Cálculo de Estatísticas: Gerar um resumo contendo o total de municípios processados, a soma da população das cidades encontradas e a média populacional agrupada por região.
