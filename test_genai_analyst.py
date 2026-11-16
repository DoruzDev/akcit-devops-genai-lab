from genai_analyst import mascarar_segredos, montar_mensagens, trecho_relevante


def test_mascara_tokens_conhecidos():
    log = "token=abc123 glpat-AAAAAAAAAAAAAAAAAAAA ghp_BBBBBBBBBBBBBBBBBBBBBBBB"

    mascarado = mascarar_segredos(log)

    assert "abc123" not in mascarado
    assert "glpat-" not in mascarado
    assert "ghp_" not in mascarado


def test_mascara_o_valor_exato_dos_segredos_do_ambiente():
    assert mascarar_segredos("chave usada: valor-secreto-123", ["valor-secreto-123"]) == (
        "chave usada: [REMOVIDO]"
    )


def test_trecho_relevante_comeca_nas_falhas_do_pytest():
    log = "coletando...\n" * 50 + "=========== FAILURES ===========\nTypeError: erro\n"

    trecho = trecho_relevante(log)

    assert trecho.startswith("=========== FAILURES")
    assert "TypeError" in trecho


def test_mensagem_avisa_que_log_e_dado_nao_confiavel():
    sistema, usuario = montar_mensagens("log", "diff")

    assert "não confiáveis" in sistema["content"]
    assert "log" in usuario["content"] and "diff" in usuario["content"]
