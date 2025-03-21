library(readr)
library(dplyr)
library(ggplot2)

# le o arquivo
ler_dados <- function(arquivo = "../Dados/dados_farmtech.csv") {
  dados <- read_csv(arquivo)
  print("Dados carregados com sucesso!")
  print(head(dados))
  return(dados)
}

# analise dos dados pela cultura
analisar_culturas <- function(dados) {
  resumo_culturas <- dados %>%
    group_by(cultura) %>%
    summarise(
      media_area = mean(area_total, na.rm = TRUE),
      media_area_util = mean(area_util, na.rm = TRUE),
      media_litros = mean(total_litros, na.rm = TRUE),
      quantidade_registros = n()
    )
  
  print("Resumo por cultura:")
  print(resumo_culturas)
  return(resumo_culturas)
}

# analise dos insulmos
analisar_insumos <- function(dados) {
  resumo_insumos <- dados %>%
    group_by(insumo) %>%
    summarise(
      media_dosagem = mean(quantidade_ml_metro, na.rm = TRUE),
      media_litros = mean(total_litros, na.rm = TRUE),
      quantidade_registros = n()
    )
  print("Resumo por insumo:")
  print(resumo_insumos)
  return(resumo_insumos)
}

# graficos
criar_graficos <- function(dados) {
  # Gráfico de barras: Área das culturas
  grafico1 <- ggplot(dados, aes(x = cultura, y = area_total, fill = cultura)) +
    geom_bar(stat = "identity") +
    labs(title = "Área Total por Cultura",
         x = "Cultura",
         y = "Área Total (m²)") +
    theme_minimal()
  
  # Gráfico de barras: Consumo por cultura
  grafico2 <- ggplot(dados, aes(x = cultura, y = total_litros, fill = insumo)) +
    geom_bar(stat = "identity", position = "dodge") +
    labs(title = "Consumo de Insumos por Cultura",
         x = "Cultura",
         y = "Total de Insumos (litros)") +
    theme_minimal()
  
  # Mostrar os gráficos
  print(grafico1)
  print(grafico2)
  
  return(list(grafico_area = grafico1, grafico_insumos = grafico2))
}

# relatorio em texto
criar_relatorio <- function(resumo_culturas, resumo_insumos, arquivo = "relatorio_simples.txt") {
  sink(arquivo)
  
  cat("=== RELATÓRIO FARMTECH SOLUTIONS ===\n\n")

  cat("RESUMO POR CULTURA:\n")
  print(resumo_culturas)
  
  cat("\nRESUMO POR INSUMO:\n")
  print(resumo_insumos)
  
  sink()
  print(paste("Relatório salvo em:", arquivo))
}

# Função para executar as analises jnt
analisar_dados <- function(arquivo = "dados_farmtech.csv") {
  dados <- ler_dados(arquivo)
  if (is.null(dados)) return()
  
  resumo_culturas <- analisar_culturas(dados)
  
  resumo_insumos <- analisar_insumos(dados)
  
  graficos <- criar_graficos(dados)
  
  criar_relatorio(resumo_culturas, resumo_insumos)
  
  return(list(
    dados = dados,
    resumo_culturas = resumo_culturas,
    resumo_insumos = resumo_insumos,
    graficos = graficos
  ))
}