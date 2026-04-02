import argparse
import os


def ler_header_ppm(f):
    tipo = f.readline().strip()
    if tipo != b'P6':
        raise ValueError("Formato não suportado. Esperado PPM P6.")
    linha = f.readline().strip()
    while linha.startswith(b'#'):
        linha = f.readline().strip()
    largura, altura = map(int, linha.split())
    linha = f.readline().strip()
    while linha.startswith(b'#'):
        linha = f.readline().strip()
    valor_maximo = int(linha)
    if valor_maximo != 255:
        raise ValueError("Somente PPM com max=255 suportado.")
    offset_dados = f.tell()
    return largura, altura, valor_maximo, offset_dados


def dividir_imagem(arquivo_entrada, n_partes=12, pasta_saida="partes"):
    os.makedirs(pasta_saida, exist_ok=True)

    with open(arquivo_entrada, "rb") as f:
        largura, altura, valor_maximo, offset_dados = ler_header_ppm(f)

        print(f"Imagem: {largura}x{altura}")
        print(f"Dividindo em {n_partes} partes → pasta '{pasta_saida}/'")
        print()

        bytes_por_linha = largura * 3
        linhas_por_parte = altura // n_partes
        f.seek(offset_dados)

        for i in range(n_partes):
            inicio = i * linhas_por_parte
            fim = (i + 1) * linhas_por_parte if i < n_partes - 1 else altura
            n_linhas = fim - inicio

            caminho = os.path.join(pasta_saida, f"parte_{i:02d}.ppm")
            header = f"P6\n{largura} {n_linhas}\n{valor_maximo}\n".encode("ascii")
            dados = f.read(n_linhas * bytes_por_linha)

            with open(caminho, "wb") as fout:
                fout.write(header)
                fout.write(dados)

            tamanho_mb = os.path.getsize(caminho) / (1024 ** 2)
            print(f"  Parte {i:02d}: linhas {inicio}–{fim - 1} → {caminho} ({tamanho_mb:.0f} MB)")

    print(f"\n✅ Divisão concluída! {n_partes} arquivos gerados em '{pasta_saida}/'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Divide uma imagem PPM em partes horizontais")
    parser.add_argument("arquivo_entrada", help="Caminho da imagem PPM de entrada")
    parser.add_argument("--partes", type=int, default=12, help="Número de partes (padrão: 12)")
    parser.add_argument("--pasta", type=str, default="partes", help="Pasta de saída (padrão: partes/)")
    args = parser.parse_args()

    dividir_imagem(args.arquivo_entrada, args.partes, args.pasta)