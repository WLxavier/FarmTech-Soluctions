import os
import math
import time
import pandas as pd

# Armazenamento de dados
areas = [] 
insumos = []

# Lista de culturas disponíveis inicialmente
culturas = ["Milho", "Soja"]

# Lista de insumos disponíveis com suas dosagens em (mL/m²)
lista_insumos = {
    "Herbicida": 300,
    "Fertilizante": 250,
    "Inseticida": 200,
    "Fungicida": 150
}

def exportar_para_r():
    """
    Exporta os dados de insumos para um arquivo CSV para análise em R
    """
    df = pd.DataFrame(insumos)
    df.to_csv('Dados/dados_farmtech.csv', index=False)
    print('\nDados exportados com sucesso para Dados/dados_farmtech.csv')
    input("Pressione ENTER para continuar...")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def calcular_area_retangular(dimensoes):
    return dimensoes["comprimento"] * dimensoes["largura"]

def calcular_area_circular(dimensoes):
    return math.pi * (dimensoes["raio"] ** 2)

def calcular_area_triangular(dimensoes):
    return (dimensoes["base"] * dimensoes["altura"]) / 2

tipos_areas = {
    "Retangular": calcular_area_retangular,
    "Circular": calcular_area_circular,
    "Triangular": calcular_area_triangular
}

def calcular_area_ruas(ruas, largura_rua, comprimento_area):
    if ruas == 0:
        return 0
    return ruas * largura_rua * comprimento_area

def calcular_area_util(area_total, area_ruas):
    area_util = max(0, area_total - area_ruas)
    return area_util

def calcular_insumos(area_total, ruas, largura_rua, comprimento_area, cultura, insumo, dosagem):
    area_ruas = calcular_area_ruas(ruas, largura_rua, comprimento_area)
    
    area_util = calcular_area_util(area_total, area_ruas)
    
    total_ml = area_util * dosagem
    total_litros = total_ml / 1000
    
    return {
        "cultura": cultura,
        "insumo": insumo,
        "area_total": area_total,
        "area_util": area_util,
        "area_ruas": area_ruas,
        "quantidade_ml_metro": dosagem,
        "ruas": ruas,
        "largura_rua": largura_rua if ruas > 0 else 0,
        "comprimento_area": comprimento_area,
        "total_litros": total_litros
    }

def adicionar_cultura():
    limpar_tela()
    print("\n===== ADICIONAR NOVA CULTURA =====")
    nova_cultura = input("Digite o nome da nova cultura: ")
    
    if nova_cultura and nova_cultura not in culturas:
        culturas.append(nova_cultura)
        print(f"\nCultura '{nova_cultura}' adicionada com sucesso!")
    elif nova_cultura in culturas:
        print(f"\nA cultura '{nova_cultura}' já existe na lista!")
    else:
        print("\nNome de cultura inválido!")
    
    input("Pressione ENTER para continuar...")

def adicionar_insumo():
    limpar_tela()
    print("\n===== ADICIONAR NOVO INSUMO =====")
    novo_insumo = input("Digite o nome do novo insumo: ")
    
    if novo_insumo and novo_insumo not in lista_insumos:
        try:
            dosagem = float(input(f"Digite a dosagem padrão para {novo_insumo} (mL/m²): "))
            if dosagem <= 0:
                print("\nDosagem inválida. A dosagem deve ser positiva.")
                input("Pressione ENTER para continuar...")
                return
                
            lista_insumos[novo_insumo] = dosagem
            print(f"\nInsumo '{novo_insumo}' adicionado com sucesso!")
        except ValueError:
            print("\nDosagem inválida. Por favor, insira um valor numérico.")
    elif novo_insumo in lista_insumos:
        print(f"\nO insumo '{novo_insumo}' já existe na lista!")
    else:
        print("\nNome de insumo inválido!")
    
    input("Pressione ENTER para continuar...")

def entrada_dados():
    limpar_tela()
    print("\n===== ENTRADA DE DADOS =====")
    
    print("\nCulturas disponíveis:")
    for i, cultura in enumerate(culturas):
        print(f"{i+1} - {cultura}")
    print(f"{len(culturas)+1} - Adicionar nova cultura")
    
    try:
        escolha_cultura = int(input("Escolha a cultura: "))
        
        if escolha_cultura == len(culturas)+1:
            adicionar_cultura()
            return
        elif escolha_cultura < 1 or escolha_cultura > len(culturas):
            print("\nOpção inválida!")
            input("Pressione ENTER para continuar...")
            return
            
        cultura_selecionada = culturas[escolha_cultura-1]
        
        print("\nTipos de área disponíveis:")
        tipos_disponiveis = list(tipos_areas.keys())
        for i, tipo in enumerate(tipos_disponiveis):
            print(f"{i+1} - {tipo}")
        
        escolha_tipo = int(input("Escolha o tipo de área: "))
        if escolha_tipo < 1 or escolha_tipo > len(tipos_disponiveis):
            print("\nOpção inválida!")
            input("Pressione ENTER para continuar...")
            return
            
        tipo_area = tipos_disponiveis[escolha_tipo-1]
        
        dimensoes = {}
        comprimento_area = 0
        if tipo_area == "Retangular":
            dimensoes["comprimento"] = float(input("Comprimento da área (metros): "))
            dimensoes["largura"] = float(input("Largura da área (metros): "))
            comprimento_area = dimensoes["comprimento"]
            
            if dimensoes["comprimento"] <= 0 or dimensoes["largura"] <= 0:
                print("\nValores inválidos. Todos os valores devem ser positivos.")
                input("Pressione ENTER para continuar...")
                return
                
        elif tipo_area == "Circular":
            dimensoes["raio"] = float(input("Raio da área circular (metros): "))
            comprimento_area = dimensoes["raio"] * 2  # Diâmetro como comprimento
            
            if dimensoes["raio"] <= 0:
                print("\nValor inválido. O raio deve ser positivo.")
                input("Pressione ENTER para continuar...")
                return
                
        elif tipo_area == "Triangular":
            dimensoes["base"] = float(input("Base do triângulo (metros): "))
            dimensoes["altura"] = float(input("Altura do triângulo (metros): "))
            comprimento_area = dimensoes["base"]
            
            if dimensoes["base"] <= 0 or dimensoes["altura"] <= 0:
                print("\nValores inválidos. Todos os valores devem ser positivos.")
                input("Pressione ENTER para continuar...")
                return
        
        funcao_calculo = tipos_areas[tipo_area]
        area = funcao_calculo(dimensoes)
        
        registro_area = {
            "cultura": cultura_selecionada,
            "tipo_area": tipo_area,
            "dimensoes": dimensoes,
            "area": area,
            "comprimento_area": comprimento_area
        }
        areas.append(registro_area)
        
        print("\nInsumos disponíveis:")
        insumos_disponiveis = list(lista_insumos.keys())
        for i, insumo in enumerate(insumos_disponiveis):
            print(f"{i+1} - {insumo} ({lista_insumos[insumo]} mL/m²)")
        print(f"{len(insumos_disponiveis)+1} - Adicionar novo insumo")
        
        escolha_insumo = int(input("Escolha o insumo: "))
        
        if escolha_insumo == len(insumos_disponiveis)+1:
            adicionar_insumo()
            areas.pop()
            return
        elif escolha_insumo < 1 or escolha_insumo > len(insumos_disponiveis):
            print("\nOpção inválida!")
            areas.pop()
            input("Pressione ENTER para continuar...")
            return
            
        insumo_selecionado = insumos_disponiveis[escolha_insumo-1]
        dosagem_padrao = lista_insumos[insumo_selecionado]
        
        print(f"\nDosagem padrão para {insumo_selecionado}: {dosagem_padrao} mL/m²")
        personalizar = input("Deseja personalizar a dosagem? (S/N): ").upper()
        
        if personalizar == 'S':
            dosagem = float(input("Nova dosagem (mL/m²): "))
            if dosagem <= 0:
                print("\nValor inválido. A dosagem deve ser positiva.")
                areas.pop()
                input("Pressione ENTER para continuar...")
                return
        else:
            dosagem = dosagem_padrao
        
        ruas = int(input("Número de ruas na lavoura (0 para nenhuma rua): "))
        if ruas < 0:
            print("\nValor inválido. O número de ruas não pode ser negativo.")
            areas.pop()
            input("Pressione ENTER para continuar...")
            return
        
        largura_rua = 0
        if ruas > 0:
            largura_rua = float(input("Largura das ruas (metros): "))
            if largura_rua <= 0:
                print("\nValor inválido. A largura das ruas deve ser positiva.")
                areas.pop()
                input("Pressione ENTER para continuar...")
                return
        
        registro_insumo = calcular_insumos(area, ruas, largura_rua, comprimento_area, cultura_selecionada, insumo_selecionado, dosagem)
        insumos.append(registro_insumo)
        
        area_util = registro_insumo['area_util']
        area_ruas = registro_insumo['area_ruas']
        
        print(f"\nRegistro adicionado!")
        print(f"Área total: {area:.2f} m²")
        if ruas > 0:
            print(f"Área das ruas: {area_ruas:.2f} m²")
        print(f"Área útil para aplicação: {area_util:.2f} m²")
        print(f"Total de {insumo_selecionado} necessário: {registro_insumo['total_litros']:.2f} litros")
        input("Pressione ENTER para continuar...")
        
    except ValueError:
        print("\nEntrada inválida. Por favor, insira valores numéricos.")
        input("Pressione ENTER para continuar...")

def exibir_dados():
    limpar_tela()
    print("\n===== DADOS REGISTRADOS =====")
    
    if not areas or not insumos:
        print("Não há dados registrados.")
        input("Pressione ENTER para continuar...")
        return
    
    print("\n--- ÁREAS DE PLANTIO ---")
    for i, area in enumerate(areas):
        print(f"\nRegistro #{i+1}:")
        print(f"Cultura: {area['cultura']}")
        print(f"Tipo de Área: {area['tipo_area']}")
        
        if area['tipo_area'] == 'Retangular':
            print(f"Comprimento: {area['dimensoes']['comprimento']:.2f} m")
            print(f"Largura: {area['dimensoes']['largura']:.2f} m")
        elif area['tipo_area'] == 'Circular':
            print(f"Raio: {area['dimensoes']['raio']:.2f} m")
        elif area['tipo_area'] == 'Triangular':
            print(f"Base: {area['dimensoes']['base']:.2f} m")
            print(f"Altura: {area['dimensoes']['altura']:.2f} m")
            
        print(f"Área Total: {area['area']:.2f} m²")
    
    print("\n--- MANEJO DE INSUMOS ---")
    for i, insumo in enumerate(insumos):
        print(f"\nRegistro #{i+1}:")
        print(f"Cultura: {insumo['cultura']}")
        print(f"Insumo: {insumo['insumo']}")
        print(f"Área Total: {insumo['area_total']:.2f} m²")
        print(f"Número de Ruas: {insumo['ruas']}")
        
        if insumo['ruas'] > 0:
            print(f"Largura das Ruas: {insumo['largura_rua']:.2f} m")
            print(f"Área das Ruas: {insumo['area_ruas']:.2f} m²")
            
        print(f"Área Útil para Aplicação: {insumo['area_util']:.2f} m²")
        print(f"Dosagem: {insumo['quantidade_ml_metro']} mL/m²")
        print(f"Total de Insumo Necessário: {insumo['total_litros']:.2f} litros")
    
    input("\nPressione ENTER para continuar...")

def atualizar_dados():
    limpar_tela()
    print("\n===== ATUALIZAR DADOS =====")
    
    if not areas or not insumos:
        print("Não há dados para atualizar.")
        input("Pressione ENTER para continuar...")
        return
    
    print("Qual vetor deseja atualizar?")
    print("1 - Áreas de Plantio")
    print("2 - Manejo de Insumos")
    
    try:
        opcao = int(input("Opção: "))
        
        if opcao == 1:
            print("\n--- ÁREAS DE PLANTIO DISPONÍVEIS ---")
            for i, area in enumerate(areas):
                print(f"{i+1} - {area['cultura']} ({area['tipo_area']}): {area['area']:.2f} m²")
            
            indice = int(input("\nDigite o número do registro a atualizar: ")) - 1
            
            if 0 <= indice < len(areas):
                area_atual = areas[indice]
                
                print(f"\nAtualizando registro da cultura {area_atual['cultura']}")
                
                print("\nTipos de área disponíveis:")
                tipos_disponiveis = list(tipos_areas.keys())
                for i, tipo in enumerate(tipos_disponiveis):
                    print(f"{i+1} - {tipo}")
                
                escolha_tipo = int(input(f"Escolha o novo tipo de área (atual: {area_atual['tipo_area']}): "))
                if escolha_tipo < 1 or escolha_tipo > len(tipos_disponiveis):
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
                    return
                    
                tipo_area = tipos_disponiveis[escolha_tipo-1]
                
                dimensoes = {}
                comprimento_area = 0
                if tipo_area == "Retangular":
                    dimensoes["comprimento"] = float(input("Comprimento da área (metros): "))
                    dimensoes["largura"] = float(input("Largura da área (metros): "))
                    comprimento_area = dimensoes["comprimento"]
                    
                    if dimensoes["comprimento"] <= 0 or dimensoes["largura"] <= 0:
                        print("\nValores inválidos. Todos os valores devem ser positivos.")
                        input("Pressione ENTER para continuar...")
                        return
                        
                elif tipo_area == "Circular":
                    dimensoes["raio"] = float(input("Raio da área circular (metros): "))
                    comprimento_area = dimensoes["raio"] * 2
                    
                    if dimensoes["raio"] <= 0:
                        print("\nValor inválido. O raio deve ser positivo.")
                        input("Pressione ENTER para continuar...")
                        return
                        
                elif tipo_area == "Triangular":
                    dimensoes["base"] = float(input("Base do triângulo (metros): "))
                    dimensoes["altura"] = float(input("Altura do triângulo (metros): "))
                    comprimento_area = dimensoes["base"]
                    
                    if dimensoes["base"] <= 0 or dimensoes["altura"] <= 0:
                        print("\nValores inválidos. Todos os valores devem ser positivos.")
                        input("Pressione ENTER para continuar...")
                        return
                
                funcao_calculo = tipos_areas[tipo_area]
                area = funcao_calculo(dimensoes)
                
                areas[indice] = {
                    "cultura": area_atual['cultura'],
                    "tipo_area": tipo_area,
                    "dimensoes": dimensoes,
                    "area": area,
                    "comprimento_area": comprimento_area
                }
                
                ruas = int(input(f"Novo número de ruas (atual: {insumos[indice]['ruas']}, 0 para nenhuma rua): "))
                if ruas < 0:
                    print("\nValor inválido. O número de ruas não pode ser negativo.")
                    input("Pressione ENTER para continuar...")
                    return
                
                largura_rua = 0
                if ruas > 0:
                    largura_rua = float(input("Largura das ruas (metros): "))
                    if largura_rua <= 0:
                        print("\nValor inválido. A largura das ruas deve ser positiva.")
                        input("Pressione ENTER para continuar...")
                        return
                
                insumo_nome = insumos[indice]['insumo']
                dosagem_atual = insumos[indice]['quantidade_ml_metro']
                
                insumos[indice] = calcular_insumos(
                    area,
                    ruas,
                    largura_rua,
                    comprimento_area,
                    area_atual['cultura'],
                    insumo_nome,
                    dosagem_atual
                )
                
                area_util = insumos[indice]['area_util']
                area_ruas = insumos[indice]['area_ruas']
                
                print(f"\nRegistro atualizado!")
                print(f"Nova área total: {area:.2f} m²")
                if ruas > 0:
                    print(f"Nova área das ruas: {area_ruas:.2f} m²")
                print(f"Nova área útil para aplicação: {area_util:.2f} m²")
                print(f"Novo total de insumo necessário: {insumos[indice]['total_litros']:.2f} litros")
            else:
                print("\nÍndice inválido!")
        
        elif opcao == 2:
            print("\n--- MANEJO DE INSUMOS DISPONÍVEIS ---")
            for i, insumo in enumerate(insumos):
                print(f"{i+1} - {insumo['cultura']} ({insumo['insumo']}): {insumo['total_litros']:.2f} litros")
            
            indice = int(input("\nDigite o número do registro a atualizar: ")) - 1
            
            if 0 <= indice < len(insumos):
                insumo_atual = insumos[indice]
                
                print(f"\nAtualizando registro de insumo para {insumo_atual['cultura']}")
                
                print("\nInsumos disponíveis:")
                insumos_disponiveis = list(lista_insumos.keys())
                for i, insumo_nome in enumerate(insumos_disponiveis):
                    print(f"{i+1} - {insumo_nome} ({lista_insumos[insumo_nome]} mL/m²)")
                print(f"{len(insumos_disponiveis)+1} - Adicionar novo insumo")
                print(f"{len(insumos_disponiveis)+2} - Manter insumo atual ({insumo_atual['insumo']})")
                
                escolha_insumo = int(input("Escolha o insumo: "))
                
                if escolha_insumo == len(insumos_disponiveis)+1:
                    adicionar_insumo()
                    return
                elif escolha_insumo == len(insumos_disponiveis)+2:
                    insumo_selecionado = insumo_atual['insumo']
                    dosagem_padrao = insumo_atual['quantidade_ml_metro']
                elif 1 <= escolha_insumo <= len(insumos_disponiveis):
                    insumo_selecionado = insumos_disponiveis[escolha_insumo-1]
                    dosagem_padrao = lista_insumos[insumo_selecionado]
                else:
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
                    return
                
                print(f"\nDosagem padrão para {insumo_selecionado}: {dosagem_padrao} mL/m²")
                personalizar = input("Deseja personalizar a dosagem? (S/N): ").upper()
                
                if personalizar == 'S':
                    dosagem = float(input("Nova dosagem (mL/m²): "))
                    if dosagem <= 0:
                        print("\nValor inválido. A dosagem deve ser positiva.")
                        input("Pressione ENTER para continuar...")
                        return
                else:
                    dosagem = dosagem_padrao
                
                ruas = int(input(f"Novo número de ruas (atual: {insumo_atual['ruas']}, 0 para nenhuma rua): "))
                if ruas < 0:
                    print("\nValor inválido. O número de ruas não pode ser negativo.")
                    input("Pressione ENTER para continuar...")
                    return
                
                largura_rua = 0
                if ruas > 0:
                    largura_rua = float(input("Largura das ruas (metros): "))
                    if largura_rua <= 0:
                        print("\nValor inválido. A largura das ruas deve ser positiva.")
                        input("Pressione ENTER para continuar...")
                        return
                
                insumos[indice] = calcular_insumos(
                    insumo_atual['area_total'],
                    ruas,
                    largura_rua,
                    insumo_atual['comprimento_area'],
                    insumo_atual['cultura'],
                    insumo_selecionado,
                    dosagem
                )
                
                area_util = insumos[indice]['area_util']
                area_ruas = insumos[indice]['area_ruas']
                
                print(f"\nRegistro atualizado!")
                print(f"Nova área útil para aplicação: {area_util:.2f} m²")
                if ruas > 0:
                    print(f"Nova área das ruas: {area_ruas:.2f} m²")
                print(f"Novo total de insumo necessário: {insumos[indice]['total_litros']:.2f} litros")
            else:
                print("\nÍndice inválido!")
        
        else:
            print("\nOpção inválida!")
        
        input("Pressione ENTER para continuar...")
    
    except ValueError:
        print("\nEntrada inválida. Por favor, insira valores numéricos.")
        input("Pressione ENTER para continuar...")

def deletar_dados():
    limpar_tela()
    print("\n===== DELETAR DADOS =====")
    
    if not areas or not insumos:
        print("Não há dados para deletar.")
        input("Pressione ENTER para continuar...")
        return
    
    print("Qual registro deseja deletar?")
    for i, (area, insumo) in enumerate(zip(areas, insumos)):
        print(f"{i+1} - {area['cultura']} - Área: {area['area']:.2f} m² - Insumo: {insumo['total_litros']:.2f} litros")
    
    try:
        indice = int(input("\nDigite o número do registro a deletar (0 para cancelar): ")) - 1
        
        if indice == -1:  # Cancelar
            print("\nOperação cancelada.")
        elif 0 <= indice < len(areas):
            cultura = areas[indice]['cultura']
            areas.pop(indice)
            insumos.pop(indice)
            print(f"\nRegistro da cultura {cultura} deletado com sucesso!")
        else:
            print("\nÍndice inválido!")
        
        input("Pressione ENTER para continuar...")
    
    except ValueError:
        print("\nEntrada inválida. Por favor, insira um valor numérico.")
        input("Pressione ENTER para continuar...")

def exibir_menu():
    limpar_tela()
    print("\n====================================")
    print("  FARMTECH SOLUTIONS - AGRICULTURA DIGITAL")
    print("====================================")
    print("1 - Entrada de Dados")
    print("2 - Exibir Dados")
    print("3 - Atualizar Dados")
    print("4 - Deletar Dados")
    print("5 - Adicionar Nova Cultura")
    print("6 - Adicionar Novo Insumo")
    print("7 - Exportar Dados para Análise em R")
    print("0 - Sair do Programa")
    print("====================================")
    return input("Escolha uma opção: ")

def main():
    while True:
        opcao = exibir_menu()
        
        if opcao == '1':
            entrada_dados()
        elif opcao == '2':
            exibir_dados()
        elif opcao == '3':
            atualizar_dados()
        elif opcao == '4':
            deletar_dados()
        elif opcao == '5':
            adicionar_cultura()
        elif opcao == '6':
            adicionar_insumo()
        elif opcao == '7':
            exportar_para_r()
        elif opcao == '0':
            limpar_tela()
            print("Obrigado por utilizar o sistema da FarmTech Solutions!")
            time.sleep(3)
            break
        else:
            print("\nOpção inválida! Por favor, tente novamente.")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()