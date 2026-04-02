import numpy as np

def gerar_imagem_ppm_1gb(
    caminho_saida="imagem_aleatoria_1gb.ppm",
    largura=18918,
    altura=18918,
    linhas_por_bloco=256,
    seed=None
):
    """
    Gera uma imagem RGB aleatória em formato PPM binário (P6),
    com tamanho aproximado de 1 GiB.

    Fórmula:
        tamanho_dados = largura * altura * 3 bytes
    pois cada pixel RGB usa 3 bytes."

    Para largura=18918 e altura=18918:
        18918 * 18918 * 3 = 1.073.671.572 bytes
    O que fica muito próximo de 1 GiB (1.073.741.824 bytes),
    somando ainda alguns bytes do cabeçalho.
    """

    rng = np.random.default_rng(seed)

    # Cabeçalho do formato PPM P6
    header = f"P6\n{largura} {altura}\n255\n".encode("ascii")

    total_bytes_pixels = largura * altura * 3
    total_bytes_estimado = len(header) + total_bytes_pixels

    print(f"Gerando arquivo: {caminho_saida}")
    print(f"Dimensões: {largura} x {altura}")
    print(f"Tamanho estimado: {total_bytes_estimado / (1024**3):.4f} GiB")

    with open(caminho_saida, "wb") as f:
        f.write(header)

        for y in range(0, altura, linhas_por_bloco):
            bloco_altura = min(linhas_por_bloco, altura - y)

            # Gera um bloco RGB aleatório
            bloco = rng.integers(
                0, 256,
                size=(bloco_altura, largura, 3),
                dtype=np.uint8
            )

            f.write(bloco.tobytes())

            progresso = (y + bloco_altura) / altura * 100
            print(f"Progresso: {progresso:6.2f}%")

    print("Concluído com sucesso!")


if __name__ == "__main__":
    gerar_imagem_ppm_1gb(
        caminho_saida="imagem_aleatoria_1gb.ppm",
        largura=75672,
        altura=75672,
        linhas_por_bloco=256,
        seed=42
    )

#18918 x 18918 x 3 = 1.073.671.572 bytes
#375672 x 375672 x 3 = 4.286.685.632 bytes (aprox 4 GiB)
#75672 x 75672 x 3 = 17.146.742.528 bytes (aprox 16 GiB)
