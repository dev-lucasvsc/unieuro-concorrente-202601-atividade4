import argparse
import os
import sys


def ler_header_ppm(caminho):
    with open(caminho, "rb") as f:
        tipo = f.readline().strip()
        if tipo != b'P6':
            raise ValueError(f"Formato inválido em {caminho}. Esperado PPM P6.")
        linha = f.readline().strip()
        while linha.startswith(b'#'):
            linha = f.readline().strip()
        largura, altura = map(int, linha.split())
        linha = f.readline().strip()
        while linha.startswith(b'#'):
            linha = f.readline().strip()
        valor_maximo = int(linha)
        offset_dados = f.tell()
    return largura, altura, valor_maximo, offset_dados


def juntar_imagens(pasta_entrada, arquivo_saida):
    arquivos = sorted([
        os.path.join(pasta_entrada, f)
        for f in os.listdir(pasta_entrada)
        if f.endswith(".ppm")
    ])

    if not arquivos:
        print(f"❌ Nenhum arquivo .ppm encontrado em '{pasta_entrada}/'")
        print("   Execute processar_paralelo.py primeiro.")
        sys.exit(1)

    # Lê dimensões da primeira parte para montar o cabeçalho final
    largura_ref, _, valor_maximo_ref, _ = ler_header_ppm(arquivos[0])

    # Calcula altura total somando a altura de cada parte
    altura_total = 0
    for caminho in arquivos:
        _, altura_parte, _, _ = ler_header_ppm(caminho)
        altura_total += altura_parte

    print(f"Juntando {len(arquivos)} partes...")
    print(f"Dimensão final: {largura_ref}x{altura_total}")
    print(f"Saída: {arquivo_saida}\n")

    header = f"P6\n{largura_ref} {altura_total}\n{valor_maximo_ref}\n".encode("ascii")

    with open(arquivo_saida, "wb") as fout:
        fout.write(header)

        for i, caminho in enumerate(arquivos):
            _, _, _, offset = ler_header_ppm(caminho)
            tamanho = os.path.getsize(caminho) - offset

            with open(caminho, "rb") as fin:
                fin.seek(offset)
                copiados = 0
                while copiados < tamanho:
                    bloco = fin.read(min(4 * 1024 * 1024, tamanho - copiados))  # 4 MB
                    if not bloco:
                        break
                    fout.write(bloco)
                    copiados += len(bloco)

            progresso = (i + 1) / len(arquivos) * 100
            print(f"  [{i:02d}] {os.path.basename(caminho)} → {progresso:.1f}%")

    tamanho_final_gb = os.path.getsize(arquivo_saida) / (1024 ** 3)
    print(f"\n✅ Imagem final gerada: {arquivo_saida}")
    print(f"   Tamanho: {tamanho_final_gb:.2f} GiB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Junta partes PPM em uma única imagem")
    parser.add_argument("arquivo_saida", help="Caminho da imagem PPM de saída final")
    parser.add_argument(
        "--pasta", type=str, default="partes_cinza",
        help="Pasta com as partes processadas (padrão: partes_cinza/)"
    )
    args = parser.parse_args()

    juntar_imagens(args.pasta, args.arquivo_saida)